from aiogram import Bot
from datetime import datetime


LOG_CHAT_ID = 1005492319149
async def send_log(
    bot: Bot,
    action,
    admin,
    user,
    reason=None
):

    text = f"""
🛡 <b>ЛОГ МОДЕРАЦИИ</b>

⚠️ Действие:
<b>{action}</b>

👮 Администратор:
{admin}

👤 Пользователь:
{user}
"""


    if reason:
        text += f"""

📝 Причина:
{reason}
"""


    text += f"""

📅 Дата:
{datetime.now().strftime("%d.%m.%Y %H:%M")}
"""


    await bot.send_message(
        LOG_CHAT_ID,
        text,
        parse_mode="HTML"
    )