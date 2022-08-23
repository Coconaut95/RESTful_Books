#################################
# Dive into FastAPI, a web framework for developing modern RESTful APIs using Python. 
# FastAPI is built off of Starlette and Pydantic, therefore the performance of FastAPI is off the charts. 
# Pydantic allows type hints to perform data validation and serialization / deserialization of data. 
# astAPI automatically creates interactive Swagger UI documentation which is perfect for any developer. 
#################################

#Here i'll create created FastAPI
#HTTP METHODS REQUEST:
#GET (read), POST (create), PUT (update/replace), DELETE (se entiende)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id : UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101) # between 0 and 100

BOOKS = [] 

@app.post('/')
def create_books(book:Book):
    BOOKS.append(book)
    return book

@app.get('/') #'/{}' path parameter
def read_api():
    return BOOKS

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