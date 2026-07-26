from aiogram import Router
from aiogram.types import ChatMemberUpdated

from database import is_banned, is_tempbanned

router = Router()


@router.chat_member()
async def user_join(event: ChatMemberUpdated):

    # Пользователь вступил в группу
    if (
        event.old_chat_member.status in ("left", "kicked")
        and event.new_chat_member.status == "member"
    ):

        user = event.new_chat_member.user

        banned = await is_banned(user.id)

        tempbanned = await is_tempbanned(user.id)


        if banned or tempbanned:

            await event.bot.ban_chat_member(
                chat_id=event.chat.id,
                user_id=user.id
            )

            await event.bot.send_message(
                event.chat.id,
                f"🚫 Пользователь @{user.username if user.username else user.full_name} пытался зайти, но находится в бане."
            )