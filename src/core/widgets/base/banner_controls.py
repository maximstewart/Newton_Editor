# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
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
        # styles_chooser_button = GtkSource.StyleSchemeChooserButton()

        self.add(ToggleLineHighlight())
        # self.add(styles_chooser_button)
        self.add(ScaleUpButton())
        self.add(ScaleDownButton())
