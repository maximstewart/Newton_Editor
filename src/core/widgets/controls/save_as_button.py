# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class SaveAsButton(Gtk.Button):
    def __init__(self):
        super(SaveAsButton, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_label("Save As")
        self.set_image( Gtk.Image.new_from_icon_name("gtk-save-as", 4) )
        self.set_always_show_image(True)
        self.set_image_position(1) # Left - 0, Right = 1
        self.set_hexpand(False)
        self.set_sensitive(False)

    def _setup_signals(self):
        self.connect("released", self._emit_save_as_eve)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _emit_save_as_eve(self, widget, eve = None):
        event_system.emit('keyboard_save_file')
