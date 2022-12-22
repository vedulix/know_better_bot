import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class TestFilter(BoundFilter):
    key = 'is_test'

    def __init__(self, is_test: typing.Optional[bool] = None):
        self.is_test = is_test

    async def check(self, obj):
        if self.is_test is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.from_user.id in config.tg_bot.test_ids) == self.is_test

