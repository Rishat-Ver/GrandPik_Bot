from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from database.crud.read_data import get_items
from keyboards.default import main_keyboard
from handlers.states import SearchStates

router_search = Router()


@router_search.message(lambda message: message.text == "Найти")
async def search_prompt(message: Message, state: FSMContext):

    await message.reply("Введите данные в формате:\n\n<артикул><ПРОБЕЛ><размер>\n<артикул><ПРОБЕЛ><размер>\nи т д")
    await state.set_state(SearchStates.waiting_for_search_input)


@router_search.message(SearchStates.waiting_for_search_input)
async def process_search(message: Message, state: FSMContext):
    many_items = message.text.split('\n')
    result = []

    for item in many_items:

        if len(item.split()) == 2:
            article, size = item.split()
            object = get_items(article, size)
            if object:
                result.append(
                    "\n".join([
                        f"Артикул: {item[1]}\n"
                        f"Размер: {item[2]}\n"
                        f"Кол-во: {item[3]}\n"
                        f"Место: {item[5]}"
                        for item in object
                    ])
                )
            else:
                result.append(f'Артикул: {article}\nРазмер: {size}\nНет такого тавара')
        else:
            result.append(f'{item}\nФормат данных неверный.\nВведите: <артикул><ПРОБЕЛ><размер>.')

    await message.reply('\n---------------------------\n'.join(result), reply_markup=main_keyboard)
    await state.clear()


def register_handlers_search(dp):
    dp.include_router(router_search)
