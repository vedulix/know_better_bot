from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.reply import s1, s2, s3, s4
from tgbot.locals.load_json import data
from tgbot.misc.states import Start



async def start(message: Message, state: FSMContext):
    await message.answer(data.start.hi.text, reply_markup=s1)
    config = message.bot.get("config")
    admin_ids = config.tg_bot.admin_ids
    await message.bot.send_message(chat_id=admin_ids[0], text=f"@{message.from_user.username} {message.from_user.id}")
    await Start.s1.set()


async def start_2(message: Message, state: FSMContext):
    await message.answer(data.start.ask_question_how.text, reply_markup=s2)
    await Start.s2.set()


async def start_3(message: Message, state: FSMContext):
    await message.answer(data.start.ask_question_for_whom.text, reply_markup=s3)
    await Start.s3.set()


async def start_4(message: Message, state: FSMContext):
    await message.answer(data.start.to_main_menu.text, reply_markup=s4)
    await state.reset_state()


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(start_2, state=Start.s1)
    dp.register_message_handler(start_3, state=Start.s2)
    dp.register_message_handler(start_4, state=Start.s3)

