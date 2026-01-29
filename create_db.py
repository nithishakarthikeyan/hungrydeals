from database import Base, engine
from models import Deal

Base.metadata.create_all(bind=engine)

print("Database created!")
