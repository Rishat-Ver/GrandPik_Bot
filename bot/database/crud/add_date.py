import sqlite3


def add_or_update_item(article, size):

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, quantity, location FROM warehouse WHERE article = ? AND size = ?
    """, (article, size))
    record = cursor.fetchone()

    if record:
        item_id, current_quantity, location = record
        new_quantity = current_quantity + 1
        cursor.execute("""
            UPDATE warehouse SET quantity = ?, location = ? WHERE id = ?
        """, (new_quantity, location, item_id))
        connection.commit()
        connection.close()
        return "updated", location
    else:
        min_location, max_location = check_location()
        print(min_location, max_location)
        location = min_location if min_location is not None else max_location
        print(location)
        cursor.execute("""
            INSERT INTO warehouse (article, size, quantity, location)
            VALUES (?, ?, ?, ?)
        """, (article, size, 1, location))

        connection.commit()
        connection.close()

        return "added", location


def check_location():

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    max_location = cursor.fetchone()
    min_location = None

    cursor.execute("""
        SELECT MAX(location)
          FROM warehouse
    """)

    max_location = cursor.fetchone()[0] + 1

    cursor.execute("""
        SELECT location, COUNT(*)
          FROM warehouse
         GROUP BY location
    """)

    record = cursor.fetchall()
    print(record)
    for i in record:
        if i[1] < 8:
            min_location = i[0]

    connection.commit()
    connection.close()

    return min_location, max_location
