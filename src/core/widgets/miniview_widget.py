# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')
from gi.repository.GtkSource import Map


# Application imports



class MiniViewWidget(Map):
    def __init__(self):
        super(MiniViewWidget, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_hexpand(False)

    def _setup_signals(self):
        event_system.subscribe(f"set_source_view", self.set_source_view)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def set_source_view(self, source_view):
        self.set_view(source_view)
