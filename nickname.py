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


    # свой ник
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
<b>{nickname}</b>
""",
            parse_mode="HTML"
        )

        return



    # ник другому пользователю
    if len(args) < 3:

        await message.answer(
            "❌ Использование:\n"
            "/snick ник\n"
            "или\n"
            "/snick @пользователь ник"
        )

        return



    access = await get_access(
        message.from_user.id
    )


    if access < 2:

        await message.answer(
            "❌ У вас нет прав.\n"
            "🛡 Нужно 2+ уровень доступа"
        )

        return



    username = args[1].replace("@", "")

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
✅ Ник изменён

👤 Пользователь:
@{username}

🏷 Новый ник:
<b>{nickname}</b>
""",
        parse_mode="HTML"
    )


@router.message(Command("rnick"))
async def remove_nick(message: Message):

    args = message.text.split()


    # если указан другой пользователь

    if len(args) > 1:

        access = await get_access(
            message.from_user.id
        )


        if access < 2:

            await message.answer(
                "❌ У вас недостаточно прав.\n"
                "🛡 Нужно: 2 уровень доступа"
            )

            return


        target = args[1]


        await remove_nickname(
            target
        )


        await message.answer(
            f"✅ Ник пользователя {target} удалён."
        )

        return



    # удаление своего ника

    await remove_nickname(
        message.from_user.id
    )


    await message.answer(
        "✅ Ваш ник удалён."
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
