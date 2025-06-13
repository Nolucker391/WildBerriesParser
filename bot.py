import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from database.session import engine
from database.models import Base
from settings.config import config, logger
from handlers.router import router

bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML")
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    dp = Dispatcher()
    dp.include_routers(router)

    bot_info = await bot.me()
    bot_name = bot_info.first_name
    logger.info(f"Бот {bot_name} запущен!")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(main())
