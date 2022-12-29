from datetime import datetime

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.handlers.commands import safety_send_notif
from tgbot.infrastucture.database.functions.users import select_scheduler_users, select_daily_question
from tgbot.keyboards.inline import daily_ref_kb


async def send_daily_question(bot: Bot, config: Config, dp: Dispatcher, session_pool: AsyncSession):
  async with session_pool() as session:
    hour = datetime.now().hour
    users = await select_scheduler_users(session=session, hour=hour)
    daily_data = await select_daily_question(session, category='myself')

    await safety_send_notif(bot=bot, dp=dp, users=users, data=daily_data, markup=daily_ref_kb, session=session)
