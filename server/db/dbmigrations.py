from db import Base,engine
from db import User,NormalUser
Base.metadata.create_all(engine)
print("Migration successful")