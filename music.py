from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router = Router()


@router.message(Command("music"))
async def music(message: Message):

    audio = FSInputFile("music/Кишлак - Самый Лучший День.mp3")

    await message.answer_audio(
        audio=audio,
        title="Fluger Music",
        performer="Fluger New",
        caption="🎵 Приятного прослушивания!"
    )