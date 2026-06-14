import logging
from database import db_connection


class MemberDB:
    @staticmethod
    def create_membear(data: dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """INSERT INTO members (name, email) VALUES (%s, %s)"""
        values = list(data.values())

        cursor.execute(sql, values)
        logging.info(f"a new member created, member details: {data}")

        conn.commit()
        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return new_id
    
    @staticmethod
    def get_all_members():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT * FROM members"""
        cursor.execute(sql)

        members = cursor.fetchall()

        cursor.close()
        conn.close()

        return members
    
    @staticmethod
    def get_members_by_id(members_id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT * FROM members WHERE id=%s"""
        cursor.execute(sql, (members_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row
    
    @staticmethod
    def update_member(id: int, data: dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        cause_list = [f"{key}=%s" for key in data.keys()]
        cause_txt = ", ".join(cause_list)

        sql = f"UPDATE members SET {cause_txt} WHERE id = %s"
        values = list(data.values()) + [id]

        cursor.execute(sql, values)
        logging.info(f"member id: {id} updated, new data: {data}")
        conn.commit()

        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def deactive_member(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """UPDATE members SET is_active = FALSE WHERE id = %s"""
        cursor.execute(sql, (id,))

        logging.info(f"member id {id} become deactive")
        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
    
    @staticmethod
    def active_member(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """UPDATE members SET is_active = TRUE WHERE id = %s"""
        cursor.execute(sql, (id,))

        logging.info(f"member id {id} become active")

        conn.commit()
        changed = cursor.rowcount > 0

        cursor.close()
        conn.close()

        return changed
    
    @staticmethod
    def increment_borrows(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """UPDATE members SET total_borrows = total_borrows + 1 WHERE id = %s"""
        cursor.execute(sql,(id,))

        conn.commit()
        changed = cursor.rowcount > 0

        logging.info(f"member id: {id} updated to total borrow + 1")
        cursor.close()
        conn.close()

        return changed
    
    @staticmethod
    def count_active_members():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT COUNT(is_active) AS active_members FROM members WHERE is_active = TRUE"""
        cursor.execute(sql)
        active = cursor.fetchone()

        cursor.close()
        conn.close()

        return active

    @staticmethod
    def get_top_member():

        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """SELECT id, total_borrows FROM members
                ORDER BY total_borrows DESC
                LIMIT 1
        """
        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row