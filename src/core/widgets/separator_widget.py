# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class Separator(Gtk.Separator):
    def __init__(self, id: str = None, ORIENTATION: int = 0):
        super(Separator, self).__init__()

        builder = settings_manager.get_builder()
        if id:
            builder.expose_object(id, self)

        self.ORIENTATION = ORIENTATION
        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        # HORIZONTAL = 0, VERTICAL = 1
        self.set_orientation(self.ORIENTATION)


    def _setup_signals(self):
        ...

    def _load_widgets(self):
        ...
