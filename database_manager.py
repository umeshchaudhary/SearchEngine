from typing import Union
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config as env_variables

"""
  Base class for all database models
    class User(Base):
      name = Column(String)
      email = Column(String)    
"""
Base = declarative_base()


class DBManager:
  r"""Construct a new :class:`.DBManager

  Create a new database client and a session object
  which will then be used for al database operations.
  Also perform initial setup for the database.

    manager = DBManager("postgresql://user:pass@localhost/db")

  Use `manager.session()` to create a new session for every database operation.

    async with manager.session() as session:
      async with session.begin():
        session.add(SearchHistory())

  NOTE: Only one instance of this class should be created for one application server instance.
  """

  def __init__(self, conn_str: str):
    """
    :param conn_str: The database connection url
    """
    self._conn_str = conn_str
    self._db_engine: Union[sa.engine.Engine, None] = None
    self.session: Union[sa.orm.session.sessionmaker, None] = None

  async def _create_db_client(self) -> None:
    """
    Create a database client and add it to the object to use further.
    """
    if self._db_engine:
      return None
    self._db_engine = create_async_engine(self._conn_str, echo=True)

  @property
  def client(self):
    """
    Return database engine object as db client. Just to make the naming more clear.
    :return: sqlalchemy.engine.Engine
    """
    return self._db_engine

  async def setup_db(self):
    """
    Perform database initial setup
    :return: None
    """
    await self._create_db_client()
    async with self._db_engine.begin() as conn:

      # Add al the models as tables into database
      await conn.run_sync(Base.metadata.create_all)

    # create a session object to use for database operations
    self.session = sessionmaker(
      self._db_engine, expire_on_commit=False, class_=AsyncSession
    )

  async def close(self):
    """
    Close all active sessions and connection with the database.
    :return: None
    """
    self.session.close_all()
    self._db_engine.dispose()


#  Override class name variable with its own object so that only one object
#  will be available for all the requests.
DBManager = DBManager(
    env_variables.DB_URL
)
