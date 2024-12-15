import asyncio
import time

from tgbot.handlers.main_menu import to_main_menu
from tgbot.infrastucture.database.functions.users import get_all_last_answers, load_questions, write_answer, get_last_answers, \
  count_questions_in_category, edit_notif_user
from tgbot.keyboards.inline import daily_back_kb, timelist_kb, daily_ref_kb, daily_ref_only_write_kb
from tgbot.keyboards.reply import choose_jour, self_hi, work_ans_kb, sub_hi, mkb, year_hi_kb, main_menu_buttons
from tgbot.locals.load_json import data
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state, Text
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.myfuncs import to_telegraph_link, delete_commands, nice_date
from tgbot.misc.states import Jour
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, CallbackQuery


async def back(message: types.Message, state: FSMContext, session: AsyncSession):
  async with state.proxy() as datas:
    last_func = datas["last_func"]
    await last_func(message, state, session)

async def choose(message: types.Message, state: FSMContext):
  await message.answer(data.jour.choose.text, reply_markup=choose_jour)
  await Jour.choose.set()

async def myself(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'myself', random=True)

  await state.update_data(datas=q)
  await state.update_data(category='myself')
  await state.update_data(category_name=data.jour.choose.kb[0])
  state_name = Jour.work_ans
  await state.update_data(last_state=state_name)
  await state.update_data(last_func=myself)
  await message.answer(data.jour.myself.hi.text, reply_markup=self_hi)
  await Jour.work_ans.set()


async def daily(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'daily', random=True)

  await state.update_data(datas=q)
  await state.update_data(category='daily')
  await state.update_data(category_name=data.jour.choose.kb[2])
  state_name = Jour.work_ans
  await state.update_data(last_state=state_name)
  await state.update_data(last_func=daily)
  await message.answer(data.jour.daily.hi.text, reply_markup=self_hi)
  await Jour.work_ans.set()


async def myself_notif(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'daily', random=True)
  async with state.proxy() as datas:
    if len(datas['daily_data'])>0:
      q = [datas['daily_data']] + q
      datas['daily_data'] = []
  await state.update_data(datas=q)
  await state.update_data(category='daily')
  await state.update_data(category_name=data.jour.choose.kb[2])
  state_name = Jour.work_ans
  await state.update_data(last_state=state_name)
  await state.update_data(last_func=daily)
  await Jour.work_ans.set()


async def year_hi(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.jour.year.hi.text, reply_markup=mkb(data.jour.year.hi.kb))
  await state.update_data(category='year')
  await state.update_data(category_name=data.jour.choose.kb[1])
  await Jour.year_hi_.set()


async def year_to(message: types.Message, state: FSMContext, session: AsyncSession):
  q = await load_questions(session, 'year', random=False)

  await state.update_data(datas=q)
  state_name = Jour.year_hi_
  await state.update_data(last_state=state_name)
  await state.update_data(last_func=year_hi)
  await message.answer(data.jour.year.to.text, reply_markup=mkb(data.jour.year.to.kb))
  await Jour.work_ans.set()

async def year_why_1(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.jour.year.why_1.text, reply_markup=mkb(data.jour.year.why_1.kb))
  await Jour.year_why1.set()

async def year_why_2(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.jour.year.why_2.text, reply_markup=mkb(data.jour.year.why_2.kb))
  await Jour.year_why2.set()

async def year_why_3(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.jour.year.why_3.text, reply_markup=mkb(data.jour.year.why_3.kb))
  await Jour.year_why3.set()

async def year_why_4(message: types.Message, state: FSMContext, session: AsyncSession):
  await message.answer(data.jour.year.why_4.text, reply_markup=mkb(data.jour.year.why_4.kb))
  await Jour.year_hi_.set()


async def work_ans(message: types.Message, state: FSMContext, session: AsyncSession):
  async with state.proxy() as datas:
    answer = message.text
    if all((answer != i) for i in data.jour.sub.hi.kb + data.jour.sub.work_ans.kb + data.main_menu.kb + data.jour.choose.kb):
      await write_answer(
        session=session,
        telegram_id=message.from_user.id,
        answer=answer,
        question_id=datas["datas"][0]['id'],
        category=datas["datas"][0]['category']
      )
      await session.commit()
      await message.answer(f"{data.jour.sub.work_ans.after_answer} {random.choice(data.emoji)}\n\n{random.choice(data.jour.sub.work_ans.support_words)}", disable_web_page_preview=False)
      await asyncio.sleep(4)

    if data.jour.sub.hi.kb[0] != answer: #В тексте нет "к вопросам"
      datas["datas"] = datas["datas"][1:]
    if len(datas["datas"])>0:
      #if str(datas["datas"][0]['id'])=='1809':
      #  await message.answer(data.jour.year.end_8_text)
      #  time.sleep(5)
      await message.answer(datas["datas"][0]['question']+"\n\n"+data.jour.write_answer.text, reply_markup=work_ans_kb)
    else:
      await message.answer(data.jour.sub.work_ans.end, reply_markup=sub_hi)
      await state.set_state(datas["last_state"])

async def see_ans(message: types.Message, state: FSMContext, session: AsyncSession):
  state_data = await state.get_data()
  category = state_data.get("category")
  category_name = state_data.get("category_name")
  html = ""
  ans = await get_last_answers(session, telegram_id=message.from_user.id, category=category)
  if len(ans)>0:
    for row in ans:
      html += f"<i>{delete_commands(row['question'])}</i><br>"
      for i in range(len(row['array_agg'])):
        html += f"> {row['array_agg'][i]} ({nice_date(row['array_agg_1'][i])})<br>"
      html += "<br>"
    link = to_telegraph_link(page_name=category_name, html_content=html)
    await message.answer(f'<a href="{link}">{data.jour.sub.work_ans.take_ans}</a>\n\n{data.jour.sub.work_ans.and_ans}', reply_markup=IKM(inline_keyboard=[[IKB(text="Посмотреть ответы", url=link)]]))
    
    time.sleep(3)
  else:
    await message.answer(data.jour.sub.work_ans.zero)


async def see_all_ans(message: types.Message, session: AsyncSession):
  #state_data = await state.get_data()
  #category = state_data.get("category")
  #category_name = state_data.get("category_name")
  html = ""
  ans = await get_all_last_answers(session, telegram_id=message.from_user.id)
  if len(ans)>0:
    for row in ans:
      html += f"<i>{delete_commands(row['question'])}</i><br>"
      for i in range(len(row['array_agg'])):
        html += f"> {row['array_agg'][i]} ({nice_date(row['array_agg_1'][i])})<br>"
      html += "<br>"
    link = to_telegraph_link(page_name="Все Твои Ответы", html_content=html)

    await message.answer(f'<a href="{link}">{data.jour.sub.work_ans.take_ans}</a>\n\n{data.jour.sub.work_ans.and_all_ans}')
    
    time.sleep(3)
  else:
    await message.answer(data.jour.sub.work_ans.zero)




async def take_daily_ans(call: CallbackQuery, state: FSMContext, session: AsyncSession):
  text = call.message.text + "\n\n" + data.jour.write_answer.text
  await call.message.edit_text(text)
  await call.message.edit_reply_markup(reply_markup=daily_back_kb)

  await myself_notif(message=call.message, state=state, session=session)


async def back_daily_ref(call: CallbackQuery, state: FSMContext):
  await call.message.edit_reply_markup(reply_markup=None)
  await call.message.answer('Ты в главном меню', reply_markup=main_menu_buttons)
  await state.reset_state()

async def change_daily_ref_time(call: CallbackQuery, state: FSMContext):
  await call.message.answer(data.jour.notif.change_time_text, reply_markup=timelist_kb)
  await call.message.edit_reply_markup(reply_markup=daily_ref_only_write_kb)


async def select_time(call: CallbackQuery, state: FSMContext, session: AsyncSession):
  hour = call.data[4:]
  await edit_notif_user(session, telegram_id=call.from_user.id, setting=int(hour))
  await session.commit()

  await call.message.edit_reply_markup(reply_markup=None)
  await call.message.edit_text(data.jour.notif.change_time_ok_text.format(hour))


async def off_notif(call: CallbackQuery, state: FSMContext, session: AsyncSession):
  await call.message.edit_reply_markup(reply_markup=None)
  await call.message.edit_text(data.jour.notif.off_notif_text)
  await edit_notif_user(session, telegram_id=call.from_user.id, setting=None)
  await session.commit()

def register_journaling(dp: Dispatcher):
  dp.register_message_handler(choose, text=data.main_menu.kb[0])
  dp.register_message_handler(choose, text=data.jour.year.hi.kb[0][2], state=Jour.year_hi_)

  dp.register_message_handler(myself, text=data.jour.choose.kb[0], state=Jour.choose)
  dp.register_message_handler(daily, text=data.jour.choose.kb[2], state=Jour.choose)
  dp.register_message_handler(year_hi, text=data.jour.choose.kb[1], state=Jour.choose)
  dp.register_message_handler(year_hi, text=data.jour.year.why_1.kb[1][0], state=Jour.year_why1)
  dp.register_message_handler(year_to, text=data.jour.year.hi.kb[0][0], state=Jour.year_hi_)
  dp.register_message_handler(year_why_1, text=data.jour.year.hi.kb[1][0], state=Jour.year_hi_)
  dp.register_message_handler(year_why_2, state=Jour.year_why1)
  dp.register_message_handler(year_why_3, state=Jour.year_why2)
  dp.register_message_handler(year_why_4, state=Jour.year_why3)


  dp.register_message_handler(see_ans, text=data.jour.myself.hi.kb[1], state=Jour.work_ans)
  dp.register_message_handler(see_ans, text=data.jour.year.hi.kb[0][1], state=Jour.year_hi_)


  dp.register_message_handler(work_ans, text=data.jour.sub.hi.kb[0], state=Jour.work_ans)


  dp.register_message_handler(back, text=data.jour.sub.work_ans.kb[1], state=Jour.work_ans)

  dp.register_message_handler(choose, text=data.jour.myself.hi.kb[2], state=Jour.work_ans)

  dp.register_message_handler(work_ans, state=Jour.work_ans)
  dp.register_callback_query_handler(take_daily_ans, text="write_daily_ref_ans", state="*")
  dp.register_callback_query_handler(back_daily_ref, text="back_daily_ref", state=Jour.work_ans)
  dp.register_callback_query_handler(change_daily_ref_time, text="change_daily_ref_time", state="*")
  dp.register_callback_query_handler(select_time, Text(startswith='time'), state="*")
  dp.register_callback_query_handler(off_notif, text='off_notif', state="*")
  dp.register_callback_query_handler(see_all_ans, text='see_all_ans', state="*")
  dp.register_message_handler(see_all_ans, commands=["my_answers"], state="*")

