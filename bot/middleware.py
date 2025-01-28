from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class AccessControlMiddleware(BaseMiddleware):
    def __init__(self, whitelist: list[int]):
        super().__init__()
        self.whitelist = whitelist

    async def __call__(self, handler, event, data):
        user_id = None

        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        if user_id not in self.whitelist:
            if isinstance(event, Message):
                await event.answer("Доступ запрещён. Вы не авторизованы для работы с этим ботом.")
            elif isinstance(event, CallbackQuery):
                await event.answer("Доступ запрещён.")
            return

        return await handler(event, data)
