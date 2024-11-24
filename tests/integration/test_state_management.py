import pytest
from aiogram import types

from tgbot.handlers.journaling import choose
from tgbot.misc.states import Jour

async def test_state_management_integration(message_mock, state_mock):
    """
    Тестирует управление состояниями:
    - Переход между состояниями
    - Сохранение данных
    - Восстановление состояния
    """
    # Act
    await choose(message_mock, state_mock)
    state_data = await state_mock.get_data()
    current_state = await state_mock.get_state()
    
    # Assert
    assert current_state == Jour.choose
    assert state_data is not None 