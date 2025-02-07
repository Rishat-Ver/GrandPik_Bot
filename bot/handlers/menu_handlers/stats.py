from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.input_file import InputFile
from aiogram.types import BufferedInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import sqlite3
from io import BytesIO
from keyboards.default  import stats_keyboard
from handlers.states import StatsStates


router_stats = Router()

@router_stats.message(Command("stats"))
async def process_start_command(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        text='Статистика:\n\nВыберите , что хотели бы посмотреть',
        reply_markup=stats_keyboard
    )

    await state.set_state(StatsStates.waiting_for_stats_input)


@router_stats.callback_query(F.data == 'Панно VS Продажи')
async def send_sales_stats(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT article, size, SUM(sales) AS sales
        FROM warehouse
        GROUP BY article, size
        ORDER BY sales DESC
        LIMIT 20
    """)

    data = cursor.fetchall()
    connection.close()

    if not data:
        await callback.message.answer("Продаж пока нет.")
        return

    articles = [f"{str(row[0])} {row[1]}" for row in data]
    sales = [int(row[2]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(articles, sales, color="blue")
    plt.title("Статистика продаж Панно")
    plt.xlabel("Панно")
    plt.ylabel("Количество продаж")
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    await callback.message.answer_photo(
        BufferedInputFile(buffer.getvalue(), filename="sales_stats_art_size.png"),
        caption="Топ 20 Панно 📊"
    )

    await callback.message.answer(
        text="\n\nЧто хотите посмотреть дальше?",
        reply_markup=stats_keyboard
    )

    await state.clear()


@router_stats.callback_query(F.data == 'Артикул VS Продажи')
async def send_sales_stats(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT article, SUM(sales) as sales
        FROM warehouse
        GROUP BY article
        ORDER BY sales DESC
        LIMIT 20
    """)
    data = cursor.fetchall()
    connection.close()

    if not data:
        await callback.message.answer("Продаж пока нет.")
        return

    articles = [str(row[0]) for row in data]
    sales = [int(row[1]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(articles, sales, color="green")
    plt.title("Статистика продаж по артикулам")
    plt.xlabel("Артикул")
    plt.ylabel("Количество продаж")
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    await callback.message.answer_photo(
        BufferedInputFile(buffer.getvalue(), filename="sales_stats_art.png"),
        caption="Топ 20 артикул 📊"
    )

    await callback.message.answer(
        text="\n\nЧто хотите посмотреть дальше?",
        reply_markup=stats_keyboard
    )

    await state.clear()


@router_stats.callback_query(F.data == 'Размер VS Продажи')
async def send_sales_stats(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    connection = sqlite3.connect("bot/database/GP_warehouse.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT size, SUM(sales) as sales
        FROM warehouse
        GROUP BY size
        ORDER BY sales DESC
        LIMIT 20
    """)
    data = cursor.fetchall()
    connection.close()

    if not data:
        await callback.message.reply("Продаж пока нет.")
        return

    articles = [str(row[0]) for row in data]
    sales = [int(row[1]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(articles, sales, color="red")
    plt.title("Статистика продаж по размерам")
    plt.xlabel("Размер")
    plt.ylabel("Количество продаж")
    plt.xticks(rotation=45, ha="right")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    await callback.message.answer_photo(
        BufferedInputFile(buffer.getvalue(), filename="sales_stats_size.png"),
        caption="Топ 20 размеров 📊"
    )

    await callback.message.answer(
        text="\n\nЧто хотите посмотреть дальше?",
        reply_markup=stats_keyboard
    )

    await state.clear()


def registr_stats(dp):
    dp.include_router(router_stats)