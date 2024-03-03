# ADRESS BOOK APPLICATION

## Download Codebase
Clone the repository using the command
```bash
git clone " "
```

## Setting up virtual environment
Run the following commands
```bash
cd address_book
conda create --prefix ./env python=3.10.13 -y
conda activate ./env
```
## Installing packages
```bash
pip install -r requirements/base.txt
```

## How to interact with application?
Run the following command to start the server
```bash
uvicorn main:app --reload
```
then, navigate to http://127.0.0.1:8000/docs to get Swagger UI