from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


from database import (
    get_balance,
    add_money,
    remove_money,
    get_user_by_username
)



router = Router()



@router.message(Command("pay"))
async def pay(message: Message):


    args = message.text.split()


    if len(args) != 3:

        await message.answer(
            """
❌ Используйте:

/pay @username сумма
"""
        )

        return



    username = args[1].replace("@", "")


    try:

        amount = int(args[2])

    except:

        await message.answer(
            "❌ Сумма должна быть числом"
        )

        return



    if amount <= 0:

        await message.answer(
            "❌ Нельзя отправить такую сумму"
        )

        return



    sender_id = message.from_user.id



    sender_balance = await get_balance(
        sender_id
    )


    if sender_balance < amount:

        await message.answer(
            "❌ Недостаточно денег"
        )

        return



    receiver = await get_user_by_username(
        username
    )



    if receiver is None:

        await message.answer(
            "❌ Пользователь не найден"
        )

        return



    if receiver["user_id"] == sender_id:

        await message.answer(
            "❌ Нельзя переводить самому себе"
        )

        return



    await remove_money(
        sender_id,
        amount
    )


    await add_money(
        receiver["user_id"],
        amount
    )



    await message.answer(
f"""
✅ Перевод выполнен


💸 Отправлено:

{amount} ₽


👤 Получатель:

@{username}
"""
    )