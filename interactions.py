from typing import AsyncGenerator
# noinspection PyPackageRequirements
import discord
import constants

from services.googleApi import googleAPIManager
from search_history.manager import searchHistoryManager


async def google_search(user_input: str, channel: discord.TextChannel) -> bool:
  """
  Returns top 5 search results based on the user input
  :param user_input: text to search
  :param channel: message channel to send the response
  """

  search_keywords: str = user_input.strip()
  if len(search_keywords) > 255:  # It is the max limit to store the data in database column
    await channel.send(constants.INPUT_TOO_LONG)
    return True
  urls: list = await googleAPIManager.return_google_search_results(
      search_keywords
  )
  if not urls:
    await channel.send('Nothing found.')
    return True

  for url in urls:
    await channel.send(url)

  result: bool = await searchHistoryManager.save_search_keywords(search_keywords)
  return result


async def recent_search_history(user_input: str, channel: discord.TextChannel) -> bool:
  """
  Search the given text into database and return all the matched results
  :param user_input: input text to search into the database
  :param channel: channel to send the response
  :return:
  """
  if len(user_input) > 255:  # It is the max limit to store the data in database column
    await channel.send(constants.INPUT_TOO_LONG)
    return True
  search_history: [AsyncGenerator[str], bool] = searchHistoryManager.get_search_history_by_keywords(user_input)

  # If `False` is returned as the response then probably something went wrong with the database.
  if not search_history:
    return False

  results = False
  # Iterate over the cursor and send objects one by one
  # await channel.send('\n'.join([o[0] for o in search_history]))
  async for history in search_history:
    if history.endswith('=\n'):
      results = False
      continue
    await channel.send(history)
    if not results:
      results = True
  if not results:
    await channel.send(constants.NO_RESULTS)
    return True
  await channel.send('====================================\n')
  return True

interactions = {
  'hi': 'hey',
  '!google': google_search,
  '!recent': recent_search_history,
}
