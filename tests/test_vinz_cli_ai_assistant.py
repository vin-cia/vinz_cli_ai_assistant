import pytest
import shelve
from unittest.mock import patch, MagicMock, ANY
from vinz_cli_ai_assistant import get_answer_from_openai, handle_question, CACHE_FILE

@pytest.fixture
def mock_cache():
    with shelve.open(CACHE_FILE, flag='n') as db:
        yield db

@patch("vinz_cli_ai_assistant.client.chat.completions.create")
def test_get_answer_from_openai_cached(mock_create, mock_cache):
    mock_cache["test question"] = "cached answer"
    answer = get_answer_from_openai("test question", mock_cache, "gpt-3.5-turbo")
    assert answer == "cached answer"
    mock_create.assert_not_called()

@patch("vinz_cli_ai_assistant.client.chat.completions.create")
def test_get_answer_from_openai_api(mock_create, mock_cache):
    mock_create.return_value = MagicMock(choices=[MagicMock(message=MagicMock(content="api answer"))])
    answer = get_answer_from_openai("new question", mock_cache, "gpt-3.5-turbo")
    assert answer == "api answer"
    mock_create.assert_called_once()

@patch("vinz_cli_ai_assistant.get_answer_from_openai")
def test_handle_question(mock_get_answer_from_openai, mock_cache):
    mock_get_answer_from_openai.return_value = "handled answer"
    answer = handle_question("another question", "gpt-3.5-turbo")
    assert answer == "handled answer"
    mock_get_answer_from_openai.assert_called_once_with("another question", ANY, "gpt-3.5-turbo")
