import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.infrastucture.database.functions.users import select_all_users, deactivate_user
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
  await state.reset_state()

  for u in users:
    try:
      await message.send_copy(chat_id=u['telegram_id'], reply_markup=main_menu_buttons)
 #   except BotBlocked or UserDeactivated:
 #     await deactivate_user(session, telegram_id=u['telegram_id'])
    except Exception as ex:
      await message.answer(f"{ex} {u['telegram_id']}")
      await deactivate_user(session, telegram_id=u['telegram_id'])

    #time.sleep(1)
  await session.commit()
  await message.answer('mailing finished')


def register_commands(dp: Dispatcher):
  dp.register_message_handler(set_mailing, commands=["mail"], state="*")
  dp.register_message_handler(cancel_mailing, commands=["cancel"], state=Mail.wait)
  dp.register_message_handler(mailing, state=Mail.wait)
