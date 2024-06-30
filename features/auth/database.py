import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://"+os.getenv('POSTGRES_USER', 'root')+":"+os.getenv('POSTGRES_PASSWORD', '')+"@"+os.getenv('POSTGRES_HOST', 'localhost')+"/"+os.getenv('POSTGRES_DB', 'defaultdb')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
"""
Create a new instance of the engine.

The engine is the starting point for any SQLAlchemy application.
It's “home base” for the actual database and its DBAPI, delivered to the SQLAlchemy application
through a connection pool and a Dialect, which describes how to talk to a specific kind of database/DBAPI combination.
"""


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Create a configured "Session" class.

The sessionmaker factory generates new Session objects when called, creating them given
the configurational arguments established here.
"""

Base = declarative_base()
"""
Create a base class for declarative class definitions.

The new base class will be given a metaclass that produces appropriate Table objects and makes
the appropriate mapper() calls based on the information provided declaratively in the class and any subclasses of the class.
"""