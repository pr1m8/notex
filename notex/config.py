import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Detect if Sphinx is running
IS_SPHINX = os.getenv("SPHINX_BUILD") == "1"

# Use dummy values if building Sphinx docs
if IS_SPHINX:
    print("⚠️ Running in Sphinx mode, using dummy API keys.")
    AZURE_OPENAI_API_KEY = "DUMMY_KEY"
    AZURE_URI = "https://dummy-url.com"
    AZURE_OPENAI_API_KEY_CANADA = "DUMMY_KEY"
    AZURE_URI_CANADA = "https://dummy-url-canada.com"
else:
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_URI = os.getenv("AZURE_URI")
    AZURE_OPENAI_API_KEY_CANADA = os.getenv("AZURE_OPENAI_API_KEY_CANADA")
    AZURE_URI_CANADA = os.getenv("AZURE_URI_CANADA")

    if not AZURE_OPENAI_API_KEY:
        raise ValueError("Missing Azure OpenAI credentials! Check .env file.")

# Lazy-load OpenAI clients
def get_openai_clients():
    if IS_SPHINX:
        return None, None
    from openai import AzureOpenAI, AsyncAzureOpenAI

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_URI, api_version="2024-02-01"
    )
    a_client = AsyncAzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_URI, api_version="2024-02-01"
    )
    return client, a_client

# Avoid initializing client during Sphinx builds
if not IS_SPHINX:
    client, a_client = get_openai_clients()
else:
    client, a_client = None, None
