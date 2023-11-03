"""
Runtime utilities.
"""

import sys


def has_arg(arg):
    """Check if a command line argument is present."""
    return arg in sys.argv
