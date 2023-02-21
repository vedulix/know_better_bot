import random
from datetime import datetime

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.handlers.commands import safety_send_notif
from tgbot.infrastucture.database.functions.users import select_scheduler_users, select_daily_question, \
  select_all_users, select_weekly_ideas
from tgbot.keyboards.inline import daily_ref_kb
from tgbot.locals.load_json import data
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB



async def send_daily_question(bot: Bot, config: Config, dp: Dispatcher, session_pool: AsyncSession):
  async with session_pool() as session:
    hour = datetime.now().hour
    users = await select_scheduler_users(session=session, hour=hour)
    daily_data = await select_daily_question(session, category='daily')

    await safety_send_notif(bot=bot, dp=dp, users=users, data=daily_data, text=None, markup=daily_ref_kb, session=session)


async def send_weekly_ideas(bot: Bot, config: Config, dp: Dispatcher, session_pool: AsyncSession):
  async with session_pool() as session:
    users = await select_all_users(session=session)
    ideas = await select_weekly_ideas(session, category='rest_ideas')
    text = random.choice(data.rest.quotes) + "\n\n" + data.rest.suggestion
    c = 1
    for idea in ideas:
      text += f"\n{c}. {idea['idea']}"
      c+=1
    await safety_send_notif(bot=bot, dp=dp, users=users, data=None, text=text, markup=IKM(inline_keyboard=[[IKB(text=f"{data.rest.thank} {random.choice(data.emoji)}", callback_data="weekly_idea_thank_click")]]),
                            session=session)
