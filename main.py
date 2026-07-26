import asyncio

from aiogram import Bot, Dispatcher

from config import TOKEN

from database import create_database, add_business_income

from start import router as start_router
from profile import router as profile_router
from messages import router as messages_router
from economy import router as economy_router
from payments import router as payments_router
from nickname import router as nickname_router
from permissions import router as permissions_router
from roles import router as roles_router
from help import router as help_router
from moderation import router as moderation_router
from join import router as join_router



async def business_timer():

    while True:

        await add_business_income()

        print("💰 Доходы бизнесов начислены")

        await asyncio.sleep(3600)



async def main():

    print("1. Запуск")

    await create_database()

    print("2. База готова")


    bot = Bot(
        token=TOKEN
    )

    dp = Dispatcher()


    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(messages_router)
    dp.include_router(economy_router)
    dp.include_router(payments_router)
    dp.include_router(nickname_router)
    dp.include_router(permissions_router)
    dp.include_router(roles_router)
    dp.include_router(help_router)
    dp.include_router(moderation_router)
    dp.include_router(join_router)


    asyncio.create_task(
        business_timer()
    )

    print("3. Таймер запущен")
    print("🤖 Бот запущен")


    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())