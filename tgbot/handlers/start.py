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



def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(start_1, state=Start.s1)
    dp.register_message_handler(start_problem, state=Start)

