from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import random

from database import (
    get_balance,
    remove_money,
    add_money
)


router = Router()


# ожидающие дуэли
duels = {}


@router.message(Command("duel"))
async def duel(message: Message):

    args = message.text.split()

    if len(args) != 3:
        await message.answer(
            "⚔️ Использование:\n"
            "/duel @игрок сумма"
        )
        return


    opponent = args[1]

    try:
        amount = int(args[2])

    except ValueError:
        await message.answer(
            "❌ Сумма должна быть числом."
        )
        return


    balance = await get_balance(
        message.from_user.id
    )


    if balance < amount:
        await message.answer(
            "❌ У вас недостаточно денег."
        )
        return


    duels[message.from_user.id] = {
        "opponent": opponent,
        "amount": amount,
        "name": message.from_user.full_name
    }


    await message.answer(
        f"""
⚔️ <b>Дуэль создана!</b>

🔥 {message.from_user.full_name}
вызывает {opponent}

💰 Ставка:
<b>{amount:,}$</b>

Чтобы принять:
<code>/accept</code>
""",
        parse_mode="HTML"
    )



@router.message(Command("accept"))
async def accept(message: Message):

    if not duels:

        await message.answer(
            "❌ Нет активных дуэлей."
        )
        return


    duel_id = list(duels.keys())[0]

    duel = duels[duel_id]


    amount = duel["amount"]


    challenger_balance = await get_balance(
        duel_id
    )


    if challenger_balance < amount:

        await message.answer(
            "❌ У игрока уже нет денег."
        )

        del duels[duel_id]

        return


    accept_balance = await get_balance(
        message.from_user.id
    )


    if accept_balance < amount:

        await message.answer(
            "❌ У вас недостаточно денег."
        )

        return



    # снимаем ставки

    await remove_money(
        duel_id,
        amount
    )


    await remove_money(
        message.from_user.id,
        amount
    )


    # победитель

    winner = random.choice(
        [
            duel_id,
            message.from_user.id
        ]
    )


    prize = amount * 2


    await add_money(
        winner,
        prize
    )


    if winner == duel_id:
        winner_name = duel["name"]

    else:
        winner_name = message.from_user.full_name



    await message.answer(
        f"""
⚔️ <b>ДУЭЛЬ ЗАКОНЧЕНА!</b>

🔥 Победитель:
<b>{winner_name}</b>

💰 Приз:
<b>{prize:,}$</b>

🎲 Удача решила судьбу!
""",
        parse_mode="HTML"
    )


    del duels[duel_id]