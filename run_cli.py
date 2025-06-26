"""
This script is a dedicated entry point for PyInstaller.

It helps PyInstaller correctly resolve modules and packages when the project
uses a 'src' layout. By running PyInstaller on this script from the project
root, we ensure that the 'src' directory is properly added to the path,
allowing the 'askit' package to be found.
"""
import sys
from askit.cli import main
from typer import Exit as TyperExit

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except TyperExit:
        # This is a clean exit, typically from the user pressing Ctrl+C.
        # We can exit gracefully without showing a traceback.
        pass 