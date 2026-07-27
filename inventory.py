from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_inventory


router = Router()


@router.message(Command("inventory"))
async def inventory(message: Message):

    items = await get_inventory(
        message.from_user.id
    )


    if not items:

        await message.answer(
            "🎒 Ваш инвентарь пуст."
        )

        return


    text = (
        "🎒 <b>Ваш инвентарь</b>\n\n"
    )


    for item in items:

        text += (
            f"🆔 {item['item_id']}\n"
            f"📦 {item['name']}\n"
            f"🔢 Количество: {item['amount']}\n\n"
        )


    await message.answer(
        text,
        parse_mode="HTML"
    )