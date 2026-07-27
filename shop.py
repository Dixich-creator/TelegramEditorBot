from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("shop"))
async def shop(message: Message):
    print("SHOP COMMAND")
    await message.answer("✅ Команда /shop работает")
