import sqlite3

DB_NAME = "library.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    year INTEGER,
    quantite INTEGER   -- Ajout de la colonne quantite avec une valeur par défaut de 1
)''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('user', 'admin')) DEFAULT 'user' -- rôle par défaut
)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS loans (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            book_id INTEGER,
                            borrower_name TEXT NOT NULL,
                            borrow_date TEXT NOT NULL,
                            return_date TEXT,
                            quantite INTEGER NOT NULL,
                            FOREIGN KEY (book_id) REFERENCES books(id)
)''')
         
    conn.commit()
    conn.close()


def show_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables existantes :", tables)
    conn.close()

