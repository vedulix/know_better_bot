from tgbot.locals.load_json import data
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state, Text
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.myfuncs import to_telegraph_link, delete_commands, nice_date
from tgbot.misc.states import Jour
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, CallbackQuery


async def thank_ans(call: CallbackQuery):
    await call.answer(data.rest.please, show_alert=False)
    await call.message.edit_reply_markup(reply_markup=None)

def register_rest(dp: Dispatcher):
    dp.register_callback_query_handler(thank_ans, text="weekly_idea_thank_click", state="*")
