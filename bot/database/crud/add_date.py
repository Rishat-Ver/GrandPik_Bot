import sqlite3


def add_or_update_item(article, size, quantity, location):

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id,
               article,
               size,
               quantity,
               location
          FROM warehouse
         WHERE article = ? AND size = ?
    """, (article, size))

    record = cursor.fetchone()

    if record and record[4] != 0:
        item_id, article, size, current_quantity, current_location = record
        new_quantity = current_quantity + int(quantity)

        cursor.execute("""
            UPDATE warehouse
               SET quantity = ?, location = ? WHERE id = ?
        """, (new_quantity, current_location, item_id))

        connection.commit()
        connection.close()

        return "updated", new_quantity, current_location

    elif record and record[4] == 0:

        new_quantity = current_quantity + int(quantity)

        cursor.execute("""
            UPDATE warehouse
               SET quantity = ?, location = ? WHERE id = ?
        """, (new_quantity, location, item_id))

        connection.commit()
        connection.close()

        return "updated_location", new_quantity, location
    else:

        cursor.execute("""
            INSERT INTO warehouse (article, size, quantity, location)
            VALUES (?, ?, ?, ?)
        """, (article, size, quantity, location))

        connection.commit()
        connection.close()

        return "added", quantity, location
