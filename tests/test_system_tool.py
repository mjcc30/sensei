import pytest
from app.tools.system import SystemTool
from unittest.mock import patch

def test_system_tool_security():
    """Test allowlist enforcement."""
    tool = SystemTool()
    
    # Test blocked command
    result = tool.run("rm -rf /")
    assert "Error" in result
    assert "not allowed" in result

    # Test allowed command (mocked execution)
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "up 1 day"
        mock_run.return_value.stderr = ""
        
        result = tool.run("uptime")
        assert result == "up 1 day"
        mock_run.assert_called_once()

def test_system_tool_args():
    """Test argument parsing."""
    tool = SystemTool()
    
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "logs"
        mock_run.return_value.stderr = ""
        
        tool.run("podman logs mycontainer")
        # Verify arguments are split correctly
        args = mock_run.call_args[0][0]
        assert args == ["podman", "logs", "mycontainer"]
