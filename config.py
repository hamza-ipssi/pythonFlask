from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from settings import CONST_BD

def getBase():
    base = declarative_base()
    return base

def getEngine():
    engine = create_engine(CONST_BD)
    return engine