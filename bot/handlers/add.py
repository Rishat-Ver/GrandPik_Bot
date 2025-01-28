from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.default import main_keyboard
from database.crud.add_date import add_or_update_item
from handlers.states import AddStates
from checkers.checker_params import chek_params_integer


router_add_item = Router()


@router_add_item.message(lambda message: message.text == "Добавить")
async def add_prompt(message: Message, state: FSMContext):

    await message.answer(
        f"Введите данные в формате:\n\n"
        f"артикул␣размер␣кол-во␣место\n"
        f"артикул␣размер␣кол-во␣место\n"
        f"и т д**",
        parse_mode='Markdown'
    )
    await state.set_state(AddStates.waiting_for_add_input)


@router_add_item.message(AddStates.waiting_for_add_input)
async def process_add(message: Message, state: FSMContext):
    result = []

    for item in message.text.split('\n'):

        if len(item.split()) == 4:

            article, size, quantity, location = item.split()

            check_param = [True if chek_params_integer(param) else False for param in (article, quantity, location)]
            if not all(check_param):
                result.append(
                    f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                    f"Не корректно ввели данные\n"
                    f"для артикула {article}\n"
                    f"Запись НЕ обновилась/добавилась\n"
                    f"---------------------------------"
                )
                continue

            action, quantity, location = add_or_update_item(article, size, quantity, location)

            if action == 'updated':
                response = (
                    f"Запись обновлена: ✅\n\n"
                    f"Артикул: {article}\n"
                    f"Размер: {size}\n"
                    f"Текущее кол-во: {quantity}\n"
                    f"Место: {location}\n\n"
                    f"Обрати внимание на место, место выбранно не то которое ты вводил, т.к данное панно уже присутствует на складе\n"
                    f"---------------------------------"
                    )
                result.append(response)
            else:
                response = (
                    f"Новая запись добавлена: ✅\n\n"
                    f"Артикул: {article}\n"
                    f"Размер: {size}\n"
                    f"Текущее кол-во: {quantity}\n"
                    f"Место: {location}\n"
                    f"---------------------------------"
                    )
                result.append(response)
        else:
            response = (
                f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                f"Ошибка: формат ввода неверный.\n"
                f"Введите данные в формате:\n"
                f"артикул␣размер␣кол-во␣место"
            )
            result.append(response)

    await message.reply('\n'.join(result), reply_markup=main_keyboard)

    await state.clear()


def register_handlers_add_item(dp):
    dp.include_router(router_add_item)
