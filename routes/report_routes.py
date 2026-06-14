import logging
from fastapi import APIRouter, HTTPException
from database.book_db import BookDB
from database.member_db import MemberDB


router = APIRouter()


@router.get("/summary")
def get_summary():
    logging.info("Request for a general summary has been received.")
    total_books = BookDB.count_total()
    available_book = BookDB.count_available_books()
    borrowed_bookd = BookDB.count_borrowed_books()
    get_sum_active_members = MemberDB.count_active_members()

    logging.info("Request to receive a general summary has been completed successfully.")

    return {**total_books, **available_book, **borrowed_bookd, **get_sum_active_members}


@router.get("/reports/books-by-genre")
def get_summary_by_ganre():
    logging.info("Request for a summary by genre has been received.")

    rows = BookDB.count_by_genre()
    logging.info("Request to receive a summary by genre has been completed successfully.")

    return rows


@router.get("/top-member")
def get_most_active_member():
    logging.info("Request for get most active membet has been received.")
    top_member = MemberDB.get_top_member()

    logging.info("Request to receive get most active member has been completed successfully.")
    return top_member

