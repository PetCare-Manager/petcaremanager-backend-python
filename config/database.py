"""
Creation of session for database connection
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.realpath(__file__))
database_url = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(base_dir, '../test.db')}")

engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
