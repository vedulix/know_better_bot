import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from tgbot.keyboards.reply import whom, next_question, main_menu_buttons, next_sub_question
from tgbot.locals.load_json import data
from tgbot.locals.load_questions import questions_myself, questions_partner, questions_family, questions_friend, \
  questions_partner_test
from tgbot.misc.states import Know

async def choose(message: types.Message, state: FSMContext):
  await message.answer(data.know_better.whom.text, reply_markup=whom)
  await Know.whom.set()
  await state.update_data(questions_family=['start'])


async def myself(message: types.Message, state: FSMContext):
  question = random.choice(questions_myself)
  await message.answer(question, reply_markup=next_question)
  await Know.myself.set()


async def partner(message: types.Message, state: FSMContext):
  question = random.choice(questions_partner)
  await message.answer(question, reply_markup=next_question)
  await Know.partner.set()

async def partner_test(message: types.Message, state: FSMContext):
  question = random.choice(questions_partner_test)
  await message.answer(question, reply_markup=next_sub_question)
  await Know.partner_test.set()


async def partner_choose(message: types.Message, state: FSMContext):
  await message.answer(data.know_better.partner.choose.text, reply_markup=partner_choose)
  await Know.partner_choose.set()


async def family_(message: types.Message, state: FSMContext):
  question = random.choice(questions_family)
  await message.answer(question, reply_markup=next_question)
  await Know.family.set()

async def family(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    if len(data["questions_family"])==0:
      await message.answer("Вопросы из этой категории закончились. Если ты хочешь предложить свой вопрос, отправь его по контактам в описании бота. Мы его рассмотрим, и если он подойдёт, добавим в список вопросов.\n\nДальше вопросы пойдут заново по второму кругу. Ты можешь сменить категорию, нажав на кнопку на клавиатуре.", reply_markup=next_question)
      data["questions_family"] = questions_family
    elif data["questions_family"][0]=='start':
      data["questions_family"] = questions_family

  question = random.choice(data.get("questions_family"))
  async with state.proxy() as data:
    tmp=data["questions_family"]
    tmp.remove(question)
    data["questions_family"]=tmp

  await message.answer(question, reply_markup=next_question)
  await Know.family.set()


async def friend(message: types.Message, state: FSMContext):
  question = random.choice(questions_friend)
  await message.answer(question, reply_markup=next_question)
  await Know.friend.set()

async def to_main_menu(message: types.Message, state: FSMContext):
  await message.answer(data.main_menu.text, reply_markup=main_menu_buttons)
  await state.reset_state()


async def dont(message: types.Message, state: FSMContext):
  await message.answer(data.know_better.questions.dont, reply_markup=next_question)

def register_know_better(dp: Dispatcher):
  dp.register_message_handler(choose, text=data.main_menu.kb[0])
  dp.register_message_handler(choose, text=data.know_better.questions.kb[1], state=Know)
  dp.register_message_handler(myself, text=data.know_better.whom.kb[0], state=Know.whom)
  dp.register_message_handler(myself, text=data.know_better.questions.kb[0], state=Know.myself)
  dp.register_message_handler(partner, text=data.know_better.whom.kb[1], state=Know.whom)
  dp.register_message_handler(partner, text=data.know_better.questions.kb[0], state=Know.partner)
  dp.register_message_handler(family, text=data.know_better.whom.kb[2], state=Know.whom)
  dp.register_message_handler(family, text=data.know_better.questions.kb[0], state=Know.family)
  dp.register_message_handler(friend, text=data.know_better.whom.kb[3], state=Know.whom)
  dp.register_message_handler(friend, text=data.know_better.questions.kb[0], state=Know.friend)
  dp.register_message_handler(to_main_menu, text=data.main_menu.text_to, state=Know)

  dp.register_message_handler(dont, state=Know)




