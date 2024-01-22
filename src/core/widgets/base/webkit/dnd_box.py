# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from libs.mixins.dnd_mixin import DnDMixin



class DnDBox(DnDMixin, Gtk.DrawingArea):
    """
        DnDBox is used as a suplamentary way to Drag and Drop files because
        Webkit2.WebView is causing issues with signal intercepts and I don't
        understand how to acount for non DnD events.
    """

    def __init__(self, index):
        super(DnDBox, self).__init__()

        self.INDEX = index

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self._setup_dnd()

    def _subscribe_to_events(self):
        event_system.subscribe("listen_dnd_signals", self._listen_dnd_signals_pre)
        event_system.subscribe("pause_dnd_signals", self._pause_dnd_signals_pre)

    def _load_widgets(self):
        ...

    def _listen_dnd_signals_pre(self):
        allocation = self.get_parent().get_allocated_size().allocation
        self.size_allocate( allocation )
        self.grab_focus()

    def _pause_dnd_signals_pre(self):
        allocation = self.get_allocated_size().allocation
        allocation.widrh  = 0
        allocation.height = 0
        self.size_allocate( allocation )