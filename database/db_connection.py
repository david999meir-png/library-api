import mysql.connector


def get_connection():
    return mysql.connector.connect(host="127.0.0.1", port=3306, user="root", password="root", database="library_db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    sql_book = """
        CREATE TABLE IF NOT EXISTS books(
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(50) NOT NULL, 
        author VARCHAR(50) NOT NULL,
        genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
        is_available BOOLEAN DEFAULT TRUE NOT NULL,
        borrowed_by_member_id INT
        )
        """
    sql_members = """
            CREATE TABLE IF NOT EXISTS members(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            is_active boolean DEFAULT TRUE NOT NULL, 
            total_borrows INT DEFAULT 0
            )
            """
    cursor.execute(sql_book)
    cursor.execute(sql_members)

    conn.commit()
    
    cursor.close()
    conn.close()