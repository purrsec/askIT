import typer
from typer.testing import CliRunner

from askit.cli import app

runner = CliRunner()

def test_app_runs():
    """
    Test that the CLI runs without crashing when called with no command.
    """
    result = runner.invoke(app)
    assert result.exit_code == 0
    # A basic Typer app with no command returns a help message.
    # We can check for a known part of that help message.
    assert "Usage" in result.stdout
    assert "Options" in result.stdout

def test_version_callback(mocker):
    """
    Test that --version flag works correctly.
    """
    # Typer's version callback exits the program, so we expect an exit code of 0.
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    # We can't easily get the version from pyproject.toml here,
    # but we can check if it prints something that looks like a version.
    assert "askit-cli version" in result.stdout 