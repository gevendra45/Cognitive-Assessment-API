import os

# Path to LIWC dictionary file
LIWC_DICTIONARY_PATH = os.path.join(os.path.dirname(__file__), '../../liwc_dictionary.json')

# JWT Secret Key
JWT_SECRET_KEY = 'your_secret_key_here'

# Default database URI
SQLALCHEMY_DB_URI = 'sqlite:///liwc.db'
