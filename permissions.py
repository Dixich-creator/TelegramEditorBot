from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from database import (
    get_access,
    get_user_by_username
)


router = Router()



ACCESS_NAMES = {
    1: "Пользователь",
    2: "Модератор",
    3: "Администратор",
    4: "Создатель"
}



@router.message(Command("setaccess"))
async def set_access_command(message: Message):

    # проверяем права того, кто выдает

    my_access = await get_access(
        message.from_user.id
    )


    if my_access < 4:

        await message.answer(
            "❌ Только Создатель может выдавать права"
        )

        return



    args = message.text.split()


    if len(args) != 3:

        await message.answer(
            """
Использование:

/setaccess @username уровень

Пример:

/setaccess @user 2
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



    if level not in [1,2,3,4]:

        await message.answer(
            "❌ Уровень только от 1 до 4"
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



    await change_access(
        user["user_id"],
        level
    )


    await message.answer(
f"""
✅ Права изменены


👤 Пользователь:

@{username}


🔑 Новый уровень:

{level} — {ACCESS_NAMES[level]}
"""
    )



async def change_access(user_id, level):

    import aiosqlite

    from database import DATABASE


    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            UPDATE users

            SET access=?

            WHERE user_id=?
            """,
            (
                level,
                user_id
            )
        )


        await db.commit()