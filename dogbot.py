import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.test import TestFilter
from tgbot.handlers.active_listening import register_active_listening
from tgbot.handlers.admin import register_admin
from tgbot.handlers.commands import register_commands
from tgbot.handlers.journaling import register_journaling
from tgbot.handlers.know_better import register_know_better
from tgbot.handlers.main_menu import register_main_menu
from tgbot.handlers.nonviolent_communication import register_nonviolent_communication
from tgbot.handlers.problem import register_problem
from tgbot.handlers.start import register_start
from tgbot.handlers.test import register_test
from tgbot.infrastucture.database.functions.setup import create_session_pool
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.last_activity import DAUMiddleware
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.misc.scheduler_jobs import send_daily_question
import warnings

from pytz_deprecation_shim import PytzUsageWarning

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, session_pool, scheduler):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(DatabaseMiddleware(session_pool=session_pool))
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(SchedulerMiddleware(scheduler))
    dp.setup_middleware(DAUMiddleware(session_pool=session_pool))



def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(TestFilter)



def register_all_handlers(dp):
    register_admin(dp)
    register_test(dp)
    register_start(dp)
    register_commands(dp)

    register_main_menu(dp)
    register_active_listening(dp)
    register_nonviolent_communication(dp)
    register_know_better(dp)
    register_journaling(dp)
    register_problem(dp)

def set_scheduled_jobs(scheduler, *args, **kwargs):
    scheduler.add_job(send_daily_question, 'cron', day_of_week='1, 3, 5', hour='*', minute=11, jitter=599)
    #scheduler.add_job(send_daily_question, 'interval', seconds=5)

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
    job_stores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
            host=config.redis.host, port=config.redis.port, password=config.redis.password
        )
    }
    warnings.filterwarnings(action="ignore", category=PytzUsageWarning)
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler())
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.ctx.add_instance(dp, declared_class=Dispatcher)
    scheduler.ctx.add_instance(config, declared_class=Config)
    scheduler.ctx.add_instance(session_pool, declared_class=AsyncSession)
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

    bot['config'] = config

    # Ставим наши таски на запуск, передаем нужные переменные
    set_scheduled_jobs(scheduler)

    register_all_middlewares(dp, config, session_pool, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        scheduler.start()
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
