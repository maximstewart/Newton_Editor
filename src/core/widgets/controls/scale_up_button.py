# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class ScaleUpButton(Gtk.Button):
    def __init__(self):
        super(ScaleUpButton, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_label("Zoom In (+)")

    def _setup_signals(self):
        self.connect("released", self._emit_scale_eve)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _emit_scale_eve(self, widget, eve = None):
        event_system.emit('scale_up_text', ("scale_up_text",))
