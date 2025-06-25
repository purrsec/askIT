import typer
from typer.testing import CliRunner

from askit.cli import app

runner = CliRunner()

def test_app_shows_error_without_prompt():
    """
    Test that the CLI shows a custom error and exits with a non-zero code
    when called with no command or prompt.
    """
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "Error: Prompt is required" in result.stdout

def test_version_callback():
    """
    Test that --version flag works correctly and exits cleanly.
    """
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "askit-cli version" in result.stdout 
    