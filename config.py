import os

from dotenv import load_dotenv
load_dotenv()
from constants import LOG_LEVELS


# Google customer search API key
GCS_API_KEY = os.getenv('GCS_API_KEY', '')

# Google programmable search engine id
GSE_ID = os.getenv('GSE_ID', '')

# number of results to return in google search
GCS_NUM_RESULTS = str(os.getenv('GCS_NUM_RESULTS', '5'))

# Discord bot secret
BOT_SECRET = os.getenv('BOT_SECRET', '')

DB_URL = os.getenv('DB_URL', '')

LOG_LEVEL = LOG_LEVELS.get(os.getenv('LOG_LEVEL', "ERROR"))
