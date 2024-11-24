import pytest
from tgbot.locals.load_json import data

async def test_localization_integration():
    """
    Тестирует интеграцию локализации:
    - Загрузка текстов
    - Проверка наличия ключевых сообщений
    """
    # Assert
    assert data.main_menu.text is not None
    assert data.jour.choose.text is not None
    assert data.jour.notif.change_time_text is not None 