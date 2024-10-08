from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastucture.database.functions.users import create_user
from tgbot.infrastucture.database.models.users import User
from tgbot.keyboards.reply import mkb
from tgbot.locals.load_json import data
from tgbot.misc.states import Start



async def start(message: Message, state: FSMContext, session: AsyncSession):

    parts = message.text.split()
    if len(parts) > 1:
        deep_link = parts[1]
    else:
        deep_link = None
    user = await session.get(User, message.from_user.id)
    if not user:
        await create_user(
            session,
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code,
            deep_link=deep_link
        )
        await session.commit()
    if deep_link is not None:
        stmt = update(User).where(User.telegram_id == message.from_user.id).values(deep_link=deep_link)
        await session.execute(stmt)
        await session.commit()
    #user = await session.get(User, message.from_user.id)
    await message.answer(data.start.hi.text, reply_markup=mkb(data.start.hi.kb))
    await Start.s1.set()


async def start_1(message: Message, state: FSMContext):
    await message.answer(data.start._1.text.format(message.from_user.first_name), reply_markup=mkb(data.start._1.kb))
    await Start.s2.set()


async def start_2(message: Message, state: FSMContext):
    await message.answer(data.start._2.text, reply_markup=mkb(data.start._2.kb))
    await Start.s3.set()


async def start_3(message: Message, state: FSMContext):
    await message.answer(data.start._3.text, reply_markup=mkb(data.start._3.kb))
    await Start.s4.set()


async def start_4(message: Message, state: FSMContext):
    await message.answer(data.start._4.text, reply_markup=mkb(data.start._4.kb))
    await Start.s5.set()

async def start_5(message: Message, state: FSMContext):
    await message.answer(data.start._5.text, reply_markup=mkb(data.start._5.kb))
    await Start.s6.set()

async def start_6(message: Message, state: FSMContext):
    await message.answer(data.start._6.text, reply_markup=mkb(data.start._6.kb))
    await Start.s7.set()

async def start_7(message: Message, state: FSMContext):
    await message.answer(data.start._7.text, reply_markup=mkb(data.start._8.kb))
    await Start.s9.set()


"""
async def start_8(message: Message, state: FSMContext):
    await message.answer(data.start._8.text, reply_markup=mkb(data.start._8.kb))
    await Start.s9.set()
"""

async def last(message: Message, state: FSMContext):
    await message.answer(data.start.last.text, reply_markup=mkb(data.main_menu.new_kb))
    await state.reset_state()


async def start_problem(message: Message, state: FSMContext):
    await message.answer(data.start.problem_text, reply_markup=mkb(data.start._3.kb))



def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(start_1, state=Start.s1)
    dp.register_message_handler(start_2, text=data.start._1.kb[0][1], state=Start.s2)
    dp.register_message_handler(start_3, state=Start.s3)
    dp.register_message_handler(start_3, text=data.start._1.kb[0][0], state=Start.s2)
    dp.register_message_handler(start_2, state=Start.s2)
    dp.register_message_handler(start_4, state=Start.s4)
    dp.register_message_handler(start_5, state=Start.s5)
    dp.register_message_handler(start_6, state=Start.s6)
    dp.register_message_handler(start_7, state=Start.s7)
    #dp.register_message_handler(start_8, state=Start.s8)
    dp.register_message_handler(last, state=Start.s9)

    dp.register_message_handler(start_problem, state=Start)
