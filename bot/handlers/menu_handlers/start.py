from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.default import main_keyboard


router_commands = Router()

@router_commands.message(Command(commands='start'))
async def send_keyboard(message: Message):

    user_id = message.from_user.id

    if user_id not in (
        int(os.getenv('ID_IY')),
        int(os.getenv('ID_VR')),
        int(os.getenv('ID_VM')),
        int(os.getenv('ID_RSH')),
        int(os.getenv('ID_LA')),
        int(os.getenv('ID_NA'))
        ):
        await message.answer("У вас нет прав для использования этой функции.", show_alert=True)
        return

    await message.answer(
        "Добро пожаловать в GrandPik bot !",
        reply_markup=main_keyboard
    )

def register_handlers_commands(dp):
    dp.include_router(router_commands)