# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.base.webkit.editor import Editor



class EditorsPaned(Gtk.Paned):
    def __init__(self):
        super(EditorsPaned, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_wide_handle(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("update_paned_handle", self._update_paned_handle)

    def _load_widgets(self):
        self.add1( Editor() )
        # self.add2( Editor() )

    def _update_paned_handle(self):
        rect = self.get_allocation()
        pos = -1

        try:
            size = rect.width / 2
            pos  = int(size)
        except:
            ...

        self.set_position(size)