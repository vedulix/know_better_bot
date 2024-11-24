import pytest
from bot.utils.config import load_config

def test_load_config():
    test_config = {
        "BOT_TOKEN": "test_token",
        "DB_HOST": "localhost"
    }
    config = load_config(test_config)
    assert config.BOT_TOKEN == "test_token"
    assert config.DB_HOST == "localhost" 