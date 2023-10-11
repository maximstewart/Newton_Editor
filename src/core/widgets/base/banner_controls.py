# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..controls.open_file_button import OpenFileButton
from ..controls.save_as_button import SaveAsButton
from ..controls.scale_up_button import ScaleUpButton
from ..controls.scale_down_button import ScaleDownButton
from ..controls.toggle_line_highlight import ToggleLineHighlight
from ..controls.theme_button import ThemeButton



class BannerControls(Gtk.Box):
    def __init__(self):
        super(BannerControls, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()
        self.hide()


    def _setup_styling(self):
        self.set_orientation(0)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("tggl_top_main_menubar", self._tggl_top_main_menubar)

    def _load_widgets(self):
        self.pack_start(OpenFileButton(), False, False, 0)
        self.pack_start(SaveAsButton(), False, False, 0)

        center_box = Gtk.ButtonBox()
        center_box.add(ScaleUpButton())
        center_box.add(ScaleDownButton())
        center_box.add(ToggleLineHighlight())
        center_box.set_margin_left(15)
        center_box.set_margin_right(15)
        self.set_center_widget(center_box)

        self.pack_end(ThemeButton(), False, False, 0)


    def _tggl_top_main_menubar(self):
        self.show() if not self.is_visible() else self.hide()
