import random
from datetime import datetime
import time
from typing import List

from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.infrastucture.database.functions.users import select_all_users, deactivate_user
from tgbot.keyboards.inline import timelist_kb
from tgbot.keyboards.reply import main_menu_buttons
from tgbot.locals.load_json import data as my_data
from tgbot.misc.states import Mail


async def set_mailing(message: types.Message, config: Config):
    if message.from_user.id in config.tg_bot.test_ids:
        await message.answer("waiting your message, use /cancel if you won't send")
        await Mail.wait.set()


async def cancel_mailing(message: types.Message, state: FSMContext):
    await message.answer('canceled, you are in main menu')
    await state.reset_state()


async def safety_send_notif(bot: Bot, dp: Dispatcher, users: List, data, text, markup, session: AsyncSession):
    if data is not None:
        text = data['question']
        text += f" {random.choice(my_data.emoji)}"

    for u in users:
        try:
            if not u['telegram_id']:  # Check if user's telegram_id is valid
                raise UserDataNotValid(u['telegram_id'])

            state = dp.current_state(user=u['telegram_id'])

            if data is not None:
                await state.update_data(daily_data=data)
            await bot.send_message(chat_id=u['telegram_id'], text=text,
                                   reply_markup=markup, disable_notification=True)
        except UserDataNotValid as e:
            print(f"Invalid user data: {e}")
        except Exception as ex:
            # Raise a custom NotificationError with user_id
            raise NotificationError(u['telegram_id'], message=str(ex))
            await deactivate_user(session, telegram_id=u['telegram_id'])

    await session.commit()


async def mailing(message: types.Message, state: FSMContext, session: AsyncSession):
    users = await select_all_users(session)
    await message.answer('mailing started')
    await state.reset_state()

    for u in users:
        try:
            await message.send_copy(chat_id=u['telegram_id'], reply_markup=main_menu_buttons)
        except Exception as ex:
            await deactivate_user(session, telegram_id=u['telegram_id'])

        # time.sleep(1)
    await session.commit()
    await message.answer('mailing finished')


async def setting_time(message: types.Message, state: FSMContext, session: AsyncSession):
    await message.answer(my_data.jour.notif.change_time_text, reply_markup=timelist_kb)


async def send_emotions(message: types.Message):
    await message.answer_photo(my_data.emotions_photo.link, caption=my_data.emotions_photo.caption)


async def send_states(message: types.Message):
    await message.answer_photo(my_data.states_photo.link, caption=my_data.states_photo.caption)


async def send_needs(message: types.Message):
    await message.answer_photo(my_data.needs_photo.link, caption=my_data.needs_photo.caption)


"""
с помощью декоратора
@dp.message_handler(Command("needs"), state="*")
  async def send_needs(message: types.Message):
    await message.answer_photo(my_data.needs_photo.link, caption=my_data.needs_photo.caption)
"""


def register_commands(dp: Dispatcher):
    dp.register_message_handler(set_mailing, commands=["mail"], state="*")
    dp.register_message_handler(cancel_mailing, commands=["cancel"], state=Mail.wait)
    dp.register_message_handler(mailing, state=Mail.wait)
    dp.register_message_handler(setting_time, commands=['settings', 'set_notification', 'notification'], state="*")
    dp.register_message_handler(send_emotions, commands=["feelings"], state="*")
    dp.register_message_handler(send_states, commands=["states"], state="*")
    dp.register_message_handler(send_needs, commands=["needs"], state="*")
