import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from tgbot.keyboards.reply import rec_choose, nvc_kb_1, nvc_kb_2, nvc_kb_3, nvc_kb_4, nvc_kb_6, nvc_kb_5
from tgbot.locals.load_json import data
from tgbot.misc.states import main_menu_states, nvc_states


async def nvc1(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.define.text, reply_markup=nvc_kb_1)
  await nvc_states.n1.set()


async def nvc2(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.n1.text, reply_markup=nvc_kb_2)
  await nvc_states.n2.set()


async def nvc3(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.n2.text, reply_markup=nvc_kb_3)
  await nvc_states.n3.set()


async def nvc4(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.n3.text, reply_markup=nvc_kb_4)
  await nvc_states.n4.set()


async def nvc5(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.n4.text, reply_markup=nvc_kb_5)
  await nvc_states.n5.set()


async def nvc6(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.example.text, reply_markup=nvc_kb_6)
  await nvc_states.n6.set()



async def back(message: types.Message, state: FSMContext):
  await message.answer(data.rec.nvc.example.text_return, reply_markup=rec_choose)
  await main_menu_states.rec.set()



def register_nonviolent_communication(dp: Dispatcher):
  dp.register_message_handler(nvc1, state=main_menu_states.rec, text=data.rec.choose.kb[1])
  dp.register_message_handler(nvc2, state=nvc_states.n1, text=data.rec.nvc.define.kb[0])
  dp.register_message_handler(nvc3, state=nvc_states.n2)
  dp.register_message_handler(nvc4, state=nvc_states.n3)
  dp.register_message_handler(nvc5, state=nvc_states.n4)
  dp.register_message_handler(nvc6, state=nvc_states.n5, text=data.rec.nvc.n4.kb[0])
  dp.register_message_handler(back, state=nvc_states.n6)
  dp.register_message_handler(back, state=nvc_states.n5, text=data.rec.nvc.n4.kb[1])
  dp.register_message_handler(back, state=nvc_states, text=data.back)