from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import asyncio
import os
from handlers import search, commands, load_dump_warehouse, add, delete
from keyboards.default import main_keyboard


load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

commands.register_handlers_commands(dp)
load_dump_warehouse.register_handlers_load_warehouse(dp)
search.register_handlers_search(dp)
add.register_handlers_add_item(dp)
delete.register_handlers_delete_item(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
