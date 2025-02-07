from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from openpyxl import Workbook
from aiogram.fsm.context import FSMContext

import sqlite3
import os
from io import BytesIO


router_export = Router()


@router_export.message(Command("export"))
async def export_database_to_excel(message: Message):

    user_id = message.from_user.id

    if user_id not in (int(os.getenv('ID_IY')), int(os.getenv('ID_VR'))):
        await message.answer("У вас нет прав для использования этой функции.", show_alert=True)
        return

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT article, size, quantity, sales, location
        FROM warehouse
    """)
    data = cursor.fetchall()
    connection.close()

    if not data:
        await message.answer("В базе данных нет данных для экспорта.")
        return

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Warehouse"

    headers = ["Article", "Size", "Quantity", "Sales", "Location"]
    sheet.append(headers)

    for row in data:
        sheet.append(row)

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    await message.answer_document(
        BufferedInputFile(buffer.getvalue(), filename="warehouse_data.xlsx"),
        caption="Данные из базы в формате Excel"
    )


def registr_export(dp):
    dp.include_router(router_export)
