from datetime import datetime

from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatMemberStatus

import aiosqlite

from database import DATABASE, set_access

router = Router()


async def add_user(user_id, username):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (
                user_id,
                username,
                joined
            )
            VALUES
            (
                ?, ?, ?
            )
            """,
            (
                user_id,
                username,
                datetime.now().strftime("%d.%m.%Y")
            )
        )

        await db.commit()


@router.my_chat_member()
async def bot_added(event: ChatMemberUpdated):

    print("🤖 Бот добавлен в группу")

    chat = event.chat

    try:
        admins = await chat.get_administrators()

    except Exception as e:
        print(e)
        return


    for admin in admins:

        if admin.status == ChatMemberStatus.CREATOR:

            await add_user(
                admin.user.id,
                admin.user.username
            )

            await set_access(
                admin.user.id,
                4
            )

            print(
                f"👑 {admin.user.full_name} получил 4 уровень доступа"
            )

            break
