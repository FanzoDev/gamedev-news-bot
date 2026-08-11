import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "bot.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT UNIQUE NOT NULL,
    published TEXT,
    category TEXT DEFAULT 'OTHER',
    summary TEXT,
    is_relevant INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE NOT NULL,
        category TEXT DEFAULT 'ALL',
        active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            initialized INTEGER DEFAULT 0,
            initialized_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    connection.commit()
    connection.close()


def news_exists(link):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM news WHERE link = ?",
        (link,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def save_news(source, title, link, published, category, summary=""):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO news (
                source,
                title,
                link,
                published,
                category,
                summary
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            source,
            title,
            link,
            published,
            category,
            summary
        ))

        connection.commit()
        saved = True

    except sqlite3.IntegrityError:
        saved = False

    connection.close()

    return saved

def add_subscriber(phone, category="ALL"):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO subscribers (phone, category)
            VALUES (?, ?)
        """, (phone, category))

        connection.commit()
        result = True

    except sqlite3.IntegrityError:
        result = False

    connection.close()

    return result

def remove_subscriber(phone):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE subscribers
        SET active = 0
        WHERE phone = ?
    """, (phone,))

    connection.commit()

    removed = cursor.rowcount > 0

    connection.close()

    return removed

def get_subscribers(category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT phone
        FROM subscribers
        WHERE active = 1
        AND (category = ? OR category = 'ALL')
    """, (category,))

    subscribers = cursor.fetchall()

    connection.close()

    return [row[0] for row in subscribers]

def update_subscriber_category(phone, category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE subscribers
        SET category = ?, active = 1
        WHERE phone = ?
    """, (category, phone))

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated

def get_latest_news(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT source, title, link, published, category
        FROM news
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    news = cursor.fetchall()

    connection.close()

    return news


def source_exists(source_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM sources WHERE name = ?",
        (source_name,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def is_source_initialized(source_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT initialized FROM sources WHERE name = ?",
        (source_name,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return False

    return result[0] == 1


def initialize_source(source_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO sources (
            name,
            initialized
        )
        VALUES (?, 0)
    """, (source_name,))

    connection.commit()
    connection.close()


def mark_source_initialized(source_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE sources
        SET initialized = 1,
            initialized_at = CURRENT_TIMESTAMP
        WHERE name = ?
    """, (source_name,))

    connection.commit()
    connection.close()


if __name__ == "__main__":

    initialize_database()

    print("Database berhasil dibuat!")

    add_subscriber("628123456789", "ALL")
    add_subscriber("628987654321", "ENGINE")
    add_subscriber("628555555555", "AI")

    print()
    print("Subscriber ENGINE:")

    subscribers = get_subscribers("ENGINE")

    for phone in subscribers:
        print(phone)
