import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index,VARCHAR,JSON
# coding: utf-8
Base = declarative_base()
metadata = Base.metadata

class HotList(Base):
    __tablename__ = 'hotList'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    word = Column(VARCHAR(255))
    index = Column(Integer)
    type = Column(String(255))
    desc = Column(String(255))
    hotchange = Column(String(255))
    hotscore = Column(Integer)
    img = Column(String(255))
    query = Column(String(255))
    rawurl = Column(String(255))
    show = Column(JSON)


class TopList(Base):
    __tablename__ = 'topList'

    time = Column(DateTime, primary_key=True)
    type = Column(String(255))
    desc = Column(String(255))
    hotchange = Column(String(255))
    hotscore = Column(Integer)
    img = Column(String(255))
    query = Column(String(255))
    rawurl = Column(String(255))
    show = Column(String(255))
    word = Column(String(255))

