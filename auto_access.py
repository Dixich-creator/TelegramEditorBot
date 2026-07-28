from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatMemberStatus

from database import add_user, set_access


router = Router()


@router.my_chat_member()
async def bot_added(event: ChatMemberUpdated):

    # Проверяем, что бот добавили в группу

    if event.new_chat_member.status not in [
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR
    ]:
        return


    chat = event.chat


    try:

        admins = await chat.get_administrators()

    except Exception:

        return



    for admin in admins:

    if admin.status == ChatMemberStatus.CREATOR:

        await add_user(
            admin.user.id,
            admin.user.username,
            admin.user.full_name
        )

        await set_access(
            admin.user.id,
            4
        )

        print(
            f"👑 {admin.user.full_name} получил 4 уровень"
        )

        break
