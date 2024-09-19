import os
import logging

from gemmi import cif

from ccd_maintenance.models import get_table, is_number

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
                    logger.warning(f"Ignoring item {i} in {category}")
                    continue

                if is_number(sql_table, i):
                    row[i] = cif.as_number(r[i])
                else:
                    row[i] = cif.as_string(r[i])

            print(row)
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
                logger.warning(f"Category {cat} not found in {file_path}")
                continue
        
            cc_data[cat] = self._table_to_dict(cat, table)

        return cc_data
