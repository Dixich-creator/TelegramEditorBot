from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import random

from database import (
    get_balance,
    remove_money,
    add_money
)


router = Router()


# активные дуэли
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
            "❌ Недостаточно денег."
        )
        return


    duels[message.from_user.id] = {
        "opponent": opponent,
        "amount": amount,
        "name": message.from_user.full_name
    }


    keyboard = InlineKeyboardBuilder()


    keyboard.button(
        text="✅ Принять",
        callback_data=f"accept_duel:{message.from_user.id}"
    )


    keyboard.button(
        text="❌ Отказаться",
        callback_data=f"cancel_duel:{message.from_user.id}"
    )


    await message.answer(
        f"""
⚔️ <b>ДУЭЛЬ!</b>

🔥 {message.from_user.full_name}
вызывает {opponent}

💰 Ставка:
<b>{amount:,}$</b>

Принять бой?
""",
        parse_mode="HTML",
        reply_markup=keyboard.as_markup()
    )



@router.callback_query(lambda c: c.data.startswith("accept_duel"))
async def accept_duel(callback: CallbackQuery):


    duel_id = int(
        callback.data.split(":")[1]
    )


    if duel_id not in duels:

        await callback.answer(
            "❌ Дуэль уже закончена",
            show_alert=True
        )

        return



    duel = duels[duel_id]

    amount = duel["amount"]


    balance = await get_balance(
        callback.from_user.id
    )


    if balance < amount:

        await callback.answer(
            "❌ У вас нет денег",
            show_alert=True
        )

        return



    await remove_money(
        duel_id,
        amount
    )


    await remove_money(
        callback.from_user.id,
        amount
    )


    winner = random.choice(
        [
            duel_id,
            callback.from_user.id
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
        winner_name = callback.from_user.full_name



    await callback.message.edit_text(
        f"""
⚔️ <b>ДУЭЛЬ ОКОНЧЕНА!</b>

🏆 Победитель:
<b>{winner_name}</b>

💰 Получает:
<b>{prize:,}$</b>

🎲 Удача решила судьбу!
""",
        parse_mode="HTML"
    )


    del duels[duel_id]


    await callback.answer()



@router.callback_query(lambda c: c.data.startswith("cancel_duel"))
async def cancel_duel(callback: CallbackQuery):

    duel_id = int(
        callback.data.split(":")[1]
    )


    if duel_id in duels:

        del duels[duel_id]


    await callback.message.edit_text(
        "❌ Дуэль отменена."
    )


    await callback.answer()
