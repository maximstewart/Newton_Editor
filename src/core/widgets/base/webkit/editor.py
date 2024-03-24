# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ....controllers.files_controller import FilesController
from .fixed_box import FixedBox



class Editor(Gtk.Box):
    ccount = 0

    def __new__(cls, *args, **kwargs):
        obj        = super(Editor, cls).__new__(cls)
        cls.ccount += 1

        return obj

    def __init__(self):
        super(Editor, self).__init__()

        self.INDEX = self.ccount

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_orientation( Gtk.Orientation.VERTICAL )

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        FilesController(self.INDEX)

    def _load_widgets(self):
        self.add( FixedBox(self.INDEX) )
