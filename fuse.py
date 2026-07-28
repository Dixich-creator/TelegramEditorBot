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
    add_item,
    add_business
)


router = Router()


@router.message(Command("fuse"))
async def fuse(message: Message):

    args = message.text.split()


    if len(args) != 14:

        await message.answer(
            """
❌ Использование:

/fuse ID предмета

Пример:
/fuse 4
"""
        )

        return



    try:

        item_id = int(args[1])

    except ValueError:

        await message.answer(
            "❌ ID должен быть числом."
        )

        return



    item = await get_user_item(
        message.from_user.id,
        item_id
    )


    if item is None:

        await message.answer(
            "❌ У вас нет этого предмета."
        )

        return



    # ==========================
    # ЛЕГЕНДАРНЫЙ КЕЙС
    # ==========================

    if item_id == 16:


        await remove_item(
            message.from_user.id,
            item_id
        )


        msg = await message.answer(
            """
🎁 Открываем легендарный кейс...

🎲 ...
"""
        )


        await asyncio.sleep(1)


        await msg.edit_text(
            """
🎁 Открываем легендарный кейс...

🎲 ........
"""
        )


        await asyncio.sleep(1)



        roll = random.randint(
            1,
            100
        )



        # 35% деньги

        if roll <= 35:


            money = random.randint(
                5_000_000,
                20_000_000
            )


            await add_money(
                message.from_user.id,
                money
            )


            await msg.edit_text(
                f"""
✨ НАГРАДА НАЙДЕНА!

💰 Вы получили:

<b>{money:,}$</b>
"""
            )



        # 25% fluger coins

        elif roll <= 60:


            coins = random.randint(
                25,
                100
            )


            await add_fluger_coins(
                message.from_user.id,
                coins
            )


            await msg.edit_text(
                f"""
✨ НАГРАДА НАЙДЕНА!

💎 Вы получили:

<b>{coins} FLUGER COINS</b>
"""
            )



        # 15% бизнес

        elif roll <= 75:


            business_id = random.randint(
                1,
                5
            )


            await add_business(
                message.from_user.id,
                business_id
            )


            await msg.edit_text(
                f"""
✨ НАГРАДА НАЙДЕНА!

🏢 Вы получили бизнес:

<b>№{business_id}</b>
"""
            )



        # 10% КФГ ФЛЮГЕРА

        elif roll <= 85:


            await add_item(
                message.from_user.id,
                1
            )


            await msg.edit_text(
                """
👑 НЕВЕРОЯТНО!

Выпал:

<b>КФГ ФЛЮГЕРА</b>

🔥 Теперь у вас особый предмет!
"""
            )



        # 13% ещё кейс

        elif roll <= 98:


            await add_item(
                message.from_user.id,
                4
            )


            await msg.edit_text(
                """
🎁 ВЫПАЛО ЕЩЁ!

Вы получили:

<b>Легендарный кейс</b>
"""
            )



        # 2% джекпот

        else:


            await add_fluger_coins(
                message.from_user.id,
                500
            )


            await msg.edit_text(
                """
💎💎💎 ДЖЕКПОТ!!!

Вы выбили:

<b>500 FLUGER COINS</b>

🔥 Это очень редкая награда!
"""
            )


        return



    # ==========================
    # КФГ ФЛЮГЕРА
    # ==========================

    if item_id == 13:


        await message.answer(
            """
👑 КФГ ФЛЮГЕРА

Этот предмет постоянный.

Он помогает в дуэлях.
Использовать не нужно.
"""
        )


        return



    # ==========================
    # ДЕНЕЖНЫЙ БУСТ
    # ==========================

    if item_id == 14:


        await remove_item(
            message.from_user.id,
            item_id
        )


        await message.answer(
            """
💰 Денежный буст активирован!

Следующая награда будет увеличена.
"""
        )


        return



    # ==========================
    # АМУЛЕТ ДУЭЛЕЙ
    # ==========================

    if item_id == 15:


        await remove_item(
            message.from_user.id,
            item_id
        )


        await message.answer(
            """
⚔️ Амулет победителя активирован!

Шанс победы в дуэлях увеличен.
"""
        )


        return
