from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from database import add_news, get_news, get_access


router = Router()



@router.message(Command("addnews"))
async def addnews(message: Message):

    access = await get_access(message.from_user.id)


    if access < 4:
        await message.answer(
            "❌ Только создатель может добавлять новости."
        )
        return


    text = message.text.replace(
        "/addnews",
        ""
    ).strip()


    if not text:

        await message.answer(
            "Использование:\n"
            "/addnews текст новости"
        )

        return


    await add_news(
        text,
        message.from_user.id
    )


    await message.answer(
        "✅ Новость добавлена!"
    )




@router.message(Command("news"))
async def news(message: Message):

    items = await get_news()


    if not items:

        await message.answer(
            "📰 Новостей пока нет."
        )

        return



    text = "📰 <b>Новости Fluget New</b>\n\n"


    for item in items:

        text += (
            f"🔥 {item['text']}\n"
            f"📅 {item['date']}\n"
            f"━━━━━━━━━━━━━━\n"
        )


    await message.answer(
        text,
        parse_mode="HTML"
    )