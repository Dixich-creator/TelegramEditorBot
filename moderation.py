import random
MUTE_MESSAGES = [
    "🔇 ЫЫЫЫЫ ШИПУЧКЭЭЭЭЭ 😭",
    " Несправедливоооооо",
    "😂 ЫЫЫЫЫ ДЕЛЬТА БУСТИТ!",
    "🤣 ЫЫЫЫ ВКИСАЙТ БУСТИИИИТ!"
]
from aiogram import Router
from logs import send_log
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from datetime import datetime, timedelta
from aiogram.types import ChatPermissions
from database import remove_mute, get_user_by_username, get_access
from database import add_ban
from database import remove_ban
import time
from database import (
    remove_mute,
    get_user_by_username,
    get_access,
    add_ban,
    remove_ban,
    add_tempban,
    remove_tempban,
    add_mute,
    get_mute,
    set_access,
    get_bans,
    get_tempbans,
    get_staff,
    add_money
)

router = Router()


@router.message(Command("mute"))
async def mute(message: Message):

    access = await get_access(message.from_user.id)

    if access < 2:
        await message.answer("❌ У вас недостаточно прав.")
        return

    target = None
    username = None

    # ---------- Вариант 1: Ответ на сообщение ----------
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        args = message.text.split(maxsplit=2)

        if len(args) < 3:
            await message.answer(
                "Использование:\n"
                "/mute <минуты> <причина>\n\n"
                "Пример:\n"
                "/mute 10 Флуд"
            )
            return

        try:
            minutes = int(args[1])
        except ValueError:
            await message.answer("❌ Минуты должны быть числом.")
            return

        reason = args[2]

    # ---------- Вариант 2: Через @username ----------
    else:

        args = message.text.split(maxsplit=3)

        if len(args) < 4:
            await message.answer(
                "Использование:\n"
                "/mute @username <минуты> <причина>"
            )
            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:
            await message.answer("❌ Пользователь не найден.")
            return

        target = user

        try:
            minutes = int(args[2])
        except ValueError:
            await message.answer("❌ Минуты должны быть числом.")
            return

        reason = args[3]

    until = datetime.now() + timedelta(minutes=minutes)

    # Ограничиваем пользователя
    await message.bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=target.id if hasattr(target, "id") else target["user_id"],
        permissions=ChatPermissions(
            can_send_messages=False
        ),
        until_date=until
    )

    await add_mute(
        target.id if hasattr(target, "id") else target["user_id"],
        int(until.timestamp()),
        reason
    )

    name = (
        target.full_name
        if hasattr(target, "full_name")
        else f"@{username}"
    )

    await message.answer(
        f"🔇 Пользователь {name} получил мут.\n\n"
        f"⏳ Срок: {minutes} минут\n"
        f"📝 Причина: {reason}\n\n"
        f"{random.choice(MUTE_MESSAGES)}"
    )

    await send_log(
        message.bot,
        "Выдан мут",
        message.from_user.full_name,
        name,
        reason
    )
@router.message(Command("unmute"))
async def unmute(message: Message):

    access = await get_access(message.from_user.id)

    if access < 2:
        await message.answer("❌ У вас недостаточно прав.")
        return

    # По ответу на сообщение
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        user_id = target.id
        name = target.full_name

    # По @username
    else:

        args = message.text.split()

        if len(args) != 2:

            await message.answer(
                "Использование:\n"
                "/unmute @username\n\n"
                "или ответьте на сообщение пользователя:\n"
                "/unmute"
            )

            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:

            await message.answer("❌ Пользователь не найден.")

            return

        user_id = user["user_id"]
        name = f"@{username}"

    # Снимаем ограничения
    await message.bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_invite_users=True
        )
    )

    # Удаляем запись из базы
    await remove_mute(user_id)

    await message.answer(
        f"🔊 Пользователь {name} больше не находится в муте."
    )
@router.message(Command("ban"))
async def ban(message: Message):

    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer("❌ Недостаточно прав.")
        return

    # По ответу
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        args = message.text.split(maxsplit=1)

        if len(args) < 2:
            await message.answer(
                "Использование:\n/ban причина"
            )
            return

        user_id = target.id
        name = target.full_name
        reason = args[1]

    # По @username
    else:

        args = message.text.split(maxsplit=2)

        if len(args) < 3:
            await message.answer(
                "Использование:\n/ban @username причина"
            )
            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:

            await message.answer(
                "❌ Пользователь не найден."
            )

            return

        user_id = user["user_id"]
        name = f"@{username}"
        reason = args[2]

    await add_ban(
        user_id,
        message.from_user.id,
        reason
    )

    await message.bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=user_id
    )

    await message.answer(
        f"""
🚫 Пользователь заблокирован.

👤 {name}

📝 Причина:
{reason}
"""
    )
    await send_log(
        message.bot,
        "Выдан бан",
        message.from_user.full_name,
        name,
        reason
    )
@router.message(Command("unban"))
async def unban(message: Message):

    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer("❌ Недостаточно прав.")
        return

    # По ответу
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        user_id = target.id
        name = target.full_name

    # По username
    else:

        args = message.text.split()

        if len(args) != 2:

            await message.answer(
                "Использование:\n"
                "/unban @username\n\n"
                "или ответьте на сообщение пользователя:\n"
                "/unban"
            )

            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:

            await message.answer("❌ Пользователь не найден.")

            return

        user_id = user["user_id"]
        name = f"@{username}"

    # Снимаем бан в Telegram
    await message.bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        only_if_banned=True
    )

    # Удаляем запись из базы
    await remove_ban(user_id)

    await message.answer(
        f"""✅ Пользователь {name} разбанен."""
    )
@router.message(Command("tempban"))
async def tempban(message: Message):

    # Проверяем права
    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer(
            "❌ Недостаточно прав."
        )
        return


    user_id = None
    name = None


    # =========================
    # Вариант через ответ
    # =========================

    if message.reply_to_message:

        target = message.reply_to_message.from_user

        args = message.text.split(maxsplit=2)

        if len(args) < 3:
            await message.answer(
                "Использование:\n"
                "/tempban дни причина\n\n"
                "Пример:\n"
                "/tempban 7 Реклама"
            )
            return


        try:
            days = int(args[1])

        except ValueError:
            await message.answer(
                "❌ Количество дней должно быть числом."
            )
            return


        user_id = target.id
        name = target.full_name
        reason = args[2]


    # =========================
    # Вариант через @username
    # =========================

    else:

        args = message.text.split(maxsplit=3)


        if len(args) < 4:

            await message.answer(
                "Использование:\n"
                "/tempban @username дни причина\n\n"
                "Пример:\n"
                "/tempban @user 7 Реклама"
            )

            return


        username = args[1].replace("@", "")


        user = await get_user_by_username(username)


        if user is None:

            await message.answer(
                "❌ Пользователь не найден."
            )

            return


        user_id = user["user_id"]
        name = f"@{username}"


        try:
            days = int(args[2])

        except ValueError:

            await message.answer(
                "❌ Количество дней должно быть числом."
            )

            return


        reason = args[3]


    # Срок окончания бана
    until = int(time.time()) + (days * 86400)


    # Сохраняем в базу
    await add_tempban(
        user_id,
        message.from_user.id,
        reason,
        until
    )


    # Баним в Telegram
    await message.bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        until_date=until
    )


    await message.answer(
        f"""
⛔ Временный бан выдан

👤 Пользователь:
{name}

⏳ Срок:
{days} дней

📝 Причина:
{reason}
"""
    )
@router.message(Command("untempban"))
async def untempban(message: Message):

    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer(
            "❌ Недостаточно прав."
        )
        return


    user_id = None
    name = None


    # Через ответ на сообщение
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        user_id = target.id
        name = target.full_name


    # Через username
    else:

        args = message.text.split()

        if len(args) != 2:

            await message.answer(
                "Использование:\n"
                "/untempban @username\n\n"
                "или ответьте на сообщение пользователя:\n"
                "/untempban"
            )

            return


        username = args[1].replace("@", "")

        user = await get_user_by_username(username)


        if user is None:

            await message.answer(
                "❌ Пользователь не найден."
            )

            return


        user_id = user["user_id"]
        name = f"@{username}"


    # Снимаем бан в Telegram
    await message.bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=user_id
    )


    # Удаляем временный бан из базы
    await remove_tempban(user_id)


    await message.answer(
        f"""
✅ Временный бан снят

👤 Пользователь:
{name}
"""
    )
@router.message(Command("getban"))
async def getban(message: Message):

    access = await get_access(message.from_user.id)

    if access < 2:
        await message.answer(
            "❌ Недостаточно прав."
        )
        return


    user_id = None
    name = None


    # Через ответ
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        user_id = target.id
        name = target.full_name


    # Через username
    else:

        args = message.text.split()

        if len(args) != 2:

            await message.answer(
                "Использование:\n"
                "/getban @username\n\n"
                "или ответьте на сообщение пользователя"
            )

            return


        username = args[1].replace("@", "")

        user = await get_user_by_username(username)


        if user is None:

            await message.answer(
                "❌ Пользователь не найден."
            )

            return


        user_id = user["user_id"]
        name = f"@{username}"


    bans = await get_bans(user_id)

    tempbans = await get_tempbans(user_id)


    if not bans and not tempbans:

        await message.answer(
            f"✅ У пользователя {name} нет банов."
        )

        return


    text = f"📜 История банов\n\n👤 {name}\n\n"


    if bans:

        text += "🚫 Постоянные баны:\n\n"

        for ban in bans:

            text += (
                f"📝 Причина: {ban['reason']}\n"
                f"👮 Выдал: {ban['admin_id']}\n"
                f"📅 Дата: {ban['ban_date']}\n\n"
            )


    if tempbans:

        text += "⏳ Временные баны:\n\n"

        for ban in tempbans:

            text += (
                f"📝 Причина: {ban['reason']}\n"
                f"👮 Выдал: {ban['admin_id']}\n"
                f"⏳ До: {ban['until']}\n\n"
            )


    await message.answer(text)
@router.message(Command("kick"))
async def kick(message: Message):

    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer("❌ Недостаточно прав.")
        return

    if not message.reply_to_message:
        await message.answer(
            "Использование:\n"
            "Ответьте на сообщение пользователя:\n"
            "/kick причина"
        )
        return

    target = message.reply_to_message.from_user

    # Нельзя кикнуть себя
    if target.id == message.from_user.id:
        await message.answer("❌ Нельзя кикнуть самого себя.")
        return

    # Причина
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("❌ Укажите причину.")
        return

    reason = args[1]

    # Проверяем уровень доступа пользователя
    target_access = await get_access(target.id)

    if target_access >= access:
        await message.answer(
            "❌ Нельзя кикнуть пользователя с таким же или более высоким уровнем доступа."
        )
        return

    # Проверяем статус в Telegram
    member = await message.bot.get_chat_member(
        message.chat.id,
        target.id
    )

    if member.status == "creator":
        await message.answer("❌ Нельзя кикнуть владельца группы.")
        return

    if member.status == "administrator":
        await message.answer("❌ Нельзя кикнуть администратора Telegram.")
        return

    try:

        # Кик = бан + сразу разбан
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=target.id
        )

        await message.bot.unban_chat_member(
            chat_id=message.chat.id,
            user_id=target.id,
            only_if_banned=True
        )

        await message.answer(
            f"👢 Пользователь {target.full_name} был кикнут.\n\n"
            f"📝 Причина: {reason}\n"
            f"👮 Модератор: {message.from_user.full_name}"
        )

    except TelegramBadRequest as e:
        await message.answer(f"❌ Ошибка Telegram:\n{e}")

    except Exception as e:
        await message.answer(f"❌ Не удалось кикнуть пользователя:\n{e}")
        await send_log(
            message.bot,
            "Кик",
            message.from_user.full_name,
            target.full_name,
            reason
        )
@router.message(Command("setmoder"))
async def setmoder(message: Message):

    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer("❌ Недостаточно прав.")
        return

    user_id = None
    name = None

    # По ответу
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        if target.id == message.from_user.id:
            await message.answer("❌ Нельзя назначить самого себя.")
            return

        user_id = target.id
        name = target.full_name

    # Через username
    else:

        args = message.text.split()

        if len(args) != 2:
            await message.answer(
                "Использование:\n"
                "/setmoder @username\n\n"
                "или ответьте на сообщение пользователя."
            )
            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:
            await message.answer("❌ Пользователь не найден.")
            return

        user_id = user["user_id"]
        name = f"@{username}"

    # Защита: нельзя понизить или изменить пользователя
    # с таким же или более высоким уровнем доступа
    target_access = await get_access(user_id)

    if target_access >= access:
        await message.answer(
            "❌ Нельзя изменить уровень доступа пользователя с таким же или более высоким уровнем."
        )
        return

    await set_access(user_id, 2)

    await message.answer(
        f"✅ Пользователь {name} назначен модератором.\n\n"
        f"🔐 Новый уровень доступа: 2"
    )
@router.message(Command("rmoder"))
async def rmoder(message: Message):

    access = await get_access(message.from_user.id)

    if access < 3:
        await message.answer("❌ Недостаточно прав.")
        return

    user_id = None
    name = None

    # По ответу
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        if target.id == message.from_user.id:
            await message.answer("❌ Нельзя снять права самому себе.")
            return

        user_id = target.id
        name = target.full_name

    # Через @username
    else:

        args = message.text.split()

        if len(args) != 2:
            await message.answer(
                "Использование:\n"
                "/rmoder @username\n\n"
                "или ответьте на сообщение пользователя."
            )
            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:
            await message.answer("❌ Пользователь не найден.")
            return

        user_id = user["user_id"]
        name = f"@{username}"

    # Проверяем уровень доступа пользователя
    target_access = await get_access(user_id)

    if target_access >= access:
        await message.answer(
            "❌ Нельзя изменить уровень доступа пользователя с таким же или более высоким уровнем."
        )
        return

    # Если пользователь уже обычный
    if target_access == 1:
        await message.answer("❌ У пользователя уже нет прав модератора.")
        return

    # Снимаем права
    await set_access(user_id, 1)

    await message.answer(
        f"✅ У пользователя {name} сняты права модератора.\n\n"
        f"🔐 Новый уровень доступа: 1"
    )
@router.message(Command("setadmin"))
async def setadmin(message: Message):

    access = await get_access(message.from_user.id)

    if access < 4:
        await message.answer("❌ Только создатель может назначать администраторов.")
        return

    user_id = None
    name = None

    if message.reply_to_message:

        target = message.reply_to_message.from_user

        if target.id == message.from_user.id:
            await message.answer("❌ Нельзя назначить самого себя.")
            return

        user_id = target.id
        name = target.full_name

    else:

        args = message.text.split()

        if len(args) != 2:
            await message.answer(
                "Использование:\n"
                "/setadmin @username\n\n"
                "или ответьте на сообщение пользователя."
            )
            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:
            await message.answer("❌ Пользователь не найден.")
            return

        user_id = user["user_id"]
        name = f"@{username}"

    target_access = await get_access(user_id)

    if target_access >= access:
        await message.answer(
            "❌ Нельзя изменить уровень доступа пользователя с таким же или более высоким уровнем."
        )
        return

    await set_access(user_id, 3)

    await message.answer(
        f"👑 Пользователь {name} назначен администратором.\n\n"
        f"🔐 Новый уровень доступа: 3"
    )
@router.message(Command("radmin"))
async def radmin(message: Message):

    access = await get_access(message.from_user.id)

    if access < 4:
        await message.answer("❌ Только создатель может снимать администраторов.")
        return

    user_id = None
    name = None

    if message.reply_to_message:

        target = message.reply_to_message.from_user

        if target.id == message.from_user.id:
            await message.answer("❌ Нельзя снять права самому себе.")
            return

        user_id = target.id
        name = target.full_name

    else:

        args = message.text.split()

        if len(args) != 2:
            await message.answer(
                "Использование:\n"
                "/radmin @username\n\n"
                "или ответьте на сообщение пользователя."
            )
            return

        username = args[1].replace("@", "")

        user = await get_user_by_username(username)

        if user is None:
            await message.answer("❌ Пользователь не найден.")
            return

        user_id = user["user_id"]
        name = f"@{username}"

    target_access = await get_access(user_id)

    if target_access >= access:
        await message.answer(
            "❌ Нельзя изменить уровень доступа пользователя с таким же или более высоким уровнем."
        )
        return

    if target_access != 3:
        await message.answer("❌ Пользователь не является администратором.")
        return

    await set_access(user_id, 2)

    await message.answer(
        f"✅ Пользователь {name} больше не администратор.\n\n"
        f"🔐 Новый уровень доступа: 2 (Модератор)"
    )
@router.message(Command("givemoney"))
async def givemoney(message: Message):

    await message.answer("1. Команда запущена")

    access = await get_access(message.from_user.id)

    await message.answer(f"2. Твой доступ: {access}")
@router.message()
async def check_mute(message: Message):

    if not message.from_user:
        return

    if message.text and message.text.startswith("/"):
        return

    mute = await get_mute(message.from_user.id)

    if mute:
        try:
            await message.delete()
        except Exception:
            pass
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
