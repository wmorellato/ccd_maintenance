from datetime import datetime, date

from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, DateTime, Boolean


metadata_obj = MetaData()
Column("Component_ID", String(10), primary_key=True),


chem_comp = Table("chem_comp",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("formula", String(255), nullable=True),
    Column("formula_weight", Float, nullable=True),
    Column("id", String(10), primary_key=True),
    Column("model_details", String(255), nullable=True),
    Column("model_erf", String(128), nullable=True),
    Column("model_source", String(255), nullable=True),
    Column("mon_nstd_class", String(255), nullable=True),
    Column("mon_nstd_details", String(255), nullable=True),
    Column("mon_nstd_flag", String(10), nullable=True, default="'no'"),
    Column("mon_nstd_parent", String(20), nullable=True),
    Column("mon_nstd_parent_comp_id", String(50), nullable=True),
    Column("name", String(255), nullable=True),
    Column("number_atoms_all", Integer, nullable=True),
    Column("number_atoms_nh", Integer, nullable=True),
    Column("one_letter_code", String(10), nullable=True),
    Column("three_letter_code", String(6), nullable=True),
    Column("type", String(50)),
    Column("pdbx_synonyms", String(255), nullable=True),
    Column("pdbx_modification_details", String(255), nullable=True),
    Column("pdbx_component_no", Integer, nullable=True),
    Column("pdbx_type", String(50), nullable=True),
    Column("pdbx_ambiguous_flag", String(20), nullable=True),
    Column("pdbx_replaced_by", String(10), nullable=True),
    Column("pdbx_replaces", String(50), nullable=True),
    Column("pdbx_formal_charge", Integer, nullable=True, default="'0'"),
    Column("pdbx_subcomponent_list", String(255), nullable=True),
    Column("pdbx_model_coordinates_details", String(255), nullable=True),
    Column("pdbx_model_coordinates_db_code", String(128), nullable=True),
    Column("pdbx_ideal_coordinates_details", String(255), nullable=True),
    Column("pdbx_ideal_coordinates_missing_flag", String(10), nullable=True, default="'N'"),
    Column("pdbx_model_coordinates_missing_flag", String(10), nullable=True, default="'N'"),
    Column("pdbx_initial_date", DateTime, nullable=True),
    Column("pdbx_modified_date", DateTime, nullable=True),
    Column("pdbx_release_status", String(128), nullable=True),
    Column("pdbx_processing_site", String(20), nullable=True),
    Column("pdbx_pcm", String(20), nullable=True)
)


chem_comp_angle = Table("chem_comp_angle",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("atom_id_1", String(6), primary_key=True),
    Column("atom_id_2", String(6), primary_key=True),
    Column("atom_id_3", String(6), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("value_angle", Float, nullable=True),
    Column("value_angle_esd", Float, nullable=True),
    Column("value_dist", Float, nullable=True),
    Column("value_dist_esd", Float, nullable=True)
)


chem_comp_atom = Table("chem_comp_atom",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("alt_atom_id", String(128), nullable=True),
    Column("atom_id", String(6), primary_key=True),
    Column("charge", Integer, nullable=True, default="'0'"),
    Column("model_Cartn_x", Float, nullable=True),
    Column("model_Cartn_x_esd", Float, nullable=True),
    Column("model_Cartn_y", Float, nullable=True),
    Column("model_Cartn_y_esd", Float, nullable=True),
    Column("model_Cartn_z", Float, nullable=True),
    Column("model_Cartn_z_esd", Float, nullable=True),
    Column("comp_id", String(10), primary_key=True),
    Column("partial_charge", Float, nullable=True),
    Column("substruct_code", String(10), nullable=True),
    Column("type_symbol", String(20)),
    Column("pdbx_align", Integer, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_alt_atom_id", String(6), nullable=True),
    Column("pdbx_alt_comp_id", String(10), nullable=True),
    Column("pdbx_model_Cartn_x_ideal", Float, nullable=True),
    Column("pdbx_model_Cartn_y_ideal", Float, nullable=True),
    Column("pdbx_model_Cartn_z_ideal", Float, nullable=True),
    Column("pdbx_stereo_config", String(10), nullable=True),
    Column("pdbx_aromatic_flag", String(10), nullable=True),
    Column("pdbx_leaving_atom_flag", String(10), nullable=True),
    Column("pdbx_stnd_atom_id", String(128), nullable=True),
    Column("pdbx_backbone_atom_flag", String(10), nullable=True),
    Column("pdbx_n_terminal_atom_flag", String(10), nullable=True),
    Column("pdbx_c_terminal_atom_flag", String(10), nullable=True)
)


chem_comp_bond = Table("chem_comp_bond",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("atom_id_1", String(6), primary_key=True),
    Column("atom_id_2", String(6), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("value_order", String(10), nullable=True, default="'sing'"),
    Column("value_dist", Float, nullable=True),
    Column("value_dist_esd", Float, nullable=True),
    Column("pdbx_ordinal", Integer, nullable=True),
    Column("pdbx_stereo_config", String(10), nullable=True),
    Column("pdbx_aromatic_flag", String(10), nullable=True)
)


chem_comp_chir = Table("chem_comp_chir",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("atom_id", String(6)),
    Column("atom_config", String(10), nullable=True),
    Column("id", String(20), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("number_atoms_all", Integer, nullable=True),
    Column("number_atoms_nh", Integer, nullable=True),
    Column("volume_flag", String(10), nullable=True),
    Column("volume_three", Float, nullable=True),
    Column("volume_three_esd", Float, nullable=True)
)


chem_comp_chir_atom = Table("chem_comp_chir_atom",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("atom_id", String(6), primary_key=True),
    Column("chir_id", String(20), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("dev", Float, nullable=True)
)


chem_comp_link = Table("chem_comp_link",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("link_id", String(20), primary_key=True),
    Column("details", String(255), nullable=True),
    Column("type_comp_1", String(50)),
    Column("type_comp_2", String(50))
)


chem_comp_plane = Table("chem_comp_plane",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("id", String(20), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("number_atoms_all", Integer, nullable=True),
    Column("number_atoms_nh", Integer, nullable=True)
)


chem_comp_plane_atom = Table("chem_comp_plane_atom",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("atom_id", String(6), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("plane_id", String(20), primary_key=True),
    Column("dist_esd", Float, nullable=True)
)


chem_comp_tor = Table("chem_comp_tor",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("atom_id_1", String(6)),
    Column("atom_id_2", String(6)),
    Column("atom_id_3", String(6)),
    Column("atom_id_4", String(6)),
    Column("id", String(20), primary_key=True),
    Column("comp_id", String(10), primary_key=True)
)


chem_comp_tor_value = Table("chem_comp_tor_value",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("tor_id", String(20), primary_key=True),
    Column("angle", Float),
    Column("angle_esd", Float),
    Column("dist", Float, nullable=True),
    Column("dist_esd", Float, nullable=True)
)


pdbx_chem_comp_atom_edit = Table("pdbx_chem_comp_atom_edit",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("ordinal", Integer, primary_key=True),
    Column("comp_id", String(10)),
    Column("edit_op", String(10)),
    Column("atom_id", String(6)),
    Column("edit_atom_id", String(6)),
    Column("edit_atom_value", String(128), nullable=True)
)


pdbx_chem_comp_atom_related = Table("pdbx_chem_comp_atom_related",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("related_comp_id", String(10), primary_key=True),
    Column("ordinal", Integer, primary_key=True),
    Column("atom_id", String(6)),
    Column("related_atom_id", String(6), nullable=True),
    Column("related_type", String(128))
)


pdbx_chem_comp_audit = Table("pdbx_chem_comp_audit",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("date", DateTime, primary_key=True),
    Column("annotator", String(20), nullable=True),
    Column("action_type", String(128), primary_key=True)
)


pdbx_chem_comp_bond_edit = Table("pdbx_chem_comp_bond_edit",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("ordinal", Integer),
    Column("comp_id", String(10), primary_key=True),
    Column("edit_op", String(10), primary_key=True),
    Column("atom_id_1", String(6), primary_key=True),
    Column("atom_id_2", String(6), primary_key=True),
    Column("edit_bond_value", String(128), nullable=True)
)


pdbx_chem_comp_descriptor = Table("pdbx_chem_comp_descriptor",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("descriptor", String(2048)),
    Column("type", String(50), primary_key=True),
    Column("program", String(128), primary_key=True),
    Column("program_version", String(128), primary_key=True),
    Column("ordinal", Integer, nullable=True)
)


pdbx_chem_comp_feature = Table("pdbx_chem_comp_feature",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("type", String(128), primary_key=True),
    Column("support", String(255), nullable=True),
    Column("value", String(255), primary_key=True),
    Column("source", String(128), primary_key=True)
)


pdbx_chem_comp_identifier = Table("pdbx_chem_comp_identifier",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("identifier", String(255)),
    Column("type", String(128), primary_key=True),
    Column("program", String(128), primary_key=True),
    Column("program_version", String(128), primary_key=True),
    Column("ordinal", Integer, nullable=True)
)


pdbx_chem_comp_import = Table("pdbx_chem_comp_import",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True)
)


pdbx_chem_comp_related = Table("pdbx_chem_comp_related",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("comp_id", String(10), primary_key=True),
    Column("related_comp_id", String(10), primary_key=True),
    Column("relationship_type", String(128), primary_key=True),
    Column("details", String(255), nullable=True)
)


pdbx_chem_comp_synonyms = Table("pdbx_chem_comp_synonyms",
    metadata_obj,
    Column("Component_ID", String(10), primary_key=True),
    Column("ordinal", Integer, primary_key=True),
    Column("name", String(255)),
    Column("comp_id", String(10), primary_key=True),
    Column("provenance", String(128), nullable=True),
    Column("type", String(128), nullable=True)
)


def get_table(table_name):
    return metadata_obj.tables.get(table_name)
    Column("Component_ID", String(10), primary_key=True),


def cast_type(table_obj: Table, tag: str, value):
    if not isinstance(table_obj.c[tag].type, String) and value == "":
        return None

    if isinstance(table_obj.c[tag].type, Float):
        return float(value)

    if isinstance(table_obj.c[tag].type, Integer):
        return int(value)

    if isinstance(table_obj.c[tag].type, DateTime):
        return datetime.strptime(value, "%Y-%m-%d")

    if isinstance(table_obj.c[tag].type, Date):
        return date.fromisoformat(value)

    if isinstance(table_obj.c[tag].type, Boolean):
        return bool(value)

    return value
