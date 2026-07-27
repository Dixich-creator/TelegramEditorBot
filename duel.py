from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import random

from database import (
    get_balance,
    remove_money,
    add_money,
    get_inventory
)


router = Router()


# активные дуэли
duels = {}


# проверка КФГ ФЛЮГЕРА
async def has_duel_boost(user_id):

    items = await get_inventory(user_id)

    for item in items:

        if item["item_id"] == 9:
            return True

    return False



# создание дуэли
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




# принятие дуэли
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




    player_balance = await get_balance(
        callback.from_user.id
    )



    if player_balance < amount:


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




    # проверяем КФГ

    challenger_boost = await has_duel_boost(
        duel_id
    )


    player_boost = await has_duel_boost(
        callback.from_user.id
    )




    # выбор победителя

    if challenger_boost:


        winner = random.choices(

            [
                duel_id,
                callback.from_user.id
            ],

            weights=[

                70,
                30

            ]

        )[0]



    elif player_boost:


        winner = random.choices(

            [
                duel_id,
                callback.from_user.id
            ],

            weights=[

                30,
                70

            ]

        )[0]



    else:


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




    boost_text = ""


    if await has_duel_boost(winner):

        boost_text = (

            "\n\n👑 КФГ ФЛЮГЕРА ЗАБУСТИЛООО 🔥"

        )




    await callback.message.edit_text(

        f"""
⚔️ <b>ДУЭЛЬ ОКОНЧЕНА!</b>

🏆 Победитель:
<b>{winner_name}</b>

💰 Получает:
<b>{prize:,}$</b>

🎲 Судьба решила!
{boost_text}
""",

        parse_mode="HTML"

    )



    del duels[duel_id]


    await callback.answer()




# отказ от дуэли
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
