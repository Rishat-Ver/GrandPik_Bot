from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Найти")],
        [KeyboardButton(text="Добавить")],
        [KeyboardButton(text="Убрать")]
    ],
    resize_keyboard=True
)