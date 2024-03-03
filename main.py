from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from src.address import router
from src.address import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
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