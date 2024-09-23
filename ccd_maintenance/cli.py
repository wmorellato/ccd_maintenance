import click

from wwpdb.utils.config.ConfigInfo import ConfigInfo
from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppCc


def get_site_config_db_url():
    config = ConfigInfo()
    # dbname = config.get("SITE_REFDATA_CC_DB_NAME")
    dbname = "compv4_test"
    host = config.get("SITE_REFDATA_DB_HOST_NAME")
    port = config.get("SITE_REFDATA_DB_PORT_NUMBER")
    socket = config.get("SITE_REFDATA_DB_SOCKET")
    user = config.get("SITE_REFDATA_DB_USER_NAME")
    password = config.get("SITE_REFDATA_DB_PASSWORD")

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"


def get_ccd_root():
    cc_config = ConfigInfoAppCc()
    return cc_config.get_site_refdata_top_cvs_sb_path()


@click.group()
def cli():
    pass


@click.command()
@click.option('--db_url', default=None, help='Database URL')
@click.option('--ccd_root', default=None, help='CCD root directory')
def load(db_url, ccd_root):
    """Load data into the database."""
    if not db_url:
        db_url = get_site_config_db_url()

    if not ccd_root:
        ccd_root = ConfigInfo().get("SITE_REFDATA_CCDCOMPONENT_DIR")

    click.echo(f"Loading data with db_url: {db_url} and ccd_root: {ccd_root}")

cli.add_command(load)

if __name__ == '__main__':
    cli()