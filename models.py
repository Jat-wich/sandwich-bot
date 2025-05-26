from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Replace this with your actual database URL (Render Postgres URL or SQLite for local testing)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///orders.db")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_number = Column(String)
    bread = Column(String)
    filling = Column(String)

# Create tables
Base.metadata.create_all(engine)
