from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import Connection_CONFIG
from sqlalchemy import Column, Sequence
from sqlalchemy.types import Integer, String, BLOB
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

engine = create_engine(Connection_CONFIG, encoding='utf-8', echo=True)
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = "user_information"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20))
    password = Column(String(20))
    email_address = Column(String(80))

    balance = Column(Integer, default=0)
    profit = Column(Integer, default=0)

    team_performance = Column(Integer, default=0)
    leader_id = Column(Integer)
    rank = Column(Integer)

    def __repr__(self):
        return '<User %r>' % self.id


class Artwork(Base):
    __tablename__ = "Artwork"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    artist = Column(String(20), nullable=True)
    details = Column(String(1000), nullable=True)
    price = Column(Integer, nullable=True)
    image = Column(String(10000), nullable=True)


class Investment(Base):
    __tablename__ = "Investment"

    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(String(20))
    user_address = Column(String(20))
    artwork_id = Column(Integer)
    asset = Column(Integer)


class DealRecords(Base):
    __tablename__ = "Deal"

    id = Column(Integer, Sequence('id'), primary_key=True)
    user_id = Column(String(20))
    user_address = Column(String(100))
    deposit = Column(Integer)
    withdraw = Column(Integer)
    confirmed = Column(Integer)


class Admin(Base):
    __tablename__ = "Admin"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(20))
    password = Column(String(20))


class Email_code(Base):
    __tablename__ = "email_code"

    id = Column(Integer, primary_key=True)
    email_address = Column(String(20))
    email_code = Column(String(20))


Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)
db_session = Session()
