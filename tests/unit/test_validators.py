import pytest
from bot.utils.validators import validate_telegram_id, validate_notification_time

def test_validate_telegram_id():
    assert validate_telegram_id(123456789)
    assert not validate_telegram_id(-1)

def test_validate_notification_time():
    assert validate_notification_time("09:00")
    assert not validate_notification_time("25:00") 