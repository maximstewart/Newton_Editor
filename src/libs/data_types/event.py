# Python imports
from dataclasses import dataclass, field

# Lib imports

# Application imports



@dataclass
class Event:
    topic: str
    ftype: str
    fhash: str
    fpath: str
    content: str
    originator: int = -1