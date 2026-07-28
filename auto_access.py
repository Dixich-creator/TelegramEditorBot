from aiogram import Router
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatMemberStatus

from database import add_user, set_access

router = Router()


@router.my_chat_member()
async def bot_added(event: ChatMemberUpdated):

    print("🤖 Сработал auto_access")

    # Бот должен быть добавлен в группу
    if event.new_chat_member.status not in (
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
    ):
        return

    try:
        admins = await event.chat.get_administrators()
    except Exception as e:
        print(f"Ошибка получения администраторов: {e}")
        return

    for admin in admins:

        # Ищем владельца группы
        if admin.status == ChatMemberStatus.CREATOR:

            # Добавляем владельца в базу, если его ещё нет
            await add_user(
                admin.user.id,
                admin.user.username
            )

            # Выдаём 4 уровень доступа
            await set_access(
                admin.user.id,
                4
            )

            print(
                f"👑 {admin.user.full_name} получил 4 уровень доступа"
            )

            break
