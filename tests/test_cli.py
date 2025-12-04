import pytest
import sys
import os
from typer.testing import CliRunner
from unittest.mock import MagicMock, AsyncMock, patch

# Hack pour inclure le dossier parent dans le path (Prioritaire)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

runner = CliRunner()

def test_ask_command_missing_key():
    """Test that the CLI complains if API key is missing."""
    # On s'assure que l'env est vide
    with patch.dict('os.environ', {}, clear=True):
        result = runner.invoke(app, ["ask", "Hello"])
        assert result.exit_code == 1
        assert "GEMINI_API_KEY not found" in result.stdout

def test_ask_command_success(mocker):
    """Test a successful CLI call with mocked Orchestrator."""
    # Mock de l'Orchestrator
    mock_orch = MagicMock()
    mock_orch.handle_request = AsyncMock(return_value="[MockAgent] This is a mocked response.")
    
    # On patch la classe Orchestrator dans main.py pour qu'elle renvoie notre mock
    mocker.patch("app.main.Orchestrator", return_value=mock_orch)

    # On lance la commande avec une fausse clé
    result = runner.invoke(app, ["ask", "Hello", "--key", "fake-key"])
    
    # Vérifications
    assert result.exit_code == 0
    assert "This is a mocked response" in result.stdout
    assert "MockAgent" in result.stdout
