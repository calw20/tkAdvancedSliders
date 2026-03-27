# Common Types
# Cal Wing

from typing import NamedTuple

type Numeric = int | float

# Head Bubble Formatting
class KnobFormatOptions(NamedTuple):
    outer_radius: int = 10
    outer_colour: str = "#c2d6d6"
    inner_radius: int = 5
    inner_colour: str = "#5c8a8a"
    line_width:   int = 2
    show_text_label: bool | None = None

# Line Formatting
class LineFormatOptions(NamedTuple):
    colour: str = "#476b6b"
    width:  int = 3