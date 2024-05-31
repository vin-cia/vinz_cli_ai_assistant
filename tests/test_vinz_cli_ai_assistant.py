import pytest
import shelve
from unittest.mock import patch, MagicMock, ANY, call
from vinz_cli_ai_assistant import get_answer_from_openai, handle_question, install_script, uninstall_script, CACHE_FILE, \
    INSTALL_PATH


@pytest.fixture
def mock_cache():
    with shelve.open(CACHE_FILE, flag='n') as db:
        yield db


@pytest.fixture
def mock_client():
    client_mock = MagicMock()
    return client_mock


@patch("vinz_cli_ai_assistant.shelve.open")
def test_get_answer_from_openai_cached(mock_shelve_open, mock_cache, mock_client):
    mock_cache["test question"] = "cached answer"
    mock_shelve_open.return_value.__enter__.return_value = mock_cache

    answer = get_answer_from_openai("test question", mock_cache, "gpt-3.5-turbo", mock_client)
    assert answer == "cached answer"
    mock_client.chat.completions.create.assert_not_called()


@patch("vinz_cli_ai_assistant.shelve.open")
def test_get_answer_from_openai_api(mock_shelve_open, mock_cache, mock_client):
    mock_shelve_open.return_value.__enter__.return_value = mock_cache

    mock_message = MagicMock()
    mock_message.content.strip.return_value = "api answer"
    mock_choice = MagicMock(message=mock_message)
    mock_client.chat.completions.create.return_value.choices = [mock_choice]

    answer = get_answer_from_openai("new question", mock_cache, "gpt-3.5-turbo", mock_client)
    assert answer == "api answer"
    mock_client.chat.completions.create.assert_called_once()


@patch("vinz_cli_ai_assistant.shelve.open")
@patch("vinz_cli_ai_assistant.get_answer_from_openai")
def test_handle_question(mock_get_answer_from_openai, mock_shelve_open, mock_cache, mock_client):
    mock_shelve_open.return_value.__enter__.return_value = mock_cache

    mock_get_answer_from_openai.return_value = "handled answer"
    answer = handle_question("another question", "gpt-3.5-turbo", mock_client)
    assert answer == "handled answer"
    mock_get_answer_from_openai.assert_called_once_with("another question", ANY, "gpt-3.5-turbo", mock_client)


@patch("vinz_cli_ai_assistant.shutil.copy")
@patch("vinz_cli_ai_assistant.os.chmod")
@patch("vinz_cli_ai_assistant.os.path.abspath")
@patch("vinz_cli_ai_assistant.print")
def test_install_script(mock_print, mock_abspath, mock_chmod, mock_copy):
    mock_abspath.return_value = "/path/to/script/vinz_cli_ai_assistant.py"

    install_script()

    mock_copy.assert_called_once_with("/path/to/script/vinz_cli_ai_assistant.py", INSTALL_PATH)
    mock_chmod.assert_called_once_with(INSTALL_PATH, 0o755)
    mock_print.assert_called_once_with(f"Script has been installed to {INSTALL_PATH} and is now executable as 'v'.")


@patch("vinz_cli_ai_assistant.os.path.exists")
@patch("vinz_cli_ai_assistant.os.remove")
@patch("vinz_cli_ai_assistant.print")
def test_uninstall_script(mock_print, mock_remove, mock_exists):
    mock_exists.side_effect = lambda x: x in [INSTALL_PATH, CACHE_FILE]

    uninstall_script()

    expected_calls = [call(INSTALL_PATH), call(CACHE_FILE)]
    mock_remove.assert_has_calls(expected_calls, any_order=True)
    mock_print.assert_has_calls([
        call(f"Script has been removed from {INSTALL_PATH}."),
        call(f"Cache file {CACHE_FILE} has been removed.")
    ])


@patch("vinz_cli_ai_assistant.os.path.exists")
@patch("vinz_cli_ai_assistant.os.remove")
@patch("vinz_cli_ai_assistant.print")
def test_uninstall_script_no_cache(mock_print, mock_remove, mock_exists):
    mock_exists.side_effect = lambda x: x == INSTALL_PATH

    uninstall_script()

    mock_remove.assert_called_once_with(INSTALL_PATH)
    mock_print.assert_any_call(f"Script has been removed from {INSTALL_PATH}.")
    mock_print.assert_any_call(f"Cache file {CACHE_FILE} not found.")


@patch("vinz_cli_ai_assistant.os.path.exists")
@patch("vinz_cli_ai_assistant.print")
def test_uninstall_script_no_install(mock_print, mock_exists):
    mock_exists.return_value = False

    uninstall_script()

    mock_print.assert_any_call(f"Script not found at {INSTALL_PATH}.")
    mock_print.assert_any_call(f"Cache file {CACHE_FILE} not found.")
