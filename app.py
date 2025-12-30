from flask import Flask, render_template, request, redirect, flash
from models import (
    init_db,
    add_book,
    list_books,
    add_member,
    list_members,
    issue_book,
    return_book,
    remove_book
)

# Use standard folders
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "your_secret_key_here"

# Initialize DB (creates tables if not present)
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        isbn = request.form['isbn'].strip()
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        copies = request.form.get('copies', '0').strip()
        result = add_book(isbn, title, author, copies)
        if result == "SUCCESS":
            flash("Book added successfully!", "success")
        elif result == "DUPLICATE":
            flash("Book already existed — copies updated.", "success")
        else:
            flash("An error occurred while adding the book.", "error")
        return redirect('/')
    return render_template('add_book.html')

@app.route('/books')
def books():
    books = list_books()
    return render_template('books.html', books=books)

@app.route('/remove_book', methods=['POST'])
def remove_book_route():
    isbn = request.form.get('isbn')
    if not isbn:
        flash("ISBN is required to remove a book.", "error")
        return redirect('/books')
    res = remove_book(isbn)
    if res == "SUCCESS":
        flash("Book removed successfully.", "success")
    else:
        flash("Book not found.", "error")
    return redirect('/books')

@app.route('/add_member', methods=['GET', 'POST'])
def create_member():
    if request.method == 'POST':
        member_id = request.form['member_id'].strip()
        name = request.form['name'].strip()
        res = add_member(member_id, name)
        if res == "SUCCESS":
            flash("Member added successfully!", "success")
        else:
            flash("Member ID already exists!", "error")
        return redirect('/')
    return render_template('add_member.html')

@app.route('/members')
def members():
    members = list_members()
    return render_template('members.html', members=members)

@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if request.method == 'POST':
        isbn = request.form['isbn'].strip()
        member_id = request.form['member_id'].strip()
        res = issue_book(isbn, member_id)
        if res == "SUCCESS":
            flash("Book issued successfully!", "success")
        elif res == "NO_BOOK":
            flash("Book not found.", "error")
        elif res == "NO_MEMBER":
            flash("Member not found.", "error")
        elif res == "NO_COPIES":
            flash("No copies available to issue.", "error")
        else:
            flash("An error occurred.", "error")
        return redirect('/')
    books = list_books()
    members = list_members()
    return render_template('issue.html', books=books, members=members)

@app.route('/return', methods=['GET', 'POST'])
def return_route():
    if request.method == 'POST':
        isbn = request.form['isbn'].strip()
        member_id = request.form['member_id'].strip()
        res = return_book(isbn, member_id)
        if res == "SUCCESS":
            flash("Book returned successfully!", "success")
        elif res == "NO_TRANSACTION":
            flash("No matching issue record found.", "error")
        else:
            flash("An error occurred.", "error")
        return redirect('/')
    books = list_books()
    members = list_members()
    return render_template('return.html', books=books, members=members)

if __name__ == '__main__':
    # If port 5000 is problematic you can run: python app.py --port 5001
    app.run(debug=True)
