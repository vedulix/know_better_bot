from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.locals.load_json import data


async def problem(message: types.Message, state: FSMContext):
  await message.answer(data.problem.text)


def register_problem(dp: Dispatcher):
  dp.register_message_handler(problem, state="*")
