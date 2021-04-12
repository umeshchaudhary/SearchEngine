import logging
import aiohttp
import config as env_variables

from constants import GCS_API_URL


class GoogleAPIManager:

  def __init__(self, api_key: str, search_engine_id: str) -> None:
    self._api_key = api_key
    self.search_engine_id = search_engine_id
    self.search_api_url = f'{GCS_API_URL}?' \
                          f'key={self._api_key}&cx={search_engine_id}' \
                          f'&num={env_variables.GCS_NUM_RESULTS}'\
                          f'&googlehost=google.com&hl=en&as_qdr=all'

  @staticmethod
  async def add_query_text(api_url, keywords: str):
    return api_url + f'&q={keywords}'

  async def return_google_search_results(self, keywords: str) -> list:

    # get new url object to add custom query attributes
    api_url: str = self.search_api_url

    # add query param for ex: &q=nodejs
    api_url = await self.add_query_text(api_url, keywords)

    async with aiohttp.ClientSession() as session:
      try:
        async with session.get(api_url) as response:
          resp = await response.json()
      except Exception as ex:
        logging.error(ex.args)
        raise ex
      else:
        urls = []
        for result in resp.get('items', []):
          urls.append(result['link'])
    return urls


googleAPIManager = GoogleAPIManager(
  env_variables.GCS_API_KEY,
  env_variables.GSE_ID
)
