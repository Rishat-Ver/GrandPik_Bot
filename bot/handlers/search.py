from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from database.crud.read_data import get_items
from keyboards.default import main_keyboard
from handlers.states import SearchStates
from checkers.checker_params import chek_params_integer

router_search = Router()


@router_search.message(lambda message: message.text == "🔍")
async def search_prompt(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        f"Введите данные в формате:\n\n"
        f"артикул␣размер\n"
        f"артикул␣размер\n"
        f"и т д"
        )
    await state.set_state(SearchStates.waiting_for_search_input)


@router_search.message(SearchStates.waiting_for_search_input)
async def process_search(message: Message, state: FSMContext):
    many_items = message.text.split('\n')
    result = []

    for item in many_items:

        if len(item.split()) == 2:
            article, size = item.split()

            if not chek_params_integer(article):
                result.append(
                    f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                    f"Не корректно ввели данные\n"
                    f"Артикул - {article}\n"
                )
                continue

            object = get_items(article, size)
            if object:
                result.append(
                    "\n".join([
                        f"✅\n"
                        f"Артикул: {item[1]}\n"
                        f"Размер: {item[2]}\n"
                        f"Кол-во: {item[3]}\n"
                        f"Место: {item[5]}"
                        for item in object
                    ])
                )
            else:
                result.append(
                    f'Артикул: {article}\n'
                    f'Размер: {size}\n'
                    f'Нет такого товара'
                    )
        else:
            result.append(
                f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                f'Формат данных неверный.\n'
                f'Введите: артикул␣размер.'
                )

    await message.reply('\n---------------------------\n'.join(result), reply_markup=main_keyboard)
    await state.clear()


def register_handlers_search(dp):
    dp.include_router(router_search)
