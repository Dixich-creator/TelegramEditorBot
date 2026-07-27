import random

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import (
    get_shop_item,
    remove_item,
    add_money,
    add_item,
    set_access
)

router = Router()


@router.message(Command("open"))
async def open_case(message: Message):

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "Использование:\n"
            "/open ID кейса"
        )
        return


    try:
        case_id = int(args[1])

    except ValueError:
        await message.answer(
            "❌ ID должен быть числом."
        )
        return


    case = await get_shop_item(case_id)


    if case is None:
        await message.answer(
            "❌ Такого кейса нет."
        )
        return


    if not case["type"].startswith("case_"):
        await message.answer(
            "❌ Это не кейс."
        )
        return


    # проверяем наличие кейса
    removed = await remove_item(
        message.from_user.id,
        case_id
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


    # =====================
    # Кейс FLUGER
    # =====================

    if case["type"] == "case_fluger":

        rewards = [
            ("🥤 ШИПУЧКА", 35),
            ("🌪 ФЛЮГА", 25),
            ("🪰 МУХАА", 20),
            ("😈 ДЕМОН", 15),
            ("⚡ КФГ ФЛЮГЕРА", 5)
        ]


        names = []

        for name, chance in rewards:
            names += [name] * chance


        reward = random.choice(names)
        await add_item(
            message.from_user.id,
            rewards.index((reward, next(chance for name, chance in rewards if name == reward))) + 4
        )


        await message.answer(
            f"🎉 Поздравляем!\n\n"
            f"🏆 Выпало:\n"
            f"{reward}"
        )


    # =====================
    # Кейс денег
    # =====================

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
            f"🎉 Вам выпало:\n\n"
            f"💰 {money:,} ₽"
        )


    # =====================
    # Бизнес кейс
    # =====================

    elif case["type"] == "case_business":

        await message.answer(
            "🏢 Вам выпал бизнес!\n\n"
            "Пока система бизнеса будет добавлена следующим шагом."
        )
