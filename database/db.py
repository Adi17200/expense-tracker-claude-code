import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = 'spendly.db'

def get_db():
    """
    Returns a SQLite connection with row_factory and foreign keys enabled.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates the users and expenses tables using CREATE TABLE IF NOT EXISTS.
    """
    conn = get_db()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Expenses table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()

def seed_db():
    """
    Inserts sample data for development if the database is empty.
    """
    conn = get_db()

    # Check if users table already contains data
    user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    if user:
        conn.close()
        return

    # Insert demo user
    hashed_pw = generate_password_hash('demo123')
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", hashed_pw)
    )
    user_id = cursor.lastrowid

    # Insert 8 sample expenses covering all required categories
    # Categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
    expenses = [
        (15.50, "Food", "2026-10-01", "Lunch at Cafe"),
        (45.00, "Transport", "2026-10-02", "Gas refill"),
        (120.00, "Bills", "2026-10-03", "Internet bill"),
        (30.00, "Health", "2026-10-05", "Pharmacy"),
        (60.00, "Entertainment", "2026-10-07", "Movie night"),
        (85.20, "Shopping", "2026-10-10", "New shoes"),
        (12.00, "Other", "2026-10-12", "Postage"),
        (25.00, "Food", "2026-10-15", "Grocery store"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        [(user_id, *exp) for exp in expenses]
    )

    conn.commit()
    conn.close()
