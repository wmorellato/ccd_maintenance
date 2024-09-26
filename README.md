# CCD Maintenance CLI

This CLI tool is designed to load the CCD from a given root directory into a specified database.

## Command Usage

```bash
ccd-tasks load [OPTIONS]
```

## Options

- **`--db_url`**: The URL of the database where the CCD data will be loaded.`
- **`--ccd_root`**: The root directory where the CCD files are stored. The tool will read CCD files from this directory and load them into the database. 
- **`--production`**: Flag to indicate whether the production database should be used. If this flag is set, the application will load data into the production environment.

## Example

```bash
ccd-tasks load --db_url "mysql+mysqlconnector://user:password@localhost/my_database" --ccd_root "/data/ccd"
```

This command loads CCD data from the `/data/ccd` directory into the local MySQL database at `localhost`. The connector used for the production database is `pymysql`.
