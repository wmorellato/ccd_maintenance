class Config:
    def __init__(self):
        self.chem_comp_categories = [
            "_chem_comp",
            "_chem_comp_angle",
            "_chem_comp_atom",
            "_chem_comp_bond",
            "_chem_comp_chir",
            "_chem_comp_chir_atom",
            "_chem_comp_link",
            "_chem_comp_plane",
            "_chem_comp_plane_atom",
            "_chem_comp_tor",
            "_chem_comp_tor_value",
            "_pdbx_chem_comp_synonyms",
            "_pdbx_chem_comp_feature",
            "_pdbx_chem_comp_descriptor",
            "_pdbx_chem_comp_identifier",
            "_pdbx_chem_comp_import",
            "_pdbx_chem_comp_atom_edit",
            "_pdbx_chem_comp_bond_edit",
            "_pdbx_chem_comp_audit",
            "_pdbx_chem_comp_pcm",
            "_pdbx_chem_comp_related",
            "_pdbx_chem_comp_atom_related",
        ]
        self.num_threads = 4
