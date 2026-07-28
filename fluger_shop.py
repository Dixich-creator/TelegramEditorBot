from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

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