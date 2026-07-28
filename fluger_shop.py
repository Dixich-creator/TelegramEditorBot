ITEMS = {
    1: {
        "name": "👑 КФГ ФЛЮГЕРА",
        "price": 500,
        "item_id": 13
    },

    2: {
        "name": "💰 Денежный буст",
        "price": 100,
        "item_id": 14
    },

    3: {
        "name": "⚔️ Амулет победителя",
        "price": 250,
        "item_id": 15
    },

    4: {
        "name": "🎁 Легендарный кейс",
        "price": 150,
        "item_id": 16
    }
}
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database import (
    get_fluger_item,
    get_fluger_coins,
    remove_fluger_coins,
    add_item
)

router = Router()


@router.message(Command("flugershop"))
async def fluger_shop(message: Message):

    await message.answer(
        """
💎 <b>FLUGER SHOP</b>

━━━━━━━━━━━━━━━━━━

1️⃣ 👑 КФГ ФЛЮГЕРА
💎 Цена: <b>500 FC</b>

📈 +20% шанс победы в дуэлях

━━━━━━━━━━━━━━━━━━

2️⃣ 💰 Денежный буст
💎 Цена: <b>100 FC</b>

Следующий /reward ×2

━━━━━━━━━━━━━━━━━━

3️⃣ ⚔️ Амулет победителя
💎 Цена: <b>250 FC</b>

+15% шанс победы
на 5 дуэлей

━━━━━━━━━━━━━━━━━━

4️⃣ 🎁 Легендарный кейс
💎 Цена: <b>150 FC</b>

Редкий кейс

━━━━━━━━━━━━━━━━━━

Для покупки:

<code>/fbuy ID</code>
""",
        parse_mode="HTML"
    )
@router.message(Command("fbuy"))
async def fbuy(message: Message):

    args = message.text.split()

    if len(args) != 2:

        await message.answer(
            "Использование:\n/fbuy ID"
        )
        return


    try:
        item = int(args[1])

    except:

        await message.answer(
            "❌ ID должен быть числом."
        )
        return


    if item not in ITEMS:

        await message.answer(
            "❌ Такого предмета нет."
        )
        return


    info = ITEMS[item]


    coins = await get_fluger_coins(
        message.from_user.id
    )


    if coins < info["price"]:

        await message.answer(
            "❌ Недостаточно FLUGER COINS"
        )
        return



    # списываем FC

    await remove_fluger_coins(
        message.from_user.id,
        info["price"]
    )


    # добавляем предмет

    await add_item(
        message.from_user.id,
        info["item_id"]
    )


    await message.answer(
        f"""
✅ Покупка успешна!

📦 Получено:

{info["name"]}

💎 Потрачено:

{info["price"]} FC
"""
    )
