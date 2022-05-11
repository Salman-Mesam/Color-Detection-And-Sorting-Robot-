#!/usr/bin/env python3

"""
File containing unit and integration tests for logic that does not require the robot hardware
and can therefore be run on a computer.
"""

# change these imports based on your actual implementation

from logic import get_bin_for_color

import pytest


def test_pytest_is_working():
    """
    Trivial test to ensure pytest is installed and configured correctly. This test should be
    detected by the pytest framework and it should pass.
    """
    assert True


def test_get_bin_for_color():
    """
    Test that the correct bin is returned for a given color.
    """
    # success cases (valid input)
    assert get_bin_for_color("Red") == 1
    assert get_bin_for_color("Green") == 2
    assert get_bin_for_color("Blue") == 3

    # failure cases (invalid input), check that exception of the correct type is raised
    for bad_color in ["Black", "Unknown", None]:
        with pytest.raises(ValueError):
            get_bin_for_color(bad_color)


if __name__ == "__main__":
    print("To run the tests, first run `pipenv` with the project's virtual environment activated. "
          "This can be done automatically in Visual Studio Code by running the relevant task "
          "accessed from the Command Palette (Ctrl+Shift+P). "
          "Then, run `pytest` on the command line or use the testing option (🧪) in Visual Studio Code.")
