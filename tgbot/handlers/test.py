from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastucture.database.functions.users import get_last_answers


async def admin_test(message: Message, state: FSMContext, session: AsyncSession):
    await get_last_answers(session, telegram_id=message.from_user.id, category='myself', )

def register_test(dp: Dispatcher):
    dp.register_message_handler(admin_test, commands=["test"], state="*", is_test=True)
