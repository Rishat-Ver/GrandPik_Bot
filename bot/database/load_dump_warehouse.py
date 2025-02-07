import sqlite3
import pandas as pd

def load_data_from_excel(file_path, db_path="bot/database/GP_warehouse.db"):


    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Ошибка чтения Excel файла: {e}")
        return


    required_columns = {"article", "size", "quantity", "sales", "location"}
    if not required_columns.issubset(data.columns):
        print(f"Excel файл должен содержать как минимум следующие колонки: {required_columns}")
        return

    data = data.fillna({
        "article": 0,
        "size": "",
        "quantity": 0,
        "sales": 0,
    })


    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()


    for _, row in data.iterrows():
        cursor.execute("""
            INSERT INTO warehouse (article, size, quantity, sales, location)
            VALUES (?, ?, ?, ?, ?)
        """, (
            row["article"],
            row["size"],
            int(row["quantity"]),
            int(row["sales"]),
            int(row["location"])
        ))

    connection.commit()
    connection.close()

    print("Данные успешно загружены в базу данных.")


if __name__ == "__main__":
    load_data_from_excel("bot/database/data.xlsx")
