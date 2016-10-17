import os
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = "dsjfjdslf"
SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:password@localhost/pyt" # Sql Alchemy to automate database management
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "dbrepo")
# User Management. Stormpath. Have to create an application and set it up before running the server.
STORMPATH_API_KEY_FILE = os.path.expanduser('~/.stormpath/apiKey.properties') # Path to the api key properties
STORMPATH_APPLICATION = 'Pyt' # Name of the stormpath application
