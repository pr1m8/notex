import os
import configparser
import firebase_admin
from firebase_admin import credentials, firestore

# Determine the absolute path to the config file
config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read(config_file_path)

# Get the relative path from the configuration
key_path = config['firebase']['key_path']

# Resolve the absolute path to the key file
absolute_key_path = os.path.join(os.path.dirname(__file__), '..', key_path)

# Initialize Firebase app
cred = credentials.Certificate(absolute_key_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
