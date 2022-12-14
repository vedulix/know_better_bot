import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from tgbot.keyboards.reply import rec_choose, main_menu_buttons, about_bot_kb
from tgbot.locals.load_json import data
from tgbot.misc.states import main_menu_states


async def recommendations(message: types.Message, state: FSMContext):
  await message.answer(data.rec.choose.text, reply_markup=rec_choose)
  await main_menu_states.rec.set()

async def about(message: types.Message, state: FSMContext):
  await message.answer(data.about_bot.text, reply_markup=about_bot_kb)
  await main_menu_states.about.set()

async def to_main_menu(message: types.Message, state: FSMContext):
  await message.answer(message.from_user.first_name + ", " + random.choice(data.main_menu.phrases) + " " + random.choice(data.emoji) + data.main_menu.text, reply_markup=main_menu_buttons)
  await state.reset_state()


def register_main_menu(dp: Dispatcher):
  dp.register_message_handler(about, text=data.main_menu.kb[2])
  dp.register_message_handler(recommendations, text=data.main_menu.kb[1])
  dp.register_message_handler(to_main_menu, text=data.main_menu.text_to, state=main_menu_states.rec)
  dp.register_message_handler(to_main_menu, text=data.about_bot.kb[0], state=main_menu_states.about)

