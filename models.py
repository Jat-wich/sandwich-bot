# models.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("postgres://sandwichbot_db_user:vQv9neKVNkQ3xaC2FfemcGamfrNLeIWs@dpg-d0qbslgdl3ps73equv3g-a/sandwichbot_db")

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_number = Column(String)
    bread = Column(String)
    filling = Column(String)

Base.metadata.create_all(engine)
