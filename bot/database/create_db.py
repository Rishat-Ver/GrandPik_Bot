import sqlite3


def create_database():
    connection = sqlite3.connect("GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS warehouse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article INTEGER NOT NULL,
            size TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            sales INTEGER NOT NULL DEFAULT 0,
            location INTEGER
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()