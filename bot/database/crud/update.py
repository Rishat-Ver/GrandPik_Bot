import sqlite3


def update_location(article, size, location):

    connection = sqlite3.connect("/home/rishik/GrandPik_bot/bot/database/GP_warehouse.db") # "bot/database/GP_warehouse.db"
    cursor = connection.cursor()

    cursor.execute(
        f"""
            UPDATE warehouse
               SET location = {location}
            WHERE article = {article}
                  AND size = {size};
        """)

    connection.commit()
    connection.close()

    return article, size, location
