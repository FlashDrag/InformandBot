import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import load_config
from aiogram.dispatcher.filters import ChatTypeFilter
# from filters.role import RoleFilter, AdminFilter
from filters.admin import AdminFilter
from handlers.private.admin.start import register_start_admin
from handlers.private.admin.add_data import register_add_data_admin
from handlers.private.user import register_private_user
# from middlewares.db import DbMiddleware
# from middlewares.role import RoleMiddleware

from utils.set_bot_commands import set_commands

logger = logging.getLogger(__name__)


# def create_pool(user, password, database, host, echo):
#     raise NotImplementedError  # TODO check your db connector

def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    # dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ChatTypeFilter)


def register_all_handlers(dp):
    register_start_admin(dp)
    register_add_data_admin(dp)
    register_private_user(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config()

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()
    # pool = await create_pool(
    #     user=config.db.user,
    #     password=config.db.password,
    #     database=config.db.database,
    #     host=config.db.host,
    #     echo=False,
    # )

    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)

    # dp.middleware.setup(DbMiddleware(pool))
    # dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))

    bot['config'] = config
    # если в хендлере нунжо получить что-то из конфиг
    # bot.get('config')

    await set_commands(dp)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
