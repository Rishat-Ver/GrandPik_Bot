from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from middleware import AccessControlMiddleware
from dotenv import load_dotenv

import asyncio
import os
from handlers import search, add, delete, moving
from handlers.menu_handlers import start, stats, export_db, sql_requests


load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

WHITELIST = [
    int(os.getenv('ID_VR')),
    int(os.getenv('ID_IY')),
    int(os.getenv('ID_LA')),
    int(os.getenv('ID_NA')),
    int(os.getenv('ID_RSH')),
    int(os.getenv('ID_VM'))
]

dp.message.middleware(AccessControlMiddleware(WHITELIST))
dp.callback_query.middleware(AccessControlMiddleware(WHITELIST))


start.register_handlers_commands(dp)
stats.registr_stats(dp)
export_db.registr_export(dp)
sql_requests.registr_sql(dp)


search.register_handlers_search(dp)
add.register_handlers_add_item(dp)
moving.register_handlers_update_item(dp)
delete.register_handlers_delete_item(dp)


async def set_main_menu(bot: Bot):

    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="stats", description="Выберите какую статистику хотите посмотреть 📈📉"),
        BotCommand(command="export", description="Выгрузить базу в exel 📜"),
        BotCommand(command="sql", description="Сделать запрос в БД"),

    ]
    await bot.set_my_commands(commands)


async def main():
    await set_main_menu(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
