import pytest
from bot.utils.formatters import format_question

def test_format_question():
    question = {
        "text": "Как ваши дела?",
        "category": "daily"
    }
    formatted = format_question(question)
    assert "Как ваши дела?" in formatted
    assert "[daily]" in formatted 