# Common Types
# Cal Wing

from typing import NamedTuple, TypedDict

# Generic Number Type
type Numeric = int | float

type KnobCompIds = tuple[
    int | None, # Outer Oval Id
    int | None, # Inner Oval Id
    int | None  # Text Label
]

# Knob Formatting
class KnobFormatOptions(NamedTuple):
    outer_radius: int = 10
    outer_colour: str = "#c2d6d6"
    inner_radius: int = 5
    inner_colour: str = "#5c8a8a"
    line_width:   int = 2
    show_text_label: bool | None = None

# Knob Info Dictionary
class KnobInfo(TypedDict):
    ids: KnobCompIds
    norm_pos: float
    value: float
    fmt_options: KnobFormatOptions

# Line Formatting
class LineFormatOptions(NamedTuple):
    colour: str = "#476b6b"
    width:  int = 3