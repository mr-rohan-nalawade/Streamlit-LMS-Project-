import mysql.connector

def connect():
    db_errors = []
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="lms"
            )
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS BOOKS (
                       BOOK_ID INT AUTO_INCREMENT PRIMARY KEY,
                       TITLE VARCHAR(100) NOT NULL,
                       AUTHOR VARCHAR(50) NOT NULL,
                       GENRE VARCHAR(50) NOT NULL,
                       TOTAL_COPIES INT NOT NULL,
                       AVAILABLE_COPIES INT NOT NULL)
                       """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS MEMBERS (
                       MEMBER_ID INT AUTO_INCREMENT PRIMARY KEY,
                       MEMBER_NAME VARCHAR(50) NOT NULL,
                       EMAIL VARCHAR(50) UNIQUE NOT NULL,
                       JOIN_DATE DATE NOT NULL,
                       STATUS ENUM('Active', 'Inactive') DEFAULT 'Active')
                       """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS TRANSACTIONS (
                       ISSUE_ID INT AUTO_INCREMENT PRIMARY KEY,
                       MEMBER_ID INT NOT NULL,
                       BOOK_ID INT NOT NULL,
                       ISSUE_DATE DATE NOT NULL,
                       DUE_DATE DATE NOT NULL,
                       RETURN_DATE DATE DEFAULT NULL,
                       FOREIGN KEY (MEMBER_ID) REFERENCES MEMBERS(MEMBER_ID),
                       FOREIGN KEY (BOOK_ID) REFERENCES BOOKS(BOOK_ID)
                       )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS ADMINISTRATION (
                       ADMIN_ID INT AUTO_INCREMENT PRIMARY KEY,
                       ADMIN_NAME VARCHAR(50) NOT NULL,
                       PASSWORD VARCHAR(100)
                       )""")
        conn.commit()
        return conn, db_errors
    except mysql.connector.Error as err:
        db_errors.append(f"{err}")
        return False, db_errors