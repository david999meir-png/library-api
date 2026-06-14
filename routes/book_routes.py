import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from database.book_db import BookDB
from database.member_db import MemberDB



class Book(BaseModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"]

class BookUP(BaseModel):
    title: str | None = Field(max_length=50,default=None)
    author: str | None = Field(max_length=50, default=None)
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"] | None = None


router = APIRouter()


@router.post("", status_code=201)
def add_book(book: Book):
    logging.info(f"A request to add a new book has been received at add_bood func.")
    new_id = BookDB.create_book(book.model_dump())
    logging.info(f"Request to add a new book completed new id {new_id}")
    return {'new_id': new_id}   
    

@router.get("")
def get_all_book():
    logging.info("Request to receive all books has been accepted.")
    books = BookDB.get_all_books()
    logging.info("Request to receive all books was successfully granted.")

    return books

@router.get("/{id}")
def get_book_by_id(id: int):
    logging.info("Request to receive  book by id has been accepted.")

    book = BookDB.get_book_by_id(id)

    if book is None:
        logging.error(f"book id {id} not found")
        raise HTTPException(status_code=404, detail=f"book id {id} not found")
    
    logging.info(f"Request to receive book by id {id} was successfully granted.")
    return book


@router.patch("/{id}")
def update_book(id, data: BookUP):
    logging.info(f"Request to update book by id: {id} has been accepted.")
    updated = BookDB.update_book(id, data.model_dump(exclude_none=True))

    if not updated:
        logging.error(f"book id {id} not found")
        raise HTTPException(status_code=404, detail=f"book id {id} not found")
    
    logging.info(f"Request to update book by id {id} was successfully granted.")
    return {"msg": f"book {id} updated successfully."}


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logging.info(f"A request to borrow a book id: {id} was received from a member id {member_id}.")
    member_found = MemberDB.active_member(member_id)

    if member_found is None:
        logging.error(f"member id {id} not found")
        raise HTTPException(status_code=404, detail=f"book id {id} not found")

    if member_found["is_active"]:
        logging.error(f"member id {member_id} is not active")
        raise HTTPException(status_code=400, detail=f"member id {member_id} he isn't active.")
    
    book_details = BookDB.get_book_by_id(id)
    if book_details is None:
        logging.error(f"book id {id} not found")
        raise HTTPException(status_code=404, detail=f"book id {id} not found")
    
    available = book_details["is_available"]

    if not available:
        logging.error(f"book id {id} alrady borrowed")
        raise HTTPException(status_code=400, detail=f"Book id {id} is not available")

    books_alrady_borrowed = BookDB.count_active_borrows_by_member(member_id)

    if books_alrady_borrowed >= 3:
        logging.error(f"Member id {member_id} has reached maximum borrows")
        raise HTTPException(status_code=400, detail=f"Member id {id} has reached maximum borrows")
    
    BookDB.set_available(id, False, member_id)
    MemberDB.increment_borrows(member_id)

    logging.info(f"book {id} borrowed to member id {member_id} successfully")
    return {"msg": f"book {id} borrowed to member id {member_id} successfully"}


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logging.info(f"A request to return a book id: {id} was received from a member id {member_id}.")

    book_details = BookDB.get_book_by_id(id)

    if book_details is None:
        logging.error(f"book id {id} not found")
        raise HTTPException(status_code=404, detail=f"book id {id} not found")
    
    member_found = MemberDB.active_member(member_id)

    if member_found is None:
        logging.error(f"member id {id} not found")
        raise HTTPException(status_code=404, detail=f"book id {id} not found")
    
    available = book_details["is_available"]

    if available:
        logging.error(f"book id {id} alrady borrowed")
        raise HTTPException(status_code=400, detail=f"Book id {id} is not available")
    
    if book_details["borrowed_by_member_id"] != member_id:
        logging.error(f"book is not borrowed by this member ")
        raise HTTPException(status_code=400, detail="book is not borrowed by this member")
    
    BookDB.set_available(id, True, None)
    \
    logging.info(f"book {id} return by member id {member_id} successfully")
    return {"msg": f"book {id} return by member id {member_id} successfully"}
