# models.py
from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # ✅ CORRECT
print("Loaded DB URL in models.py:", DATABASE_URL)


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
