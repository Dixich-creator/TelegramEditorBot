from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router = Router()
print("🎵 MUSIC MODULE LOADED")


@router.message(Command("music"))
async def music(message: Message):

    print("🎵 MUSIC COMMAND RECEIVED")

    await message.answer(
        "✅ Команда /music работает"
    )
