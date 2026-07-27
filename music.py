from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

router = Router()

print("🎵 MUSIC MODULE LOADED")


@router.message(Command("music"))
async def music(message: Message):

    print("🎵 MUSIC COMMAND WORK")

    # отправляем кружок
    video = FSInputFile(
        "media/video.mp4"
    )

    await message.answer_video_note(
        video_note=video
    )


    # отправляем песню
    audio = FSInputFile(
        "media/fluger.mp3"
    )

    await message.answer_audio(
        audio=audio,
        title="Fluger Music",
        performer="Fluger New",
        caption="🎵 Приятного прослушивания!"
    )
