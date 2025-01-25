import pandas as pd
import sqlite3


def load_data_from_excel(excel_file, db_path):

    df = pd.read_excel(excel_file)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for index, row in df.iterrows():
        article = row['article']
        size = row['size']
        quantity = row['quantity']
        sales = row['sales']
        location = row['location']

        cursor.execute("""
            INSERT INTO warehouse (article, size, quantity, sales, location)
            VALUES (?, ?, ?, ?, ?)
        """, (article, size, quantity, sales, location))

    connection.commit()
    connection.close()

    print("Данные успешно загружены в базу данных.")
