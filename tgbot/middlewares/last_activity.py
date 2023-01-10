from datetime import datetime

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from sqlalchemy import update

from tgbot.infrastucture.database.functions.users import create_user
from tgbot.infrastucture.database.models.users import User


class DAUMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool


    async def on_process_message(self, message: types.Message, *args, **kwargs):
        # Get user_id from the incoming message
        telegram_id = message.from_user.id
        session = self.session_pool()

        user = await session.get(User, message.from_user.id)
        if not user:
            await create_user(
                session,
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
            )
            await session.commit()
        else:
            # If the user is in the database, update their "last_activity" field
            stmt = update(User).where(User.telegram_id == telegram_id).values(last_activity=datetime.now())
            await session.execute(stmt)
            await session.commit()
        await session.close()