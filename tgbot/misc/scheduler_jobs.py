import random
from datetime import datetime

from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.locals.load_json import data
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB



"""async def send(bot: Bot, config: Config, dp: Dispatcher, session_pool: AsyncSession):
  async with session_pool() as session:
   ..."""