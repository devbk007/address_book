import logging

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.address.dependencies import get_db
from src.address import schemas,crud
from typing import List

router = APIRouter(
    prefix="/address",
    tags=["Address"],
    responses={
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"},
    },
)

logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.Address, description="Create unique address")
def create_address(address: schemas.AddressBase, db:Session = Depends(get_db)):
    try:
        db_address = crud.get_address_by_first_line(db=db, first_line=address.first_line)
        if db_address:
            logger.warning("Address already exist.")
            raise HTTPException(status_code=400, detail="Address already exist")
        else:
            return crud.create_address(db=db, address=address)
    except HTTPException as http_exception:
        raise http_exception
    except IntegrityError as e:
        logger.error("Database integrity error: %s", e)
        raise HTTPException(status_code=500, detail="Database integrity error")
    except Exception as e:
        logger.error("Internal server error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[schemas.Address], description="Read list of addresses")
def get_address_list(db:Session = Depends(get_db)):
    try:
        address = crud.get_address(db)
        if address is None:
            logger.warning("No address found")
            raise HTTPException(status_code=400, detail="No address found")
        else:
            return address
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error("Internal server error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{address_id}", response_model=schemas.Address,description="Read single address using ID")
def get_address(address_id:int, db:Session = Depends(get_db)):
    try:
        db_address = crud.get_address_by_id(db=db, id=address_id)
        if db_address is None:
            logger.warning("Address with ID %s not found.", address_id)
            raise HTTPException(status_code=404, detail="No address found")
        else:
            return db_address
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error("Internal server error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.put("/{address_id}", response_model=schemas.Address,description="Update existing address using ID")
def update_address(address:schemas.AddressBase, address_id:int, db:Session = Depends(get_db)):
    try:
        db_address = crud.update_address(db=db, id=address_id, address=address)
        if db_address is None:
            logger.warning("Address with ID %s not found.", address_id)
            raise HTTPException(status_code=404, detail="No addresses found")
        else:
            return db_address
    except IntegrityError as e:
        logger.error("Database integrity error: %s", e)
        raise HTTPException(status_code=500, detail="Database integrity error")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error("Internal server error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.delete("/{address_id}", description="Delete existing address using ID")
def delete_address(address_id:int, db:Session=Depends(get_db)):
    try:
        success, error_message = crud.delete_address(db=db, id=address_id)
        if success:
            logger.info("Address with ID %s deleted.", address_id)
            return status.HTTP_204_NO_CONTENT
        elif error_message:
            logger.warning("Failed to delete address with ID %s : %s.", address_id, error_message)
            raise HTTPException(status_code=400, detail=error_message)
        else:
            logger.warning("Address with ID %s not found.", address_id)
            raise HTTPException(status_code=404, detail="No addresses found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error("Internal server error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/coordinates/", response_model=List[schemas.Address], summary="Get nearest address", description="Retrieve the addresses that are within a given distance and location coordinates")
def get_addresses(distance:float, latitude:float, longitude:float, db:Session = Depends(get_db)):
    try:
        addresses = crud.find_address(db=db, distance=distance, latitude=latitude, longitude=longitude)
        return addresses
    except Exception as e:
        logger.error("Internal server error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")