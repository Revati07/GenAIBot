from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    message = Column(String)

# Define your database connection here
engine = create_engine('sqlite:///conversations.db')

Base.metadata.create_all(engine)
