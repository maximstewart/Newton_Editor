# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..widgets.separator_widget import Separator
from ..widgets.miniview_widget import MiniViewWidget
from ..widgets.base.notebook.editor_notebook import EditorNotebook



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
        self.add1(EditorNotebook())
        self.add2(EditorNotebook())

    def _update_paned_handle(self):
        rect = self.get_allocation()
        pos = -1

        try:
            size = rect.width / 2
            pos  = int(size)
        except:
            ...

        self.set_position(size)


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
        self.add(Separator("separator_left"))
        self.add(EditorsPaned())
        self.add(Separator("separator_right"))
        self.add(miniview)