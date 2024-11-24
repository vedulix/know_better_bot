import pytest
from bot.utils.answers import process_answer

def test_process_answer_valid():
    answer = "Это мой тестовый ответ"
    result = process_answer(answer)
    assert result.is_valid
    assert len(result.text) == len(answer)
    assert result.error is None

def test_process_answer_empty():
    answer = ""
    result = process_answer(answer)
    assert not result.is_valid
    assert result.error == "Answer cannot be empty" 