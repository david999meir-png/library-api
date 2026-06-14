import logging
from database import db_connection


class BookDB:
    @staticmethod
    def create_book(data: dict) -> int:
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """INSERT INTO books (title, author, genreb, is_available, borrowed_by_member_id) VALUES(%s, %s, %s, %s, %s)"""
        values = list(data.values())

        cursor.execute(sql, values)
        logging.info(f"a book name {data["title"]} created at genre {data["genre"]}")
        conn.commit()

        new_id = cursor.lastrowid
        
        cursor.close()
        conn.close()

        return new_id
    
    @staticmethod
    def get_all_books():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT * FROM books"""
        cursor.execute(sql)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
    
    @staticmethod
    def get_book_by_id(book_id):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT * FROM books WHERE id = %s"""
        cursor.execute(sql, (book_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()
        return row

    @staticmethod
    def update_book(book_id: int, data: dict) -> bool:
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        list_couse = [f"{key}=%s" for key in data.keys()]
        txt_clouse = ", ".join(list_couse)

        sql = f"UPDATE books SET {txt_clouse} WHERE id = %s"
        values = list(data.values()) + [book_id]

        cursor.execute(sql, values)
        logging.info(f"book id {book_id} updated to {data}")

        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def set_available(book_id: int, val: bool, member_id: int) -> bool:
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """UPDATE books SET is_available=%s borrowed_by_member_id=%s WHERE id = %s"""
        cursor.execute(sql, (val, member_id, book_id))

        logging.info(f"book id {book_id} updated to is_available = {val} borrowed_by_member_id: {member_id}")

        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def count_total() -> int:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT COUNT(*) AS total_books FROM books AS total_books"""
        cursor.execute(sql)

        value = cursor.fetchone()

        cursor.close()
        conn.close()
        
        return value["total_books"]

    @staticmethod
    def count_available_books() -> int:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT COUNT(is_available) AS available_books FROM books WHERE is_available = TRUE"""
        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["available_books"]
    
    @staticmethod
    def count_borrowed_books() -> int:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT COUNT(is_available) AS not_available_books FROM books WHERE is_available = FALSE"""
        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["not_available_books"]
    
    @staticmethod
    def count_by_genre(genre: str) -> int:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT COUNT(genre) AS sum_books_by_genre FROM books WHERE genre=$s"""

        cursor.execute(sql, (genre,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["sum_books_by_genre"]

    @staticmethod
    def count_active_borrows_by_member(member_id: int) -> int:
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT COUNT(borrowed_by_member_id) AS total_membet_borrowed_books WHERE borrowed_by_member_id = %s"""
        cursor.execute(sql, (member_id,))

        sum_books = cursor.fetchone()

        cursor.close()
        conn.close()

        return sum_books["total_membet_borrowed_books"]
    