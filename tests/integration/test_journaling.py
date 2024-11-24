import pytest
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.handlers.journaling import work_ans
from tgbot.infrastucture.database.functions.users import get_last_answers, create_user
from tgbot.misc.states import Jour

async def test_write_answer_integration(message_mock, state_mock, session: AsyncSession):
    """
    Тестирует полный цикл записи ответа:
    - Получение сообщения
    - Сохранение в БД
    - Проверка сохраненного ответа
    """
    # Arrange
    telegram_id = message_mock.from_user.id
    answer_text = "Test answer"
    message_mock.text = answer_text
    
    # Create test user
    await create_user(
        session,
        telegram_id=telegram_id,
        full_name=message_mock.from_user.full_name,
        username=message_mock.from_user.username,
        language_code=message_mock.from_user.language_code
    )
    await session.commit()
    
    # Setup state
    await state_mock.set_state(Jour.work_ans)
    await state_mock.set_data({
        "datas": [{
            "id": 1,
            "category": "daily",
            "question": "Test question"
        }]
    })
    
    # Act
    await work_ans(message_mock, state_mock, session)
    
    # Assert
    saved_answers = await get_last_answers(
        session,
        telegram_id=telegram_id,
        category='daily'
    )
    assert len(saved_answers) == 1
    assert saved_answers[0]['answer'] == answer_text 