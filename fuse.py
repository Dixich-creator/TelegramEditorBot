from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import (
    get_user_item,
    remove_item
)

router = Router()


@router.message(Command("fuse"))
async def fuse(message: Message):

    args = message.text.split()

    if len(args) != 2:

        await message.answer(
            "Использование:\n"
            "/fuse ID"
        )

        return

    try:

        item_id = int(args[1])

    except:

        await message.answer("❌ Неверный ID.")

        return


    item = await get_user_item(
        message.from_user.id,
        item_id
    )


    if item is None:

        await message.answer(
            "❌ У вас нет такого предмета."
        )

        return


    # КФГ ФЛЮГЕРА
    if item_id == 1:

        await message.answer(
            """
👑 КФГ ФЛЮГЕРА

Этот предмет действует постоянно.

Использовать его не нужно.
"""
        )

        return


    # Денежный буст
    if item_id == 2:

        await remove_item(
            message.from_user.id,
            item_id
        )

        await message.answer(
            """
💰 Денежный буст активирован!

Следующий /reward принесёт ×2 денег.
"""
        )

        return


    # Амулет
    if item_id == 3:

        await remove_item(
            message.from_user.id,
            item_id
        )

        await message.answer(
            """
⚔️ Амулет победителя активирован!

Следующие 5 дуэлей:

+15% шанс победы.
"""
        )

        return


    # Кейс
    if item_id == 4:

        await remove_item(
            message.from_user.id,
            item_id
        )

        await message.answer(
            """
🎁 Легендарный кейс открыт!

(Позже сюда добавим выпадение наград.)
"""
        )

        return