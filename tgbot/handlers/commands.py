from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.infrastucture.database.functions.users import select_all_users
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.locals.load_json import data
from tgbot.misc.states import Mail


async def set_mailing(message: types.Message, config: Config  ):
  if message.from_user.id in config.tg_bot.test_ids:
    await message.answer("waiting your message, use /cancel if you won't send")
    await Mail.wait.set()

async def cancel_mailing(message: types.Message, state: FSMContext):
  await message.answer('canceled, you in main menu')
  await state.reset_state()


async def mailing(message: types.Message, state: FSMContext, session: AsyncSession):
  users = await select_all_users(session)
  await message.answer('mailing started')
  for u in users:
    await message.send_copy(chat_id=u['telegram_id'])
  await message.answer('mailing finished')
  await state.reset_state()


def register_commands(dp: Dispatcher):
  dp.register_message_handler(set_mailing, commands=["mail"], state="*")
  dp.register_message_handler(cancel_mailing, commands=["cancel"], state=Mail.wait)
  dp.register_message_handler(mailing, state=Mail.wait)
