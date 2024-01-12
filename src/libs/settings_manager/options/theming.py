# Python imports
from dataclasses import dataclass

# Lib imports

# Application imports


@dataclass
class Theming:
    transparency: int  = 62
    default_zoom: int  = 12
    syntax_theme: str  = "tango"
    success_color: str = "#88cc27"
    warning_color: str = "#ffa800"
    error_color: str   = "#ff0000"
