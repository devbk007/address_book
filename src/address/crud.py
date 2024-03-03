from sqlalchemy.orm import Session
from src.address import models,schemas
from src.address.utils import calculate_distance

def get_address_by_id(db:Session, id:int):
    """Get address using id

    Args:
        db (Session): DB
        id (int): ID of address

    Returns:
        schemas.Address: Address detail
    """
    return db.query(models.Address).get(id)

def get_address_by_first_line(db:Session, first_line:str):
    """Get address using first line
    Args:
        db (Session): DB
        first_line (str): First line of address

    Returns:
        schemas.Address: Address detail
    """
    return db.query(models.Address).filter(models.Address.first_line==first_line).first()

def get_address(db:Session):
    """Get all address in the database

    Args:
        db (Session): DB

    Returns:
        List[schemas.Address]: List of addresses
    """
    address = db.query(models.Address).all()
    if len(address) > 0:
        return address
    return None

def create_address(db:Session, address:schemas.AddressBase):
    """Create a new address

    Args:
        db (Session): DB
        address (schemas.AddressBase): Address details

    Returns:
        schemas.Address: Created address details
    """
    db_address = models.Address(
        first_line = address.first_line, second_line=address.second_line, phone=address.phone, 
        pincode=address.pincode, latitude = address.latitude, longitude=address.longitude
        )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db:Session, id:int):
    """Delete an address in the db

    Args:
        db (Session): DB
        id (int): ID of address to be deleted

    Returns:
        Bool, str: True/False and error message/None
    """
    db_address = db.query(models.Address).get(id)
    try:
        if db_address:
            db.delete(db_address)
            db.commit()
            return True, None
        return False, None
    except Exception as e:
        db.rollback()
        print(e)
        return False, f"Error : {e}"
    
def update_address(db:Session, id:int, address:schemas.AddressBase):
    """Update an existing address in the db

    Args:
        db (Session): DB
        id (int): id of address
        address (schemas.AddressBase): New address

    Returns:
        address(schemas.Address): Updated address
    """
    db_address = db.query(models.Address).get(id)
    if db_address:
        db_address.first_line = address.first_line
        db_address.second_line = address.second_line
        db_address.phone = address.phone
        db_address.pincode = address.pincode
        db_address.latitude = address.latitude
        db_address.longitude = address.longitude
        
        db.commit()
        db.refresh(db_address)
        return db_address
    return None

def find_address(db:Session, distance:float, latitude:float, longitude:float):
    """Find address that are within a given distance and location coordinates

    Args:
        db (Session): DB
        distance (float): Distance limit
        latitude (float): Latitude of location
        longitude (float): Longitude of location

    Returns:
        _type_: List of addresses
    """
    filtered_addresses = []
    address_list = db.query(models.Address).all()
    for address in address_list:
        lat = address.latitude
        lon = address.longitude
        if calculate_distance(lat, lon, latitude, longitude) >= distance:
            filtered_addresses.append(address)
    return filtered_addresses