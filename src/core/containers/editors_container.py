# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.separator_widget import Separator
from ..widgets.miniview_widget import MiniViewWidget
from .editors_paned import EditorsPaned



class EditorsContainer(Gtk.Box):
    def __init__(self):
        super(EditorsContainer, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        miniview = MiniViewWidget()
        miniview.hide()

        self.add(Separator("separator_left"))
        self.add(EditorsPaned())
        self.add(Separator("separator_right"))
        self.add(miniview)