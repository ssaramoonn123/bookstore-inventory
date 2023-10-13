

from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# Create a SQLite database
def get_db_connection():
    connection = sqlite3.connect('bookstore.db')
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Authors (
                AuthorID INTEGER PRIMARY KEY,
                AuthorName TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genres (
                GenreID INTEGER PRIMARY KEY,
                GenreName TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                BookID INTEGER PRIMARY KEY,
                Title TEXT,
                AuthorID INTEGER,
                GenreID INTEGER,
                Quantity INTEGER,
                Price REAL,
                PublicationYear INTEGER,
                ISBN TEXT
            )
        ''')
        conn.commit()
        conn.close()

def add_author(author_name):
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Authors (AuthorName) VALUES (?)', (author_name,))
        conn.commit()
        return cursor.lastrowid  # Get the ID of the newly added author

def add_genre(genre_name):
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Genres (GenreName) VALUES (?)', (genre_name,))
        conn.commit()
        return cursor.lastrowid  # Get the ID of the newly added genre

def add_book(title, author_id, genre_id, quantity, price, year, isbn):
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Books (Title, AuthorID, GenreID, Quantity, Price, PublicationYear, ISBN)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, author_id, genre_id, quantity, price, year, isbn))
        conn.commit()
        conn.close()

def list_books():
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT Title, AuthorName, GenreName, Quantity, Price FROM Books, Authors, Genres WHERE Books.AuthorID = Authors.AuthorID AND Books.GenreID = Genres.GenreID')
        books = cursor.fetchall()
        book_list = []
        for book in books:
            book_list.append({
                "Title": book[0],
                "Author": book[1],
                "Genre": book[2],
                "Quantity": book[3],
                "Price": round(book[4], 2)
            })
        conn.close()
        return book_list

@app.route('/')
def index():
    return render_template('index.html', books=list_books())

@app.route('/add_book_route', methods=['POST'])
def add_book_route():
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author_name']
        genre_name = request.form['genre_name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        year = int(request.form['year'])
        isbn = request.form['isbn']

        cursor = get_db_connection().cursor()
        cursor.execute('SELECT AuthorID FROM Authors WHERE AuthorName = ?', (author_name,))
        author_id = cursor.fetchone()
        if author_id is None:
            author_id = add_author(author_name)
        else:
            author_id = author_id[0]

        cursor.execute('SELECT GenreID FROM Genres WHERE GenreName = ?', (genre_name,))
        genre_id = cursor.fetchone()
        if genre_id is None:
            genre_id = add_genre(genre_name)
        else:
            genre_id = genre_id[0]

        add_book(title, author_id, genre_id, quantity, price, year, isbn)

        # Get the book details
        cursor.execute('SELECT Title, AuthorName, GenreName, Quantity, Price FROM Books, Authors, Genres WHERE Books.AuthorID = Authors.AuthorID AND Books.GenreID = Genres.GenreID AND Title = ?', (title,))
        book_data = cursor.fetchone()
        if book_data:
            return jsonify({'success': True, 'book': {
                "Title": book_data[0],
                "Author": book_data[1],
                "Genre": book_data[2],
                "Quantity": book_data[3],
                "Price": round(book_data[4], 2)
            }})

    return jsonify({'success': False})

# ...

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
