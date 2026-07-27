from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_shop

router = Router()


@router.message(Command("shop"))
async def shop(message: Message):

    items = await get_shop()

    if not items:
        await message.answer("❌ Магазин пуст.")
        return

    text = "🛒 <b>Магазин</b>\n\n"

    for item in items:

        text += (
            f"🆔 {item['id']}\n"
            f"📦 {item['name']}\n"
            f"💰 Цена: {item['price']:,} ₽\n\n"
        )

    text += (
        "━━━━━━━━━━━━━━\n"
        "Для покупки:\n"
        "<code>/buy ID</code>"
    )

    await message.answer(
        text,
        parse_mode="HTML"
    )