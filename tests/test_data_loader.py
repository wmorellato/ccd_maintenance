import os
import pytest
import shutil
import logging

from sqlalchemy import create_engine, MetaData, select

from ccd_maintenance.config import Config
from ccd_maintenance.models import metadata_obj, chem_comp
from ccd_maintenance.data_loader import lookup_ccd_fs, ChemCompReader, DataLoader

logger = logging.getLogger(__name__)


@pytest.fixture
def ligand_dict(tmp_path):
    # Define the examples
    cc_entries = [
        '0/001/001.cif',
        'A/ABC/ABC.cif',
        'M/MIL/MIL.cif',
        'T/TON/TON.cif',
    ]

    support_dirs = [
        'FULL/comp.cif',
        'REMOVED/foo.cif'
    ]

    for sd in support_dirs:
        file_path = tmp_path / sd
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write('Mock content')

    # Create the directory structure and files
    for cc in cc_entries:
        file_path = tmp_path / cc
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(file_path), "CVS"), exist_ok=True)
        shutil.copy(os.path.join("tests", "fixtures", os.path.basename(cc)), file_path)        

    # Print the temporary directory path
    logger.info(f"Mock CCD directory structure created in: {tmp_path}")
    yield tmp_path

    # Cleanup the temporary directory
    shutil.rmtree(tmp_path)


def test_cc_file_lookup(ligand_dict):
    ccd_files = list(lookup_ccd_fs(ligand_dict))
    assert len(ccd_files) == 4
    
    for cc in ccd_files:
        assert cc.endswith('.cif')
        assert 'CVS' not in cc
        assert 'REMOVED' not in cc
        assert 'FULL' not in cc


def test_parse_cc_file():
    reader = ChemCompReader(config=Config())
    data = reader.read('./tests/fixtures/MIL.cif')

    assert '_chem_comp' in data
    assert '_chem_comp_atom' in data
    assert '_chem_comp_bond' in data
    assert '_pdbx_chem_comp_descriptor' in data
    assert '_pdbx_chem_comp_identifier' in data
    assert '_pdbx_chem_comp_audit' in data


@pytest.fixture
def db_engine():
    engine = create_engine("sqlite+pysqlite:///compv4.sqlite", echo=True)
    yield engine
    engine.dispose()


@pytest.mark.integration
def test_schema_creation(db_engine, tmp_path):
    config = Config()
    loader = DataLoader(config=config, engine=db_engine, ccd_root=tmp_path)
    loader.load()

    with db_engine.connect():
        meta = MetaData()
        meta.reflect(bind=db_engine)

        for table in config.chem_comp_categories:
            assert table.lstrip("_") in meta.tables


@pytest.mark.integration
def test_schema_recreation(db_engine, tmp_path):
    config = Config()
    loader = DataLoader(config=config, engine=db_engine, ccd_root=tmp_path)
    loader.load()
    loader.load()


@pytest.mark.integration
def test_data_load(ligand_dict, db_engine):
    loader = DataLoader(config=Config(), engine=db_engine, ccd_root=ligand_dict)
    loader.load()

    with db_engine.connect() as conn:
        stmt = select(chem_comp.c.id)
        result = list(conn.execute(stmt))
        codes = list(map(lambda x: x[0], result))
        
        assert len(codes) == 4
        assert '001' in codes
        assert 'ABC' in codes
        assert 'MIL' in codes
        assert 'TON' in codes
