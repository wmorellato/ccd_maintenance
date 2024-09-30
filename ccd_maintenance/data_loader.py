import os
import queue
import logging

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from gemmi import cif

from ccd_maintenance.models import get_table, cast_type, metadata_obj

logger = logging.getLogger(__name__)


def lookup_ccd_fs(root_dir):
    """
    Lookup the CCD files in the given directory and return the list of files.
    """
    for root, _, files in os.walk(root_dir):
        if "REMOVED" in root or "FULL" in root or "CVS" in root:
            continue

        for file in files:
            if "cif-parser-ascii" in file:
                continue

            if file.endswith(".cif"):
                yield os.path.join(root, file)


class ChemCompReader:
    def __init__(self, config):
        self.config = config
    
    def _table_to_dict(self, category, table):
        sql_table = get_table(category.lstrip("_"))
        if sql_table is None:
            logger.error(f"Model not found for {category}")
            return

        items = [t.split(".")[1] for t in table.tags]
        rows = []

        for r in table:
            row = {}
            for c in sql_table.c:
                if c.name == "Component_ID" and self._cc_id:
                    row[c.name] = self._cc_id
                    continue

                if c.name not in items:
                    row[c.name] = None
                    continue

                row[c.name] = cast_type(sql_table, c.name, cif.as_string(r[c.name]))
            rows.append(row)

        return rows

    def read(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.debug(f"Reading file: {file_path}")

        cc_data = {}
        doc = cif.read(file_path)
        block = doc[-1]

        if not block:
            raise ValueError(f"No data block found in the file: {file_path}")

        self._cc_id = block.name
        for cat in self.config.chem_comp_categories:
            table = block.find_mmcif_category(cat)

            if not table:
                logger.debug(f"Category {cat} not found in {file_path}")
                continue
        
            cc_data[cat] = self._table_to_dict(cat, table)

        return cc_data


class DataLoader:
    def __init__(self, config, engine, ccd_root, batch_size=10):
        self.config = config
        self.engine = engine
        self.ccd_root = ccd_root
        self.batch_size = batch_size

    def _setup_schema(self):
        with self.engine.connect() as conn:
            with conn.begin():
                metadata_obj.drop_all(conn)
                metadata_obj.create_all(conn)
                logger.info("Database schema created")

    def _read_data(self, cc_file):
        reader = ChemCompReader(config=self.config)

        try:
            return reader.read(cc_file)
        except Exception as e:
            logger.error(f"Error reading file {cc_file}: {e}")
            return {}

    def _load_multi(self, batch_data):
        grouped_data = defaultdict(list)
        for entry in batch_data:
            for category, data in entry.items():
                grouped_data[category].extend(data)

        with self.engine.connect() as conn:
            with conn.begin():
                logger.info("Loading batch into the database")

                for category, data in grouped_data.items():
                    table = get_table(category.lstrip("_"))
                    if table is None:
                        continue

                    conn.execute(table.insert(), data)

    def _data_builder_task(self, worker, file_queue):
        db_batch = []

        while True:
            try:
                cc_file = file_queue.get()
                file_queue.task_done()
            except file_queue.Empty:
                break

            if cc_file is None:
                break

            data = self._read_data(cc_file)
            if data:
                db_batch.append(data)

            if len(db_batch) >= self.batch_size:
                try:
                    self._load_multi(db_batch)
                except Exception as e:
                    logger.error(f"Error loading data for worker {worker} from {cc_file}: {str(e)}")
                finally:
                    db_batch.clear()

    def load(self):
        file_queue = queue.Queue(maxsize=200)
        self._setup_schema()

        with ThreadPoolExecutor(max_workers=self.config.num_threads) as executor:
            futures = [executor.submit(self._data_builder_task, worker, file_queue) for worker in range(self.config.num_threads)]

            for cc_file in lookup_ccd_fs(self.ccd_root):
                file_queue.put(cc_file)

            file_queue.join()

            # stop signal for the workers
            for _ in range(self.config.num_threads):
                file_queue.put(None)

            for f in as_completed(futures):
                f.result()
