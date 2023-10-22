# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TransparencyScale(Gtk.Scale):
    def __init__(self):
        super(TransparencyScale, self).__init__()


        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_digits(0)
        self.set_value_pos(Gtk.PositionType.RIGHT)
        self.add_mark(50.0, Gtk.PositionType.TOP, "50%")


    def _setup_signals(self):
        self.connect("value-changed", self._update_transparency)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        adjust = self.get_adjustment()
        adjust.set_lower(0)
        adjust.set_upper(99)
        adjust.set_value(settings.theming.transparency)
        adjust.set_step_increment(1.0)

    def _update_transparency(self, range):
        event_system.emit("remove_transparency")
        tp = int(range.get_value())
        settings.theming.transparency = tp
        event_system.emit("update_transparency")
