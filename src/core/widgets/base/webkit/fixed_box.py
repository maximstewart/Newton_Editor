# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .dnd_box import DnDBox
from .ace_editor import AceEditor



class FixedBox(Gtk.Fixed):
    """
        In order for the desired Drag and Drop we need to stack a widget
        (aka our DnDBox) above the Webkit2.Webview to intercept and proxy accordingly.
    """

    def __init__(self, index):
        super(FixedBox, self).__init__()

        self.INDEX = index

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.connect("realize", self._on_realize)
        self.connect("size-allocate", self._on_size_allocate)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.ace_editor = AceEditor(self.INDEX)
        self.dnd_box    = DnDBox(self.INDEX)

        self.add( self.ace_editor )
        self.add( self.dnd_box )

    def _on_realize(self, wiodget):
        self._setup_styling()

    def _on_size_allocate(self, widget, allocation):
        self.ace_editor.size_allocate( allocation )