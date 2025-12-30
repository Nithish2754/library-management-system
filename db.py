import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="nithish@2754",   # change if different
        database="library_db",
        auth_plugin="mysql_native_password"
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            isbn VARCHAR(50) PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            copies INT DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            isbn VARCHAR(50),
            member_id VARCHAR(50),
            type VARCHAR(20),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE,
            FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()
