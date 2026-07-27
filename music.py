@router.message(Command("music"))
async def music(message: Message):

    print("🎵 MUSIC COMMAND WORK")

    await message.answer(
        "🎵 Музыка работает!"
    )
