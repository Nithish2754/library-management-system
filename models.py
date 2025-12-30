from db import get_db_connection

def init_db():
    from db import init_db as _init
    _init()

def add_book(isbn, title, author, copies):
    try:
        copies = int(copies)
    except:
        copies = 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT copies FROM books WHERE isbn = %s", (isbn,))
    row = cursor.fetchone()
    if row:
        new_copies = row[0] + copies
        cursor.execute("UPDATE books SET copies = %s, title = %s, author = %s WHERE isbn = %s",
                       (new_copies, title, author, isbn))
        conn.commit()
        conn.close()
        return "DUPLICATE"
    else:
        cursor.execute("INSERT INTO books (isbn, title, author, copies) VALUES (%s, %s, %s, %s)",
                       (isbn, title, author, copies))
        conn.commit()
        conn.close()
        return "SUCCESS"

def list_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT isbn, title, author, copies FROM books")
    rows = cursor.fetchall()
    conn.close()
    return [{'isbn': r[0], 'title': r[1], 'author': r[2], 'copies': r[3]} for r in rows]

def get_book(isbn):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT isbn, title, author, copies FROM books WHERE isbn = %s", (isbn,))
    r = cursor.fetchone()
    conn.close()
    if r:
        return {'isbn': r[0], 'title': r[1], 'author': r[2], 'copies': r[3]}
    return None

def remove_book(isbn):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT isbn FROM books WHERE isbn = %s", (isbn,))
    if not cursor.fetchone():
        conn.close()
        return "NO_BOOK"
    cursor.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
    conn.commit()
    conn.close()
    return "SUCCESS"

def add_member(member_id, name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO members (member_id, name) VALUES (%s, %s)", (member_id, name))
        conn.commit()
        return "SUCCESS"
    except Exception:
        return "DUPLICATE"
    finally:
        conn.close()

def list_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT member_id, name FROM members")
    rows = cursor.fetchall()
    conn.close()
    return [{'member_id': r[0], 'name': r[1]} for r in rows]

def issue_book(isbn, member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT copies FROM books WHERE isbn = %s", (isbn,))
    book = cursor.fetchone()
    if not book:
        conn.close()
        return "NO_BOOK"
    cursor.execute("SELECT member_id FROM members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()
    if not member:
        conn.close()
        return "NO_MEMBER"
    copies = book[0]
    if copies <= 0:
        conn.close()
        return "NO_COPIES"
    cursor.execute("UPDATE books SET copies = copies - 1 WHERE isbn = %s", (isbn,))
    cursor.execute("INSERT INTO transactions (isbn, member_id, type) VALUES (%s, %s, %s)", (isbn, member_id, "ISSUE"))
    conn.commit()
    conn.close()
    return "SUCCESS"

def return_book(isbn, member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM transactions
        WHERE isbn = %s AND member_id = %s AND type = 'ISSUE'
        ORDER BY timestamp DESC LIMIT 1
    """, (isbn, member_id))
    issue_row = cursor.fetchone()
    if not issue_row:
        conn.close()
        return "NO_TRANSACTION"
    cursor.execute("INSERT INTO transactions (isbn, member_id, type) VALUES (%s, %s, %s)", (isbn, member_id, "RETURN"))
    cursor.execute("UPDATE books SET copies = copies + 1 WHERE isbn = %s", (isbn,))
    conn.commit()
    conn.close()
    return "SUCCESS"
