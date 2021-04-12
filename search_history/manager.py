import datetime as dt_lib
import logging

from sqlalchemy import orm
from sqlalchemy import text
from sqlalchemy import exc
from sqlalchemy.engine import CursorResult

from database_manager import DBManager

from .model import SearchHistory


class SearchHistoryManager:
  """A configurable :class:`.SearchHistoryManager`

  The object of this class will handle all operations related to SearchHistory model.
  """

  @classmethod
  def new_session(cls) -> orm.session.Session:
    """
    Get a new database session
    """
    return DBManager.session()

  @classmethod
  async def save_search_keywords(cls, keywords: str) -> bool:
    """
    Save the search string into database as keywords
    :param keywords: search string used to search content on google
    """
    try:
      async with cls.new_session() as session:
        async with session.begin():
          obj = SearchHistory()
          obj.keywords = keywords
          obj.created_at = int(dt_lib.datetime.utcnow().timestamp())
          session.add(obj)
    except exc.SQLAlchemyError as ex:
      logging.error(ex.args)
      return False
    return True

  @classmethod
  async def get_search_history_by_keywords(cls, keywords: str):
    async with cls.new_session() as session:
      async with session.begin():
        resp: CursorResult = await session.execute(
          text(f"SELECT keywords from searchhistory where keywords ilike '%{keywords}%' ORDER BY created_at DESC")
        )
        results: str = '====================================\n'
        for obj in resp.fetchmany(size=200):
          results += obj[0] + '\n'
          if len(results) > 2000:
            yield results + '...\n'
            results = ''
        yield results


searchHistoryManager = SearchHistoryManager()
