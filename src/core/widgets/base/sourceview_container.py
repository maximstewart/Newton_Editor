# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..tab_header_widget import TabHeaderWidget
from .sourceview.source_view import SourceView



class SourceViewContainer(Gtk.ScrolledWindow):
    def __init__(self, close_tab):
        super(SourceViewContainer, self).__init__()

        self._close_tab   = close_tab
        self._source_view = None
        self._tab_widget  = None

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self._source_view = SourceView()
        self._tab_widget  = TabHeaderWidget(self, self._source_view, self._close_tab)
        self.add(self._source_view)

    def get_tab_widget(self):
        return self._tab_widget

    def get_source_view(self):
        return self._source_view
