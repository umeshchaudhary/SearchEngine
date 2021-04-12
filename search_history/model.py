from sqlalchemy import Column, Integer, String

from database_manager import Base
from constants import SEARCH_HISTORY_TABLE_NAME


class SearchHistory(Base):
  __tablename__ = SEARCH_HISTORY_TABLE_NAME

  id = Column(Integer, primary_key=True)
  keywords = Column(String(255), nullable=False)
  created_at = Column(Integer, nullable=False)
