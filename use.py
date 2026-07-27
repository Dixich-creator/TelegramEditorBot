from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import use_item

router = Router()


@router.message(Command("use"))
async def use(message: Message):

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "Использование:\n"
            "/use ID"
        )
        return

    try:
        item_id = int(args[1])

    except ValueError:

        await message.answer("ID должен быть числом.")

        return

    item = await use_item(
        message.from_user.id,
        item_id
    )

    if item is None:

        await message.answer(
            "❌ У вас нет такого предмета."
        )

        return

    await message.answer(
        f"✅ Активировано!\n\n"
        f"📦 {item['name']}"
    )