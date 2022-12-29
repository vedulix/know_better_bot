from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.handlers.commands import safety_send_notif


async def send_message_to_admin(bot: Bot, config: Config, dp: Dispatcher, session_pool: AsyncSession):
 # select users...
  #safety_send_notif(bot=bot, )
  ...