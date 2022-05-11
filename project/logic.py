"""
Module for computations that do not require robot hardware and can therefore be tested on a computer.

It is often faster to test these computations on a computer than on the robot.
"""

# The brick and sound modules must NOT be imported here, but other imports are allowed


# This is a trivial function included here as an example. Feel free to modify or remove it
def get_bin_for_color(color: str) -> int:
    """
    Return the bin number for the given color.

    Red -> 1, Green -> 2, Blue -> 3 (other colors omitted for simplicity)
    """
    BIN_FOR: dict[str, int] = {"Red": 1, "Green": 2, "Blue": 3}
    if color not in BIN_FOR:
        raise ValueError(f"No bin for color {color}")
    return BIN_FOR[color]
