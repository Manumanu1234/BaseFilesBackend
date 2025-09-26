from .dbengine import Base, engine
from .dbschema import User
Base.metadata.create_all(engine)
print("Migration successful")