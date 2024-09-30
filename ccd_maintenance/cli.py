import os
import re
import time
import click
import logging

from ccd_maintenance.config import Config
from ccd_maintenance.data_loader import DataLoader

from sqlalchemy import create_engine
from wwpdb.utils.config.ConfigInfo import ConfigInfo
from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppCc

logging.basicConfig(level=logging.INFO)


def get_site_config_db_url():
    config = ConfigInfo()
    dbname = config.get("SITE_REFDATA_CC_DB_NAME")
    host = config.get("SITE_REFDATA_DB_HOST_NAME")
    port = config.get("SITE_REFDATA_DB_PORT_NUMBER")
    user = config.get("SITE_REFDATA_DB_USER_NAME")
    password = config.get("SITE_REFDATA_DB_PASSWORD")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"


def get_ccd_root():
    config = ConfigInfo()
    cc_config = ConfigInfoAppCc()
    components_root = cc_config.get_site_refdata_top_cvs_sb_path()
    ligand_proj = config.get("SITE_REFDATA_PROJ_NAME_CC")

    return os.path.join(components_root, ligand_proj)


@click.group()
def cli():
    pass


@click.command()
@click.option("--db-url", default=None, help="Database URL")
@click.option("--ccd-root", default=None, help="CCD root directory")
@click.option("--production", flag_value=True, help="Use production database")
@click.option("--verbose", flag_value=True, help="Verbose output")
def load(db_url, ccd_root, production, verbose):
    """Load data into the database."""
    if not db_url and not production:
        raise click.UsageError("Please provide a database URL or use the --production flag")

    if verbose:
        logging.basicConfig(logging.DEBUG)
        logging.getLogger("ccd_maintenance.data_loader").setLevel(logging.DEBUG)

    if not db_url:
        click.echo("Using production database")
        db_url = get_site_config_db_url()

    if not ccd_root:
        click.echo("Using default CCD root directory")
        ccd_root = get_ccd_root()

    click.echo(f"Loading CCD data from {ccd_root} into {re.sub(r':.*@', ':****@', db_url)}")

    config = Config()
    engine = create_engine(db_url)
    loader = DataLoader(config=config, engine=engine, ccd_root=ccd_root)
    start = time.time()
    loader.load()
    end = time.time()
    click.echo(f"Data loaded in {end - start:.2f} seconds")


cli.add_command(load)

if __name__ == '__main__':
    cli()
