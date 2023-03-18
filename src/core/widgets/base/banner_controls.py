# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..controls.theme_button import ThemeButton
from ..controls.toggle_line_highlight import ToggleLineHighlight
from ..controls.scale_up_button import ScaleUpButton
from ..controls.scale_down_button import ScaleDownButton



class BannerControls(Gtk.Box):
    def __init__(self):
        super(BannerControls, self).__init__()


        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(0)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self.add(ToggleLineHighlight())
        self.add(ScaleDownButton())
        self.add(ScaleUpButton())
        self.pack_end(ThemeButton(), False, False, 0)
