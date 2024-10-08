import random
from datetime import datetime
import time
from typing import List

from aiogram import Dispatcher, types, Bot
from aiogram.bot import bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import Config
from tgbot.handlers.main_menu import to_main_menu
from tgbot.infrastucture.database.functions.users import select_all_users, deactivate_user
from tgbot.keyboards.inline import timelist_kb
from tgbot.keyboards.inline import support_link_kb
from tgbot.keyboards.reply import main_menu_buttons, back_kb
from tgbot.locals.load_json import data as my_data
from tgbot.misc.states import Mail, Feedback
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


async def set_mailing(message: types.Message, config: Config):
  if message.from_user.id in config.tg_bot.test_ids:
    await message.answer("waiting your message, use /cancel if you won't send")
    await Mail.wait.set()

async def set_donate_mailing(message: types.Message, config: Config):
  if message.from_user.id in config.tg_bot.test_ids:
    await message.answer("waiting your donate message (with donate button), use /cancel if you won't send")
    await Mail.wait_donate.set()

async def cancel_mailing(message: types.Message, state: FSMContext):
  await message.answer('canceled, you are in main menu')
  await state.reset_state()


async def safety_send_notif(bot: Bot, dp: Dispatcher, users: List, data, text, markup, session: AsyncSession):
  if data is not None:
    text = data['question']
    text += f" {random.choice(my_data.emoji)}"

  for u in users:
    try:
      state = dp.current_state(user=u['telegram_id'])

      if data is not None:
        await state.update_data(daily_data=data)
      await bot.send_message(chat_id=u['telegram_id'], text=text,
                             reply_markup=markup, disable_notification=True)
    except Exception as ex:
      #print(f"{datetime.now()} -- {ex} -- {u['telegram_id']}")
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


async def mailing_donate(message: types.Message, state: FSMContext, session: AsyncSession):
  users = await select_all_users(session)
  await message.answer('mailing donate started')
  await state.reset_state()

  for u in users:
    try:
      await message.send_copy(chat_id=u['telegram_id'], reply_markup=support_link_kb, disable_web_page_preview=True)
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

async def about(message: types.Message):
  await message.answer(my_data.about_bot.text, reply_markup=support_link_kb, disable_web_page_preview=True)

async def feedback(message: types.Message, state: FSMContext):
  await message.answer(my_data.feedback.text, reply_markup=back_kb)
  await Feedback.wait.set()

async def feedback_wait(message: types.Message, state: FSMContext, config: Config):
  if message.text == my_data.back:
    await to_main_menu(message, state)
  else:
    await state.reset_state()
    await message.forward(chat_id=config.tg_bot.test_ids[1])
    await message.answer(my_data.feedback.got_feedback_text, reply_markup=main_menu_buttons)



"""
с помощью декоратора
@dp.message_handler(Command("needs"), state="*")
  async def send_needs(message: types.Message):
    await message.answer_photo(my_data.needs_photo.link, caption=my_data.needs_photo.caption)
"""


async def set_digit_mailing(message: types.Message, config: Config):
    if message.from_user.id in config.tg_bot.test_ids:
        command_parts = message.text.split()
        if len(command_parts) != 2 or not command_parts[1].isdigit() or int(command_parts[1]) not in range(10):
            await message.answer("Пожалуйста, укажите цифру от 0 до 9 после команды, например: /mail_digit 9")
            return
        digit = int(command_parts[1])
        await message.answer(f"Ожидаю ваше сообщение для рассылки пользователям с первой цифрой ID {digit}. Используйте /cancel для отмены.")
        await Mail.wait_digit.set()
        await message.bot.get('state').update_data(digit=digit)

async def mailing_digit(message: types.Message, state: FSMContext, session: AsyncSession):
    state_data = await state.get_data()
    digit = state_data.get('digit')
    users = await select_all_users(session)
    await message.answer(f'Началась рассылка для пользователей с первой цифрой ID {digit}')
    await state.reset_state()

    for u in users:
        if str(u['telegram_id']).startswith(str(digit)):
            try:
                await message.send_copy(chat_id=u['telegram_id'], reply_markup=main_menu_buttons)
            except Exception as ex:
                await deactivate_user(session, telegram_id=u['telegram_id'])

    await session.commit()
    await message.answer('Рассылка завершена')


def register_commands(dp: Dispatcher):
  dp.register_message_handler(set_donate_mailing, commands=["mail_donate"], state="*")
  dp.register_message_handler(set_mailing, commands=["mail"], state="*")
  dp.register_message_handler(cancel_mailing, commands=["cancel"], state=Mail.wait)
  dp.register_message_handler(cancel_mailing, commands=["cancel"], state=Mail.wait_donate)
  dp.register_message_handler(mailing, state=Mail.wait)
  dp.register_message_handler(mailing_donate, state=Mail.wait_donate)
  dp.register_message_handler(setting_time, commands=['settings', 'set_notification', 'notification'], state="*")
  dp.register_message_handler(send_emotions, commands=["feelings"], state="*")
  dp.register_message_handler(send_states, commands=["states"], state="*")
  dp.register_message_handler(send_needs, commands=["needs"], state="*")
  dp.register_message_handler(about, commands=["about"], state="*")
  dp.register_message_handler(feedback, commands=["feedback"], state="*")
  dp.register_message_handler(feedback_wait, state=Feedback.wait)
  dp.register_message_handler(set_digit_mailing, commands=["mail_digit"], state="*")
  dp.register_message_handler(mailing_digit, state=Mail.wait_digit)

