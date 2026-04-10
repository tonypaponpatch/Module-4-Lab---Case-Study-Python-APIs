from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration for books.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Book model for ID, Name, Author, and Publisher
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.book_name} - {self.author}"

# --- API Routes ---

# 1. Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = []
    for b in books:
        output.append({'id': b.id, 'book_name': b.book_name, 'author': b.author, 'publisher': b.publisher})
    return {"books": output}

# 2. Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], 
                author=request.json['author'], 
                publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id, 'message': 'Book added successfully!'}

# 3. Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted!"}

