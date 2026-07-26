from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from database import (
    set_nickname,
    remove_nickname,
    get_nicknames,
    get_access,
    get_user_by_username
)


router = Router()



@router.message(Command("snick"))
async def snick(message: Message):

    args = message.text.split(maxsplit=2)


    # обычный пользователь ставит себе

    if len(args) == 2:

        nickname = args[1]


        await set_nickname(
            message.from_user.id,
            nickname
        )


        await message.answer(
f"""
✅ Ник установлен


Ваш ник:

{nickname}
"""
        )

        return



    # проверяем права

    access = await get_access(
        message.from_user.id
    )


    if access < 2:

        await message.answer(
            "❌ У вас нет прав"
        )

        return



    username = args[1].replace("@","")


    nickname = args[2]


    user = await get_user_by_username(
        username
    )


    if user is None:

        await message.answer(
            "❌ Пользователь не найден"
        )

        return



    await set_nickname(
        user["user_id"],
        nickname
    )


    await message.answer(
f"""
✅ Ник установлен


Пользователь:
@{username}


Ник:
{nickname}
"""
    )




@router.message(Command("rnick"))
async def rnick(message: Message):

    args = message.text.split()


    # удаление своего ника

    if len(args) == 1:

        await remove_nickname(
            message.from_user.id
        )


        await message.answer(
            "✅ Ваш ник удалён"
        )

        return



    # удаление чужого ника

    access = await get_access(
        message.from_user.id
    )


    if access < 2:

        await message.answer(
            "❌ У вас нет прав"
        )

        return



    username = args[1].replace("@","")


    user = await get_user_by_username(
        username
    )


    if user is None:

        await message.answer(
            "❌ Пользователь не найден"
        )

        return



    await remove_nickname(
        user["user_id"]
    )


    await message.answer(
f"""
✅ Ник удалён


Пользователь:
@{username}
"""
    )
    await remove_nickname(
        message.from_user.id
    )






@router.message(Command("nlist"))
async def nlist(message: Message):

    users = await get_nicknames()


    if not users:

        await message.answer(
            "📋 Ников пока нет"
        )

        return



    text = "📋 Список ников:\n\n"


    for user in users:

        username = user["username"]

        if username is None:
            username = "без_ника"


        text += f"@{username} — {user['nickname']}\n"



    await message.answer(text)