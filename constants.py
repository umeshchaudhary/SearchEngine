import logging

LOG_LEVELS = {
  'INFO': logging.INFO,
  'DEBUG': logging.DEBUG,
  'WARNING': logging.WARNING,
  'ERROR': logging.ERROR,
  'CRITICAL': logging.CRITICAL
}


GCS_API_URL = 'https://customsearch.googleapis.com/customsearch/v1'

SEARCH_HISTORY_TABLE_NAME = 'searchhistory'
INPUT_TOO_LONG = 'Too long input to search for. Please try some actual words to query.'
NO_RESULTS = 'Nothing found'
INVALID_INPUT = 'Can not help you with that. Please try available options below.'
INTERNAL_SERVER_ERROR = 'Unable to serve you for now. Please try again later.'
