from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import sqlite3
import os
from handlers.states import RequestaSqlStates


router_sql = Router()


@router_sql.message(Command("sql"))
async def requests_sql(message: Message, state: FSMContext):

    await state.clear()

    user_id = message.from_user.id

    if user_id not in (int(os.getenv('ID_IY')), int(os.getenv('ID_VR'))):
        await message.answer("У вас нет прав для использования этой функции.", show_alert=True)
        return

    await message.answer(f"Введите запрос !")

    await state.set_state(RequestaSqlStates.waiting_for_requests_sql_input)


@router_sql.message(RequestaSqlStates.waiting_for_requests_sql_input)
async def process_search(message: Message, state: FSMContext):

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    try:
        cursor.execute(f"{message.text}")
        result = cursor.fetchall()
        connection.commit()
        await message.answer(f"Успешный запрос\n\n{result}")
    except Exception as e:
        await message.answer("Произошла ошибка !!!")
    finally:
        connection.close()
        await state.clear()


def registr_sql(dp):
    dp.include_router(router_sql)



# DELETE FROM warehouse
# DELETE FROM sqlite_sequence WHERE name='warehouse'