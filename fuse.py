from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import random
import asyncio

from database import (
    get_user_item,
    remove_item,
    add_money,
    add_fluger_coins,
    add_item
)

from fluger_items import ITEMS


router = Router()



@router.message(Command("fuse"))
async def fuse(message: Message):

    args = message.text.split()


    if len(args) != 2:

        await message.answer(
            """
❌ Использование:

/fuse ID кейса

Пример:

/fuse 4
"""
        )

        return



    try:

        shop_id = int(args[1])

    except:

        await message.answer(
            "❌ ID должен быть числом."
        )

        return



    # проверяем есть ли такой предмет в магазине

    if shop_id not in ITEMS:

        await message.answer(
            "❌ Такого предмета нет."
        )

        return



    info = ITEMS[shop_id]


    # ID предмета в инвентаре

    item_id = info["item_id"]



    # проверяем наличие предмета

    item = await get_user_item(
        message.from_user.id,
        item_id
    )


    if item is None:

        await message.answer(
            "❌ У вас нет этого предмета."
        )

        return



    # открываем только легендарный кейс

    if shop_id != 4:

        await message.answer(
            "❌ Этот предмет нельзя открыть."
        )

        return



    # удаляем кейс

    await remove_item(
        message.from_user.id,
        item_id
    )



    msg = await message.answer(
        """
🎁 Открываем Легендарный кейс...

🎲 ...
"""
    )


    await asyncio.sleep(2)



    chance = random.randint(
        1,
        100
    )



    # 40% деньги

    if chance <= 40:


        money = random.randint(
            1_000_000,
            10_000_000
        )


        await add_money(
            message.from_user.id,
            money
        )


        await msg.edit_text(
            f"""
🎉 Кейс открыт!

💰 Вы получили:

<b>{money:,} монет</b>
"""
            ,
            parse_mode="HTML"
        )



    # 35% FLUGER COINS

    elif chance <= 75:


        coins = random.randint(
            10,
            100
        )


        await add_fluger_coins(
            message.from_user.id,
            coins
        )


        await msg.edit_text(
            f"""
🎉 Кейс открыт!

💎 Вы получили:

<b>{coins} FLUGER COINS</b>
"""
            ,
            parse_mode="HTML"
        )



    # 15% новый кейс

    elif chance <= 90:


        await add_item(
            message.from_user.id,
            16
        )


        await msg.edit_text(
            """
🔥 УДАЧА!

Вы получили ещё один:

🎁 Легендарный кейс
"""
        )



    # 10% КФГ

    else:


        await add_item(
            message.from_user.id,
            13
        )


        await msg.edit_text(
            """
👑 НЕВЕРОЯТНО!

Вы выбили:

👑 КФГ ФЛЮГЕРА
"""
        )
