import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from tgbot.keyboards.reply import rec_choose, al_kb_1, al_kb_2, al_kb_3, al_kb_4, al_kb_5, al_kb_6, al_kb_7
from tgbot.locals.load_json import data
from tgbot.misc.states import main_menu_states, actlis_states


async def al1(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.pre_define.text, reply_markup=al_kb_1)
  await actlis_states.al1.set()

async def al2(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.define.text, reply_markup=al_kb_2)
  await actlis_states.al2.set()


async def al3(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.factors.text, reply_markup=al_kb_3)
  await actlis_states.al3.set()


async def al4(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.method_1.text, reply_markup=al_kb_4)
  await actlis_states.al4.set()


async def al5(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.method_2.text, reply_markup=al_kb_5)
  await actlis_states.al5.set()


async def al6(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.method_3.text, reply_markup=al_kb_6)
  await actlis_states.al6.set()

async def al7(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.advice.text, reply_markup=al_kb_7)
  await actlis_states.al7.set()


async def back(message: types.Message, state: FSMContext):
  await message.answer(data.rec.actlis.advice.text_return, reply_markup=rec_choose)
  await main_menu_states.rec.set()



def register_active_listening(dp: Dispatcher):
  dp.register_message_handler(al1, state=main_menu_states.rec, text=data.rec.choose.kb[0])
  dp.register_message_handler(al2, state=actlis_states.al1, text=data.rec.actlis.pre_define.kb[0])
  dp.register_message_handler(al3, state=actlis_states.al2)
  dp.register_message_handler(al4, state=actlis_states.al3)
  dp.register_message_handler(al5, state=actlis_states.al4)
  dp.register_message_handler(al6, state=actlis_states.al5)
  dp.register_message_handler(al7, state=actlis_states.al6)
  dp.register_message_handler(back, state=actlis_states.al7)
  dp.register_message_handler(back, state=actlis_states, text=data.back)