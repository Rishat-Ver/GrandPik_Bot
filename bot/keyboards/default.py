from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить"), KeyboardButton(text="Переместить"), KeyboardButton(text="🔍"), KeyboardButton(text="Забрать")],
    ],
    resize_keyboard=True
)

button_1 = InlineKeyboardButton(
    text='Артикул',
    callback_data='Артикул VS Продажи'
)

button_2 = InlineKeyboardButton(
    text='Панно',
    callback_data='Панно VS Продажи'
)

button_3 = InlineKeyboardButton(
    text='Размер',
    callback_data='Размер VS Продажи'
)

stats_keyboard =InlineKeyboardMarkup(
    inline_keyboard=[[button_1, button_2, button_3]]
)
