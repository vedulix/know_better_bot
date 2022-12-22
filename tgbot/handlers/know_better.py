import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastucture.database.functions.users import load_questions, write_answer
from tgbot.keyboards.reply import whom, next_question, main_menu_buttons, work_hi_kb, friend_choose_kb, \
  partner_choose_kb, work_ans_kb, work_kb
from tgbot.locals.load_json import data
from tgbot.misc.states import Know

async def choose(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.know_better.whom.text, reply_markup=whom)
  await Know.whom.set()


async def family_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'family')
  await state.update_data(datas=q)
  await state.update_data(last_state=choose)

  await message.answer(data.know_better.family_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()

async def networking_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'networking')
  await state.update_data(datas=q)
  await state.update_data(last_state=choose)

  await message.answer(data.know_better.networking_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()

async def partner_choose(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.know_better.partner.choose.text, reply_markup=partner_choose_kb)
  await Know.partner_choose.set()

async def partner_simple_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'partner_simple')
  await state.update_data(datas=q)
  await state.update_data(last_state=partner_choose)
  await message.answer(data.know_better.partner.simple_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()

async def partner_future_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'partner_future')
  await state.update_data(datas=q)
  await state.update_data(last_state=partner_choose)
  await message.answer(data.know_better.partner.future_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()

async def partner_check_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'partner_check')
  await state.update_data(datas=q)
  await state.update_data(last_state=partner_choose)

  await message.answer(data.know_better.partner.check_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()


async def friend_choose(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.know_better.friend.choose.text, reply_markup=friend_choose_kb)
  await Know.friend_choose.set()

async def friend_simple_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'friend_simple')
  await state.update_data(datas=q)
  await state.update_data(last_state=friend_choose)
  await message.answer(data.know_better.friend.simple_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()

async def friend_private_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'friend_private')
  await state.update_data(datas=q)
  await state.update_data(last_state=friend_choose)
  await message.answer(data.know_better.friend.private_hi.text, reply_markup=work_hi_kb)
  await Know.work.set()


async def another_option(message: types.Message, state: FSMContext, session: AsyncSession):
  async with state.proxy() as datas:
    last_state = datas["last_state"]
    await last_state(message, state, session)

async def work(message: types.Message, state: FSMContext, session: AsyncSession):
  async with state.proxy() as datas:
    if len(datas["datas"])>0:
      await message.answer(datas["datas"][0]['question'], reply_markup=work_kb)
      datas["datas"] = datas["datas"][1:]
    else:
      await message.answer(data.know_better.end.text + "\n\n" + data.know_better.whom.text, reply_markup=whom)
      await Know.whom.set()

async def dont(message: types.Message, state: FSMContext):
  await message.answer(data.know_better.questions.dont, reply_markup=next_question)

def register_know_better(dp: Dispatcher):
  dp.register_message_handler(choose, text=data.main_menu.kb[0])
  #dp.register_message_handler(choose, text=data.know_better.sub_questions.work.kb[1], state=Know)
  dp.register_message_handler(another_option, text=data.know_better.sub_questions.work.kb[1], state=Know)
#  dp.register_message_handler(choose, text=data.know_better.sub_questions.work_ans.kb[1], state=Know)

  #dp.register_message_handler(myself, text=data.know_better.whom.kb[0], state=Know.whom)
  dp.register_message_handler(choose, text=data.know_better.sub_questions.hi.kb[1], state=Know.work_ans)

  dp.register_message_handler(family_hi, text=data.know_better.whom.kb[2], state=Know.whom)
  dp.register_message_handler(networking_hi, text=data.know_better.whom.kb[3], state=Know.whom)



  dp.register_message_handler(friend_choose, text=data.know_better.whom.kb[1], state=Know.whom)
  dp.register_message_handler(friend_simple_hi, text=data.know_better.friend.choose.kb[0], state=Know.friend_choose)
  dp.register_message_handler(friend_private_hi, text=data.know_better.friend.choose.kb[1], state=Know.friend_choose)
  dp.register_message_handler(choose, text=data.know_better.friend.choose.kb[2], state=Know.friend_choose)

  dp.register_message_handler(partner_choose, text=data.know_better.whom.kb[0], state=Know.whom)
  dp.register_message_handler(partner_simple_hi, text=data.know_better.partner.choose.kb[0], state=Know.partner_choose)
  dp.register_message_handler(partner_future_hi, text=data.know_better.partner.choose.kb[1], state=Know.partner_choose)
  dp.register_message_handler(partner_check_hi, text=data.know_better.partner.choose.kb[2], state=Know.partner_choose)
  dp.register_message_handler(choose, text=data.know_better.partner.choose.kb[3], state=Know.partner_choose)


  #dp.register_message_handler(to_main_menu, text=data.main_menu.text_to, state=Know)
  dp.register_message_handler(work, text=data.know_better.sub_questions.hi.kb[0], state=Know.work)
 # dp.register_message_handler(work_ans, text=data.know_better.sub_questions.hi.kb[0], state=Know.work_ans)
  dp.register_message_handler(choose, text=data.know_better.sub_questions.hi.kb[1], state=Know.work)
  dp.register_message_handler(work, state=Know.work)
#  dp.register_message_handler(work_ans, state=Know.work_ans)

  dp.register_message_handler(dont, state=Know)




