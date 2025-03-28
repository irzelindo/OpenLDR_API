# Import configparser to get all the variables from the config file
import configparser
import os

# Get the path to the config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "configs.ini"))

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

# SQL Server Databases Credentials
USERNAME = config.get("Databases", "database_user")
PASSWORD = config.get("Databases", "database_password")

# SQL Server Databases Schemas
CDR_DOMAIN_NAME_SCHEMA = config.get("Schemas", "cdr_schema")

# Define SQLALCHEMY_BINDS to map databases to their respective connection strings
SQLALCHEMY_BINDS_APHL_OPENLDR_ORG_MZ = {
    "vlSMS": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, VIRALLOADSMS_DATABASE
    ),
    "vl": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, VIRALLOADDATA_DATABASE
    ),
    "dpi": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, DPI_DATABASE_DATABASE
    ),
    "ad": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, HIVAD_DATABASE
    ),
    "tb": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CDR_DOMAIN_NAME, TBDATA_DATABASE_DATABASE
    ),
    "dict": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, LOCAL_DOMAIN_NAME, DICT_DATABASE_DATABASE
    ),
}

SQLALCHEMY_BINDS_CDR_OPENLDR_ORG_MZ = {
    "vl": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CDR_DOMAIN_NAME, VIRALLOADDATA_DATABASE
    ),
    "dpi": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CDR_DOMAIN_NAME, DPI_DATABASE_DATABASE
    ),
    "ad": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CDR_DOMAIN_NAME, HIVAD_DATABASE
    ),
    "tb": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CDR_DOMAIN_NAME, TBDATA_DATABASE_DATABASE
    ),
    "dict": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CDR_DOMAIN_NAME, DICT_DATABASE_DATABASE
    ),
}

SQLALCHEMY_BINDS_CLOUD_QUEUE_OPENLDR_ORG_MZ = {
    "vl": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, VIRALLOADDATA_DATABASE
    ),
    "dpi": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, DPI_DATABASE_DATABASE
    ),
    "ad": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, HIVAD_DATABASE
    ),
    "tb": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, TBDATA_DATABASE_DATABASE
    ),
    "dict": "mssql+pyodbc://{}:{}@{}/{}?driver=ODBC+Driver+17+for+SQL+Server".format(
        USERNAME, PASSWORD, CLOUD_DOMAIN_NAME, DICT_DATABASE_DATABASE
    ),
}
