import os
import pytest
import shutil

from ccd_maintenance.config import Config
from ccd_maintenance.data_loader import lookup_ccd_fs, ChemCompReader


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
        with open(file_path, 'w') as f:
            f.write('Mock content')

    # Print the temporary directory path
    print(f"Mock CCD directory structure created in: {tmp_path}")
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
