# Import configparser to get all the variables from the config file
import configparser
import os

# Get the path to the config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "configs.ini"))

# Get the secret key for the application
SECRET_KEY = config.get("Flask", "secret_key")

# Get the path to the domains
LOCAL_DOMAIN_NAME = config["Domains"]["local"]
CDR_DOMAIN_NAME = config["Domains"]["cdr"]
CLOUD_DOMAIN_NAME = config["Domains"]["cloud"]

# SQL Server Databases
VIRALLOADDATA_DATABASE = config.get("Databases", "ViralLoadData")
VIRALLOADSMS_DATABASE = config.get("Databases", "ViralLoadSMS")
DPI_DATABASE_DATABASE = config.get("Databases", "Dpi")
HIVAD_DATABASE = config.get("Databases", "HivAdvancedDisease")
TBDATA_DATABASE_DATABASE = config.get("Databases", "TBData")
DICT_DATABASE_DATABASE = config.get("Databases", "Dictionary")
USER_DATABASE = config.get("Databases", "Users")

# SQL Server Databases Credentials
USERNAME = config.get("Databases", "database_user")
PASSWORD = config.get("Databases", "database_password")

# SQL Server Databases Schemas
CDR_DOMAIN_NAME_SCHEMA = config.get("Schemas", "cdr_schema")


def make_url(user, pwd, host, db):
    """Constructs a SQLAlchemy connection string."""
    return (
        f"mssql+pyodbc://{user}:{pwd}@{host}/{db}?driver=ODBC+Driver+17+for+SQL+Server"
    )


# Define SQLALCHEMY_BINDS to map databases to their respective connection strings
SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ = {
    "vlSMS": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, VIRALLOADSMS_DATABASE),
    "vl": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, VIRALLOADDATA_DATABASE),
    "dpi": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, DPI_DATABASE_DATABASE),
    "ad": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, HIVAD_DATABASE),
    "tb": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, TBDATA_DATABASE_DATABASE),
    "dict": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, DICT_DATABASE_DATABASE),
    "users": make_url(USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, USER_DATABASE),
}

SQLALCHEMY_BINDS_CDR_OPENLDR_ORG_MZ = {
    "vl": make_url(USERNAME, PASSWORD, CDR_DOMAIN_NAME, VIRALLOADDATA_DATABASE),
    "dpi": make_url(USERNAME, PASSWORD, CDR_DOMAIN_NAME, DPI_DATABASE_DATABASE),
    "ad": make_url(USERNAME, PASSWORD, CDR_DOMAIN_NAME, HIVAD_DATABASE),
    "tb": make_url(USERNAME, PASSWORD, CDR_DOMAIN_NAME, TBDATA_DATABASE_DATABASE),
    "dict": make_url(USERNAME, PASSWORD, CDR_DOMAIN_NAME, DICT_DATABASE_DATABASE),
    "users": make_url(USERNAME, PASSWORD, CDR_DOMAIN_NAME, USER_DATABASE),
}

SQLALCHEMY_BINDS_CLOUD_QUEUE_OPENLDR_ORG_MZ = {
    "vl": make_url(USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, VIRALLOADDATA_DATABASE),
    "dpi": make_url(USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, DPI_DATABASE_DATABASE),
    "ad": make_url(USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, HIVAD_DATABASE),
    "tb": make_url(USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, TBDATA_DATABASE_DATABASE),
    "dict": make_url(USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, DICT_DATABASE_DATABASE),
    "users": make_url(USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, USER_DATABASE),
}
