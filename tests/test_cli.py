import typer
from typer.testing import CliRunner

from askit.cli import app

runner = CliRunner()

def test_app_runs_and_shows_help():
    """
    Test that the CLI runs, shows help, and exits with a non-zero code
    when called with no command, as Typer requires a subcommand.
    """
    result = runner.invoke(app)
    assert result.exit_code != 0  # It should exit with an error code
    assert "Usage" in result.stdout
    assert "Missing command" in result.stdout

def test_version_callback():
    """
    Test that --version flag works correctly.
    Typer's version callback exits the program, so we expect an exit code of 0.
    """
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    # We can't easily get the version from pyproject.toml here,
    # but we can check if it prints something that looks like a version.
    assert "askit-cli version" in result.stdout 