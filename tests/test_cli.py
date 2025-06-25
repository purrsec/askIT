import sys
from unittest.mock import patch

import pytest

from askit import cli


def test_main_no_args_shows_help(capsys):
    """
    Test that running with no arguments shows the help message, not an error.
    """
    with patch.object(sys, 'argv', ['askit-cli']):
        cli.main() # Test the actual entrypoint

    captured = capsys.readouterr()
    assert "Usage:" in captured.out
    assert "Error:" not in captured.err


def test_main_version_flag(capsys):
    """
    Test that --version flag works correctly and exits cleanly via the main entrypoint.
    """
    with patch.object(sys, 'argv', ['askit-cli', '--version']):
        with pytest.raises(SystemExit) as e:
            cli.main()
        # Check that it exits cleanly
        assert e.value.code == 0

    captured = capsys.readouterr()
    assert "askit-cli version" in captured.out 
    