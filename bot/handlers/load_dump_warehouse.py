from aiogram import Router
from aiogram.types import Message, ContentType
from aiogram import F
from aiogram.fsm.context import FSMContext

from keyboards.default import main_keyboard
from database.dump_warehouse import load_data_from_excel

router_load_warehouse = Router()

@router_load_warehouse.message(F.content_type==ContentType.DOCUMENT)
async def handle_document(message: Message, state: FSMContext):
    
    file_id = message.document.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    file_name = message.document.file_name
    file = await message.bot.download_file(file_path)

    with open(file_name, 'wb') as new_file:
        new_file.write(file.getvalue())

    db_path = "bot/database/GP_warehouse.db"
    load_data_from_excel(file_name, db_path)

    await message.answer("Данные загружены в базу данных.", reply_markup=main_keyboard)

def register_handlers_load_warehouse(dp):
    dp.include_router(router_load_warehouse)
