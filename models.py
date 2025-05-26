from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_number = Column(String)
    bread = Column(String)
    filling = Column(String)

engine = create_engine('sqlite:///sandwich.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
