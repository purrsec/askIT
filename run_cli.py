"""
This script is a dedicated entry point for PyInstaller.

It helps PyInstaller correctly resolve modules and packages when the project
uses a 'src' layout. By running PyInstaller on this script from the project
root, we ensure that the 'src' directory is properly added to the path,
allowing the 'askit' package to be found.
"""
import sys
from askit.cli import main

if __name__ == '__main__':
    main(sys.argv[1:]) 