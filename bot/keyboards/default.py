from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти")],
        [KeyboardButton(text="Обновить/Добавить")],
        [KeyboardButton(text="Забрать со склада/продажа")]
    ],
    resize_keyboard=True
)