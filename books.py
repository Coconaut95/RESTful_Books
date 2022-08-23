#################################
# Dive into FastAPI, a web framework for developing modern RESTful APIs using Python. 
# FastAPI is built off of Starlette and Pydantic, therefore the performance of FastAPI is off the charts. 
# Pydantic allows type hints to perform data validation and serialization / deserialization of data. 
# astAPI automatically creates interactive Swagger UI documentation which is perfect for any developer. 
#################################

#Here i'll create created FastAPI
#HTTP METHODS REQUEST:
#GET (read), POST (create), PUT (update/replace), DELETE (se entiende)

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #when this line run, it create the DB and the table if thus doesn't exists

# This funtion handle the open and close of the DB
def get_db(): 
    try:
        db = SessionLocal
        yield db
    finally:
        db.close

# Schema
class Book(BaseModel):    
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101) # between 0 and 100

BOOKS = [] #it can be replace with a DB


@app.get('/') #'/{}' path parameter
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.post('/')
def create_books(book:Book, db: Session = Depends(get_db)):   

    book_model = models.Books() #Mimic the model "Books"
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.put('/{book_id}')
def update_book(book_id: UUID, book:Book):
    counter = 0
    for x in BOOKS:
        counter+=1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id}: Does not exist"
    )

@app.delete('/{book_id}')
def delete_book (book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter +=1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID: {book_id} delated"
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id}: Does not exist"
    )