from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards.reply import main_menu_buttons
from tgbot.locals.load_json import data


async def to_main_menu(message: types.Message, state: FSMContext):
  await message.answer(data.main_menu.text, reply_markup=main_menu_buttons)
  await state.reset_state()


def register_commands(dp: Dispatcher):
  dp.register_message_handler(to_main_menu, commands=["menu", "help"], state="*")
