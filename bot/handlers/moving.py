from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.default import main_keyboard
from database.crud.update import update_location
from handlers.states import MovingStates
from checkers.checker_params import chek_params_integer


router_moving_item = Router()


@router_moving_item.message(lambda message: message.text == "Переместить")
async def add_prompt(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        f"Введите данные в формате:\n\n"
        f"артикул␣размер␣␣место\n",
        parse_mode='Markdown'
    )
    await state.set_state(MovingStates.waiting_for_moving_input)


@router_moving_item.message(MovingStates.waiting_for_moving_input)
async def process_add(message: Message, state: FSMContext):

    if len(message.text.split()) == 3:

        article, size, location = message.split()

        check_param = [True if chek_params_integer(param) else False for param in (article, location)]

        if not all(check_param):

            await message.answer(
                f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
                f"Не корректно ввели данные\n",
                parse_mode='Markdown'
            )
            return

        article, size, location = update_location(article, size, location)

        await message.answer(
            f"Перемещение панно ✅\n\n"
            f"Панно: {article} {size}\n"
            f"Новое МЕСТО: {location}\n",
            parse_mode='Markdown'
        )

    else:
        await message.answer(
            f"❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️❗️\n"
            f"Не корректно ввели данные\n",
            parse_mode='Markdown'
        )
        return

    await state.clear()


def register_handlers_update_item(dp):
    dp.include_router(router_moving_item)