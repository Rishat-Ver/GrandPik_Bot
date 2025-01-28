from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.default import main_keyboard


router_commands = Router()

@router_commands.message(Command(commands='start'))
async def send_keyboard(message: Message):

    await message.answer(
        "Добро пожаловать в GrandPik bot !",
        reply_markup=main_keyboard
    )

def register_handlers_commands(dp):
    dp.include_router(router_commands)