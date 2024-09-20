import os
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
        if os.path.basename(root) in ("CVS", "REMOVED", "FULL"):
            continue

        for file in files:
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
            for i in items:
                if i not in sql_table.c:
                    logger.debug(f"Ignoring item {i} in {category}")
                    continue

                row[i] = cast_type(sql_table, i, cif.as_string(r[i]))
            rows.append(row)
        
        return rows

    def read(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info(f"Reading file: {file_path}")

        cc_data = {}
        doc = cif.read(file_path)
        block = doc[-1]

        if not block:
            raise ValueError(f"No data block found in the file: {file_path}")
        
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

    def _read_data(self, cc_file):
        reader = ChemCompReader(config=self.config)
        return reader.read(cc_file)

    def _load_multi(self, batch_data):
        grouped_data = defaultdict(list)
        for entry in batch_data:
            for category, data in entry.items():
                grouped_data[category].extend(data)

        with self.engine.connect() as conn:
            with conn.begin():                
                for category, data in grouped_data.items():
                    table = get_table(category.lstrip("_"))
                    if table is None:
                        continue

                    conn.execute(table.insert(), data)

    def load(self):
        self._setup_schema()

        cc_data_batch = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._read_data, cc_file) for cc_file in lookup_ccd_fs(self.ccd_root)]

            for future in as_completed(futures):
                cc_data = future.result()
                cc_data_batch.append(cc_data)

                if len(cc_data_batch) >= self.batch_size:
                    # self._load_multi(cc_data_batch)
                    cc_data_batch.clear()
            
            if cc_data_batch:
                self._load_multi(cc_data_batch)
                cc_data_batch.clear()
