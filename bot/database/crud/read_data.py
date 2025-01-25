import sqlite3


def get_items(article, size):
    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM warehouse WHERE article = ? AND size = ?
    """, (article, size))

    items = cursor.fetchall()
    connection.close()

    return items