# Python imports

# Lib imports
from .signals.ipc_signals_mixin import IPCSignalsMixin
from .signals.keyboard_signals_mixin import KeyboardSignalsMixin

# Application imports




class SignalsMixins(KeyboardSignalsMixin, IPCSignalsMixin):
    ...
