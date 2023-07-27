from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, URL, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import URLType


Base = declarative_base()


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    original_url = Column(URLType, unique=True, nullable=False)
    short_url = Column(String(length=6), nullable=False)
    clicks_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        default=datetime.utcnow)



