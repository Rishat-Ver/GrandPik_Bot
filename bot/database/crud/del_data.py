import sqlite3


def update_item_for_delete(article, size, quantity):

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, quantity, sales, location
          FROM warehouse
         WHERE article = ? AND size = ?
    """, (article, size))
    record = cursor.fetchone()

    if record:
        item_id, current_quantity, current_sales, location = record
        quantity = int(quantity)

        if current_quantity >= quantity:
            new_quantity = current_quantity - quantity
            new_sales = current_sales + quantity

            cursor.execute("""
                UPDATE warehouse
                   SET quantity = ?, sales = ? WHERE id = ?
            """, (new_quantity, new_sales, item_id))

            connection.commit()
            connection.close()

            return "updated", article, new_quantity, location
        else:
            return "no updated", article, current_quantity, location

    else:
        connection.close()
        return "Нечего забирать", None, None, None
