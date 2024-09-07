import configparser
from openai import OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI

# Adjust this import according to your project structure
#from . import package_root

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Fetch the API keys and endpoints from the configuration file
AZURE_OPENAI_API_KEY = config["AZURE_OPENAI"]["API_KEY"]
AZURE_URI = config["AZURE_OPENAI"]["URI"]

AZURE_OPENAI_API_KEY_CANADA = config["AZURE_OPENAI"]["API_KEY_CANADA"]
AZURE_URI_CANADA = config["AZURE_OPENAI"]["URI_CANADA"]

# Initialize Azure OpenAI clients
client = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_URI, api_version="2024-02-01")
a_client = AsyncAzureOpenAI(api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_URI, api_version="2024-02-01")

client_canada = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY_CANADA, azure_endpoint=AZURE_URI_CANADA, api_version="2024-02-01")
a_client_canada = AsyncAzureOpenAI(api_key=AZURE_OPENAI_API_KEY_CANADA, azure_endpoint=AZURE_URI_CANADA, api_version="2024-02-01")

