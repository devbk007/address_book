from pydantic import BaseModel

class AddressBase(BaseModel):
    first_line: str
    second_line:str
    phone:str
    pincode:str
    latitude:float
    longitude:float
class Address(AddressBase):
    id: int
    class Config:
        from_attributes = True