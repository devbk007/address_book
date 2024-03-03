from sqlalchemy import Column, Integer, String, Float

from database import Base

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_line = Column(String, unique=True, index=True)
    second_line = Column(String)
    phone = Column(String)
    pincode = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
