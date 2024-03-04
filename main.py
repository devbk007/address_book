from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.address import router
from src.address import models


models.Base.metadata.create_all(bind=engine)

description = """

## Address

You will be able to:

* **Create address**
* **Read list of addresses**
* **Read address**
* **Update address**
* **Delete address**
* **Retrieve the addresses that are within a given distance and location coordinates.**
"""

app = FastAPI(
    title="Address Book Application",
    description=description,
    summary="Application where API users can create, update, delete addresses and retreive addresses within a given distance and location coordinates",
    version="0.0.1",
)

app.include_router(router.router)

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET, POST, PUT, DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Address Book Application"}