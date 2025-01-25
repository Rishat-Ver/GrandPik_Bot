from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.default import main_keyboard
from database.crud.add_date import add_or_update_item
from handlers.states import AddStates


router_add_item = Router()


@router_add_item.message(lambda message: message.text == "Добавить")
async def add_prompt(message: Message, state: FSMContext):

    await message.reply("Введите данные в формате:\n<артикул><ПРОБЕЛ><размер>")
    await state.set_state(AddStates.waiting_for_add_input)


@router_add_item.message(AddStates.waiting_for_add_input)
async def process_add(message: Message, state: FSMContext):

    if len(message.text.split()) == 2:
        article, size = message.text.split()
        result, location = add_or_update_item(article, size)

        if result == "updated":
            response = f"Запись обновлена:\nАртикул: {article}\nразмер: {size}\nМесто на складе {location}"
        else:
            response = f"Новая запись добавлена:\nАртикул: {article}\nразмер: {size}\nМесто на складе {location}"

        await message.reply(response, reply_markup=main_keyboard)
    else:
        await message.reply("Ошибка: формат ввода неверный\nВведите данные в формате:\n<артикул><ПРОБЕЛ><размер>")

    await state.clear()


def register_handlers_add_item(dp):
    dp.include_router(router_add_item)
