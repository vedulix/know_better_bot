import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.active_listening import register_active_listening
from tgbot.handlers.admin import register_admin
from tgbot.handlers.commands import register_commands
from tgbot.handlers.know_better import register_know_better
from tgbot.handlers.main_menu import register_main_menu
from tgbot.handlers.nonviolent_communication import register_nonviolent_communication
from tgbot.handlers.problem import register_problem
from tgbot.handlers.start import register_start
from tgbot.infrastucture.database.functions.setup import create_session_pool
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, session_pool):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(DatabaseMiddleware(session_pool=session_pool))



def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_start(dp)
    register_main_menu(dp)
    register_active_listening(dp)
    register_nonviolent_communication(dp)
    register_commands(dp)
    register_know_better(dp)
    register_problem(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    session_pool = create_session_pool(config.db)

    bot['config'] = config

    register_all_middlewares(dp, config, session_pool)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
