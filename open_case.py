import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import (
    get_item_by_id,
    remove_item,
    add_money,
    add_item
)


router = Router()


@router.message(Command("open"))
async def open_case(message: Message):

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "❌ Использование:\n"
            "/open ID кейса\n\n"
            "Пример:\n"
            "/open 16"
        )
        return


    try:
        item_id = int(args[1])

    except ValueError:

        await message.answer(
            "❌ ID должен быть числом."
        )

        return


    # Ищем предмет по item_id
    case = await get_item_by_id(item_id)


    if case is None:

        await message.answer(
            "❌ Такого предмета нет."
        )

        return


    # Проверяем что это кейс

    if not case["type"].startswith("case_"):

        await message.answer(
            "❌ Этот предмет нельзя открыть."
        )

        return


    # Проверяем наличие кейса у игрока

    removed = await remove_item(
        message.from_user.id,
        item_id
    )


    if not removed:

        await message.answer(
            "❌ У вас нет такого кейса."
        )

        return



    await message.answer(
        "🎁 Открываем кейс...\n\n"
        "⬜⬜⬜⬜⬜"
    )



    # =========================
    # 🎁 КЕЙС FLUGER
    # =========================

    if case["type"] == "case_fluger":


        rewards = [

            {
                "name": "🥤 Префикс ШИПУЧКА",
                "chance": 35,
                "item_id": 4
            },

            {
                "name": "🌪 Префикс ФЛЮГА",
                "chance": 25,
                "item_id": 5
            },

            {
                "name": "🪰 Префикс МУХАА",
                "chance": 20,
                "item_id": 6
            },

            {
                "name": "😈 Префикс ДЕМОН",
                "chance": 15,
                "item_id": 7
            },

            {
                "name": "⚡ КФГ ФЛЮГЕРА",
                "chance": 5,
                "item_id": 8
            }

        ]


        pool = []


        for reward in rewards:

            for _ in range(reward["chance"]):

                pool.append(reward)



        win = random.choice(pool)



        await add_item(
            message.from_user.id,
            win["item_id"]
        )


        await message.answer(
            f"""
🎉 Поздравляем!

🎁 Вам выпало:

{win["name"]}
"""
        )



    # =========================
    # 💰 КЕЙС ДЕНЕГ
    # =========================

    elif case["type"] == "case_money":


        money = random.randint(
            200000,
            1000000
        )


        await add_money(
            message.from_user.id,
            money
        )


        await message.answer(
            f"""
🎉 Поздравляем!

💰 Вы получили:

{money:,} ₽
"""
        )



    # =========================
    # 🏢 БИЗНЕС КЕЙС
    # =========================

    elif case["type"] == "case_business":


        await message.answer(
            """
🏢 Бизнес-кейс открыт!

Система бизнеса ещё не подключена.
"""
        )
