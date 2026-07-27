from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import (
    get_balance,
    get_shop_item,
    remove_money,
    add_item
)

router = Router()


@router.message(Command("buy"))
async def buy(message: Message):

    print("BUY ЗАПУЩЕН")

    args = message.text.split()

    if len(args) != 2:

        await message.answer(
            "Использование:\n"
            "/buy ID"
        )

        return

    try:
        item_id = int(args[1])

    except ValueError:

        await message.answer("ID должен быть числом.")

        return

    item = await get_shop_item(item_id)
    print("ТОВАР:", item)

    if item is None:

        await message.answer("❌ Такого товара нет.")

        return

    balance = await get_balance(message.from_user.id)
    print("БАЛАНС:", balance)

    if balance < item["price"]:

        await message.answer(
            "❌ Недостаточно денег."
        )

        return

    await remove_money(
        message.from_user.id,
        item["price"]
    )

    await add_item(
        message.from_user.id,
        item_id
    )

    await message.answer(
        f"✅ Вы купили\n\n"
        f"📦 {item['name']}\n"
        f"💰 За {item['price']:,} ₽"
    )
