from aiogram import Bot

from tgbot.config import Config


async def send_message_to_admin(bot: Bot, config: Config):
  for admin_id in config.tg_bot.test_ids:
    await bot.send_message(text="Сообщение по таймеру", chat_id=admin_id)