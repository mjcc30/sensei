import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch
from app.main import app
from app.core.memory import Memory

runner = CliRunner()

@pytest.fixture
def mock_memory():
    with patch('app.main.Memory') as MockMemory:
        mock_instance = MockMemory.return_value
        yield mock_instance

def test_history_list_sessions(mock_memory):
    mock_memory.list_sessions.return_value = [
        ("id1", "Chat 1", "2025-01-01"),
        ("id2", "Chat 2", "2025-01-02"),
    ]
    result = runner.invoke(app, ["history"])
    assert result.exit_code == 0
    assert "Recent Conversation Sessions" in result.stdout
    assert "id1" in result.stdout
    assert "Chat 1" in result.stdout
    mock_memory.list_sessions.assert_called_once()

def test_history_show_session(mock_memory):
    mock_memory.get_history.return_value = [
        {"role": "user", "parts": ["Hello"]},
        {"role": "model", "parts": ["Hi there!"]},
    ]
    result = runner.invoke(app, ["history", "--session-id", "test_id"])
    print(f"\nSTDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    assert result.exit_code == 0
    assert "History for session: test_id" in result.stdout
    assert "user: Hello" in result.stdout
    assert "model: Hi there!" in result.stdout
    mock_memory.get_history.assert_called_once_with(session_id="test_id")

def test_history_no_sessions(mock_memory):
    mock_memory.list_sessions.return_value = []
    result = runner.invoke(app, ["history"])
    print(f"\nSTDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    assert result.exit_code == 0
    assert "No sessions found." in result.stdout

def test_clear_all_history_confirmed(mock_memory):
    with patch('typer.confirm', return_value=True):
        result = runner.invoke(app, ["clear", "--all"])
        print(f"\nSTDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        assert result.exit_code == 0
        assert "All conversation history cleared." in result.stdout
        mock_memory.clear_all_history.assert_called_once()

def test_clear_all_history_cancelled(mock_memory):
    with patch('typer.confirm', return_value=False):
        result = runner.invoke(app, ["clear", "--all"])
        print(f"\nSTDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        assert result.exit_code == 0
        assert "Operation cancelled." in result.stdout
        mock_memory.clear_all_history.assert_not_called()

def test_clear_session_confirmed(mock_memory):
    with patch('typer.confirm', return_value=True):
        result = runner.invoke(app, ["clear", "--session-id", "test_id"])
        print(f"\nSTDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        assert result.exit_code == 0
        assert "Session test_id cleared." in result.stdout
        mock_memory.clear_session.assert_called_once_with("test_id")

def test_clear_session_cancelled(mock_memory):
    with patch('typer.confirm', return_value=False):
        result = runner.invoke(app, ["clear", "--session-id", "test_id"])
        print(f"\nSTDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        assert result.exit_code == 0
        assert "Operation cancelled." in result.stdout
        mock_memory.clear_session.assert_not_called()

def test_clear_no_option():
    result = runner.invoke(app, ["clear"])
    print(f"\nSTDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")
    assert result.exit_code == 0
    assert "Please specify --all or --session <ID> to clear history." in result.stdout
