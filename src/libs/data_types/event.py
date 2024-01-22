# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi

# Application imports



@dataclass
class Event:
    topic: str
    ftype: str
    fhash: str
    fpath: str
    content: str
    originator: int = -1