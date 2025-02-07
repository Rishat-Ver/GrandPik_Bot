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

    await state.clear()

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
                    f"---------------------------------"
                )
                continue

            action, quantity, location = add_or_update_item(article, size, quantity, location)

            if action == 'updated':
                response = (
                    f"Запись обновлена ✅\n\n"
                    f"Панно: {article}  {size}\n"
                    f"МЕСТО: {location}\n"
                    f"---------------------------------"
                    )
                result.append(response)
            elif action == 'updated_location':

                response = (
                    f"Запись обновлена ✅\n\n"
                    f"Панно: {article}  {size}\n"
                    f"МЕСТО: {location}\n\n"
                    f"---------------------------------"
                    )
                result.append(response)
            else:
                response = (
                    f"Новая запись: 🆕✅\n\n"
                    f"Панно: {article}  {size}  {quantity}шт.\n"
                    f"МЕСТО: {location}\n"
                    f"---------------------------------"
                    )
                result.append(response)
        else:
            data = ' '.join(item.split())
            response = (
                f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                f"Не корректно ввели данные\n"
                f"{data}\n"
                f"---------------------------------"
            )
            result.append(response)

    await message.reply('\n'.join(result), reply_markup=main_keyboard)

    await state.clear()


def register_handlers_add_item(dp):
    dp.include_router(router_add_item)
