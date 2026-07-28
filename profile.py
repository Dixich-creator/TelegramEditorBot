from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from database import get_profile



router = Router()



ACCESS_NAMES = {

    1: "Пользователь",

    2: "Модератор",

    3: "Администратор",

    4: "Создатель"

}




@router.message(Command("profile"))
async def profile(message: Message):


    user = await get_profile(
        message.from_user.id
    )


    if user is None:

        await message.answer(
            "❌ Профиль не найден"
        )

        return



    username = user["username"]


    if username:

        username = "@" + username

    else:

        username = "Нет"



    access = user["access"]


    await message.answer(
f"""
👤 Профиль пользователя


🆔 ID:
{user["user_id"]}

👤 Username:
{username}

✏️ Ник:
{user["nickname"] if user["nickname"] else "Нет"}

🥤 Префикс:
{user["prefix"] if user["prefix"] else "Нет"}

🌈 Цвет ника:
{user["nickname_color"]}

🏆 Роль:
{user["role"]}

🔑 Права:
{ACCESS_NAMES.get(access, "Неизвестно")}

💬 Сообщений:
{user["messages"]}

💰 Баланс:
{user["balance"]} ₽

📅 С нами:
{user["joined"]}
"""
    )
