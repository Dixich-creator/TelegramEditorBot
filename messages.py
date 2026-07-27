from aiogram import Router
from aiogram.types import Message

from database import add_user, add_message


router = Router()


@router.message(lambda message: message.text and not message.text.startswith("/"))
async def messages(message: Message):
    if message.from_user is None:
        return


    await add_user(
        message.from_user.id,
        message.from_user.username
    )


    await add_message(
        message.from_user.id
    )
