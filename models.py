from sqlalchemy import Column, Integer, String
from database import Base

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(String, index=True)  # Yelp restaurant ID
    title = Column(String)
    description = Column(String)
    valid_until = Column(String)  # For simplicity, store date as string
