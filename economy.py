COIN_PRICE = 500000
BUSINESSES = {
    1: {"name": "Ларёк", "price": 50000, "income": 500},
    2: {"name": "Кафе", "price": 250000, "income": 2500},
    3: {"name": "Автомойка", "price": 750000, "income": 8000},
    4: {"name": "Заправка", "price": 2500000, "income": 25000},
    5: {"name": "Автосалон", "price": 10000000, "income": 120000},
}
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import get_business_info

import random
WIN_MESSAGES = [
    "🔥 КФГ ФЛЮГЕРА ЗАБУСТИИИЛ/АААААА МУХАААА",
    "😂 ЫЫЫЫЫЫ ФЛЮГА БУСТИТ!",
    "⚡ ШИПУЧКААААААА!",
    "🥤 ДЕЛЬТААААААА!",
    "🚀 КФГ ФЛЮГЕРААААА!"
]

LOSE_MESSAGES = [
    "😭 Несправидливооо...",
    "😢 ЫЫЫЫЫЫЫЫ...",
    "💔 Не повезло...",
    "🤣 МУХАААААА...",
    "🪦 Денег больше нет..."
]
SLOTS = [
    "🍒",
    "🍋",
    "🍇",
    "💎",
    "⭐",
    "7️⃣"
]
import time
import asyncio


from database import get_balance, add_money


from database import (
    get_balance,
    add_money,
    remove_money,
    add_business,
    get_reward_time,
    set_reward_time,
    get_fluger_coins,
    add_fluger_coins
)


router = Router()


# КД награды (24 часа)
REWARD_COOLDOWN = 24 * 60 * 60


# хранение времени получения награды
reward_users = {}



@router.message(Command("balance"))
async def balance(message: Message):

    money = await get_balance(
        message.from_user.id
    )

    await message.answer(
        f"💳 <b>Ваш баланс</b>\n\n"
        f"💰 {money:,}$",
        parse_mode="HTML"
    )
@router.message(Command("reward"))
async def reward(message: Message):

    user_id = message.from_user.id

    reward = await get_reward_time(user_id)

    now = int(time.time())

    # 24 часа в секундах
    cooldown = 24 * 60 * 60


    if reward:

        last = reward[0]

        if now - last < cooldown:

            left = cooldown - (now - last)

            hours = left // 3600
            minutes = (left % 3600) // 60

            await message.answer(
                f"⏳ Вы уже получали награду.\n\n"
                f"Следующая через: "
                f"{hours}ч {minutes}мин"
            )

            return


    amount = random.randint(
        100000,
        500000
    )


    await add_money(
        user_id,
        amount
    )


    await set_reward_time(
        user_id
    )


    balance = await get_balance(
        user_id
    )


    await message.answer(
        f"🎁 <b>Награда получена!</b>\n\n"
        f"💰 +{amount:,}$\n\n"
        f"💳 Баланс: {balance:,}$",
        parse_mode="HTML"
    )
@router.message(Command("biz"))
async def biz(message: Message):

    businesses = await get_business_info(
        message.from_user.id
    )

    count = len(businesses)

    total_balance = 0
    total_income = 0

    for business in businesses:
        total_balance += business["balance"]
        total_income += business["income"]

    text = (
        "🏢 <b>Ваш бизнес</b>\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        f"📦 Количество бизнесов: <b>{count}</b>\n\n"
        f"💰 Баланс бизнеса: <b>{total_balance:,}₽</b>\n\n"
        f"📈 Доход в час: <b>{total_income:,}₽</b>\n\n"
        "━━━━━━━━━━━━━━━━"
    )

    await message.answer(
        text,
        parse_mode="HTML"
    )
@router.message(Command("buybiz"))
async def buybiz(message: Message):

    args = message.text.split()

    # Показываем магазин
    if len(args) == 1:

        text = "🏢 <b>Магазин бизнесов</b>\n\n"

        for number, biz in BUSINESSES.items():

            text += (
                f"{number}️⃣ <b>{biz['name']}</b>\n"
                f"💰 Цена: {biz['price']:,}$\n"
                f"📈 Доход: {biz['income']:,}$/час\n\n"
            )

        text += (
            "━━━━━━━━━━━━━━━━━━\n"
            "Для покупки используйте:\n"
            "<code>/buybiz номер</code>"
        )

        await message.answer(text, parse_mode="HTML")
        return

    # Покупка бизнеса
    try:
        number = int(args[1])
    except ValueError:
        await message.answer("❌ Укажите номер бизнеса.")
        return

    if number not in BUSINESSES:
        await message.answer("❌ Такого бизнеса нет.")
        return

    biz = BUSINESSES[number]

    balance = await get_balance(message.from_user.id)

    if balance < biz["price"]:
        await message.answer("❌ Недостаточно денег.")
        return

    await remove_money(
        message.from_user.id,
        biz["price"]
    )

    await add_business(
        message.from_user.id,
        biz["name"],
        biz["income"]
    )

    await message.answer(
        f"✅ Вы успешно купили бизнес!\n\n"
        f"🏢 {biz['name']}\n"
        f"💰 Стоимость: {biz['price']:,}$\n"
        f"📈 Доход: {biz['income']:,}$/час"
    )
@router.message(Command("snitbiz"))
async def take_business(message: Message):

    money = await collect_business_money(
        message.from_user.id
    )

    if money <= 0:
        await message.answer(
            "❌ На балансе бизнеса нет денег."
        )
        return


    await add_money(
        message.from_user.id,
        money
    )


    await message.answer(
        f"🏢 Вы сняли прибыль с бизнеса!\n\n"
        f"💰 Получено: {money:,}$\n"
        f"✅ Деньги переведены на ваш баланс"
    )
@router.message(Command("roulette"))
async def roulette(message: Message):

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "🎰 Использование:\n"
            "/roulette сумма"
        )
        return

    try:
        amount = int(args[1])

    except ValueError:
        await message.answer(
            "❌ Укажите число."
        )
        return

    if amount <= 0:
        await message.answer(
            "❌ Ставка должна быть больше 0."
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

    # снимаем ставку
    await remove_money(
        message.from_user.id,
        amount
    )

    chance = random.randint(1, 100)

    if chance <= 45:

        win = amount * 2

        await add_money(
            message.from_user.id,
            win
        )

        await message.answer(
            f"""
🎰 <b>Рулетка</b>

💰 Ставка: {amount:,}$

🎉 Победа!
💵 Вы получили: {win:,}$

{random.choice(WIN_MESSAGES)}
""",
            parse_mode="HTML"
        )

    else:

        await message.answer(
            f"""
🎰 <b>Рулетка</b>

💰 Ставка: {amount:,}$

💥 Вы проиграли!

{random.choice(LOSE_MESSAGES)}
""",
            parse_mode="HTML"
        )
@router.message(Command("casino"))
async def casino(message: Message):

    args = message.text.split()

    if len(args) != 2:
        await message.answer(
            "Использование:\n"
            "/casino сумма"
        )
        return

    try:
        bet = int(args[1])
    except ValueError:
        await message.answer("Введите число.")
        return

    if bet <= 0:
        await message.answer("Ставка должна быть больше 0.")
        return

    balance = await get_balance(message.from_user.id)

    if balance < bet:
        await message.answer("❌ Недостаточно денег.")
        return

    await remove_money(message.from_user.id, bet)

    msg = await message.answer("🎰 Крутим автомат...")

    await asyncio.sleep(2)

    a = random.choice(SLOTS)
    b = random.choice(SLOTS)
    c = random.choice(SLOTS)

    text = (
        "🎰 <b>Игровой автомат</b>\n\n"
        f"{a} | {b} | {c}\n\n"
    )

    if a == b == c:

        win = bet * 5

        await add_money(message.from_user.id, win)

        text += (
            "🔥 <b>ДЖЕКПОТ!!</b>\n\n"
            f"💰 Вы выиграли {win:,}$\n\n"
            f"{random.choice(WIN_MESSAGES)}"
        )

    elif a == b or b == c or a == c:

        win = bet * 2

        await add_money(message.from_user.id, win)

        text += (
            "✨ Два одинаковых!\n\n"
            f"💰 Вы выиграли {win:,}$\n\n"
            f"{random.choice(WIN_MESSAGES)}"
        )

    else:

        text += (
            "💥 Проигрыш!\n\n"
            f"{random.choice(LOSE_MESSAGES)}"
        )

    await msg.edit_text(
        text,
        parse_mode="HTML"
    )
@router.message(Command("coins"))
async def coins(message: Message):

    coins = await get_fluger_coins(
        message.from_user.id
    )

    await message.answer(
        f"""
💎 <b>FLUGER COINS</b>

Баланс:
<b>{coins} FC</b>
""",
        parse_mode="HTML"
    )
@router.message(Command("buycoin"))
async def buycoin(message: Message):

    args = message.text.split()

    if len(args) != 2:

        await message.answer(
            "Использование:\n"
            "/buycoin количество"
        )

        return


    try:

        amount = int(args[1])

    except:

        await message.answer(
            "❌ Введите число."
        )

        return


    if amount <= 0:

        await message.answer(
            "❌ Количество должно быть больше 0."
        )

        return


    price = amount * COIN_PRICE


    balance = await get_balance(
        message.from_user.id
    )


    if balance < price:

        await message.answer(
            f"""
❌ Недостаточно денег.

Нужно:

{price:,}$
"""
        )

        return


    await remove_money(
        message.from_user.id,
        price
    )


    await add_fluger_coins(
        message.from_user.id,
        amount
    )


    coins = await get_fluger_coins(
        message.from_user.id
    )


    await message.answer(
        f"""
💎 Покупка успешна!

Получено:

+{amount} FC

Потрачено:

-{price:,}$

━━━━━━━━━━━━━━

💎 Ваш баланс:

{coins} FC
"""
    )
