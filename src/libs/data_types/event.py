# Python imports
from dataclasses import dataclass, field

# Lib imports
import gi

# Application imports



@dataclass
class Event:
    topic: str
    target: str
    content: str
