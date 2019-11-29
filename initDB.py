from config import getBase, getEngine
from dataModels import User, Tweet

base = getBase()
engine = getEngine()

base.metadata.create_all(engine)