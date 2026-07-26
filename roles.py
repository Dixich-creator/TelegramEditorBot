from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from database import (
    get_access,
    get_user_by_username,
    set_role
)


router = Router()



ROLES = {

    1: "Новый эдитор",

    2: "Проверенный эдитор",

    3: "Истинный эдитор",

    4: "Лучший эдитор",

    5: "Великий эдитор"

}



@router.message(Command("setrole"))
async def setrole(message: Message):


    access = await get_access(
        message.from_user.id
    )


    if access < 3:

        await message.answer(
            "❌ Недостаточно прав"
        )

        return



    args = message.text.split()


    if len(args) != 3:

        await message.answer(
"""
Использование:

/setrole @username уровень

Пример:

/setrole @user 5
"""
        )

        return



    username = args[1].replace("@","")



    try:

        level = int(args[2])

    except:

        await message.answer(
            "❌ Уровень должен быть числом"
        )

        return



    if level not in ROLES:

        await message.answer(
            "❌ Роль только от 1 до 5"
        )

        return



    user = await get_user_by_username(
        username
    )


    if user is None:

        await message.answer(
            "❌ Пользователь не найден"
        )

        return



    await set_role(
        user["user_id"],
        ROLES[level]
    )


    await message.answer(
f"""
✅ Роль изменена


👤 Пользователь:

@{username}


🏆 Новая роль:

{ROLES[level]}
"""
    )