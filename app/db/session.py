# DEFINES DB ENGINE AND BASE MODEL USING SQLALCHEMY
# using sqlalchemy to use 'pythonic' syntax for database (sqlite) interaction
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# file-based db (data persists)
DB_URL = 'sqlite:///didiAIDB.db'
# sqlite is single thread, fastapi is async, 
# to avoid thread lock error use check_same_thread: False
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# create base class which models will inherit from
Base = declarative_base()