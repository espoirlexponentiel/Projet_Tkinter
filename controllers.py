from database import connect
import sqlite3

def add_book(title, author, genre, year, quantite):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, genre, year, quantite) VALUES (?, ?, ?, ?, ?)",
                   (title, author, genre, year, quantite))
    conn.commit()
    conn.close()

def get_books():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, genre, year, quantite FROM books")
    books = cursor.fetchall()
    conn.close()
    return books


def delete_book(book_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()


def update_book(book_id, title, author, genre, year, quantite):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE books
    SET title = ?, author = ?, genre = ?, year = ?, quantite = ?
    WHERE id = ?
    """, (title, author, genre, year, quantite, book_id))
    conn.commit()
    conn.close()

def update_book_quantity(book_id, quantite):
    try:
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET quantite = ? WHERE id = ?", (quantite, book_id))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour de la quantité du livre : {e}")
