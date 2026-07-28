from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import get_fluger_inventory

router = Router()


@router.message(Command("finventory"))
async def finventory(message: Message):

    items = await get_fluger_inventory(
        message.from_user.id
    )

    if not items:

        await message.answer(
            """
🎒 <b>FLUGER INVENTORY</b>

У вас пока нет предметов.
""",
            parse_mode="HTML"
        )

        return


    text = "🎒 <b>FLUGER INVENTORY</b>\n\n"

    for item in items:

        text += (
            f"{item['name']}"
            f" ×{item['amount']}\n"
        )

    await message.answer(
        text,
        parse_mode="HTML"
    )