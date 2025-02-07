from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.default import main_keyboard
from database.crud.del_data import update_item_for_delete
from handlers.states import DeleteStates
from checkers.checker_params import chek_params_integer


router_delete_item = Router()



@router_delete_item.message(lambda message: message.text == "Забрать")
async def delete_prompt(message: Message, state: FSMContext):

    await state.clear()

    response = (
        f"Введите данные в формате:\n\n"
        f"артикул␣размер␣колличество\n"
        f"артикул␣размер␣колличество\n"
        f"и т д\n"
        f"---------------------------------"
        )

    await message.answer(response)

    await state.set_state(DeleteStates.waiting_for_delete_input)


@router_delete_item.message(DeleteStates.waiting_for_delete_input)
async def process_delete(message: Message, state: FSMContext):

    result = []

    for item in message.text.split('\n'):

        if len(item.split()) == 3:

            article, size, quantity = item.split()

            check_param = [True if chek_params_integer(param) else False for param in (article, quantity)]
            if not all(check_param):

                result.append(
                    f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                    f"Не корректно ввели данные\n"
                    f"для артикула {article}\n"
                    f"---------------------------------"
                )
                continue

            action, article, quantity, location = update_item_for_delete(article, size, quantity)

            if action == 'updated':
                response = (
                    f"✅\n"
                    f"Панно: {article}  {size}\n\n"
                    f"МЕСТО: {location}\n"
                    f"---------------------------------"
                    )
                result.append(response)

            elif action == "no updated":
                response = (
                    f"❌\n\n"
                    f"Панно: {article}  {size}\n"
                    f"Остаток на сладе: {quantity} шт.\n"
                    f"НА СКЛАДЕ НЕТ СТОЛЬКО ПАННО\n"
                    f"---------------------------------"
                    )
                result.append(response)
            else:
                response = (
                    f"❌\n\n"
                    f"Панно: {article}  {size}\n"
                    f"НЕТ НА СКЛАДЕ !\n"
                    f"---------------------------------"
                )
                result.append(response)

        else:
            response = (
                f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                f"Ошибка: формат ввода неверный.\n"
                f"для артикула {article}\n"
                f"---------------------------------"
            )
            result.append(response)



    await message.answer('\n'.join(result), reply_markup=main_keyboard)

    await state.clear()



def register_handlers_delete_item(dp):
    dp.include_router(router_delete_item)
