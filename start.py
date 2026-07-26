from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def start(message: Message):

    await message.answer(
f"""
👋 Привет, {message.chat.title}!

Спасибо что выбрали нас.

Бот успешно запущен ✅
"""
    )
@router.message(Command("chatid"))
async def chatid(message: Message):

    await message.answer(
        f"ID этой группы:\n{message.chat.id}"
    )