import random
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

    roll = random.randint(1, 100)

    if roll <= 35:

        money = random.randint(
            5_000_000,
            20_000_000
        )

        await add_money(
            message.from_user.id,
            money
        )

        await message.answer(
            f"💰 Вы получили {money:,}$"
        )

    elif roll <= 60:

        coins = random.randint(
            25,
            100
        )

        await add_fluger_coins(
            message.from_user.id,
            coins
        )

        await message.answer(
            f"💎 Вы получили {coins} FC"
        )

    elif roll <= 75:

        business = random.randint(1, 5)

        await add_business(
            message.from_user.id,
            business
        )

        await message.answer(
            f"🏢 Выпал бизнес №{business}"
        )

    elif roll <= 85:

        await add_item(
            message.from_user.id,
            1
        )

        await message.answer(
            "👑 Выпала КФГ ФЛЮГЕРА"
        )

    elif roll <= 93:

        await add_item(
            message.from_user.id,
            4
        )

        await message.answer(
            "🎁 Выпал ещё один легендарный кейс!"
        )

    elif roll <= 98:

        await add_fluger_coins(
            message.from_user.id,
            500
        )

        await message.answer(
            "💎 ДЖЕКПОТ! 500 FC!"
        )

    else:

        await add_item(
            message.from_user.id,
            9999
        )

        await message.answer(
            "🌟 СЕКРЕТНЫЙ ПРЕДМЕТ!"
        )

    return
