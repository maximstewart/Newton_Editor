# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class ToggleLineHighlight(Gtk.ToggleButton):
    def __init__(self):
        super(ToggleLineHighlight, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_label("Toggle Line Highlight")

    def _setup_signals(self):
        self.connect("released", self._emit_toggle_eve)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _emit_toggle_eve(self, widget, eve = None):
        event_system.emit('toggle_highlight_line', ("toggle_highlight_line",))
