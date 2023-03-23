# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio

# Application imports



class OpenFileButton(Gtk.Button):
    """docstring for OpenFileButton."""

    def __init__(self):
        super(OpenFileButton, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_label("Open File(s)...")
        self.set_image( Gtk.Image.new_from_icon_name("gtk-open", 4) )
        self.set_always_show_image(True)
        self.set_image_position(1) # Left - 0, Right = 1
        self.set_hexpand(False)

    def _setup_signals(self):
        self.connect("button-release-event", self._open_files)

    def _subscribe_to_events(self):
        event_system.subscribe("open_files", self._open_files)

    def _load_widgets(self):
        ...

    def _open_files(self, widget = None, eve = None):
        chooser = Gtk.FileChooserDialog("Open File...", None,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            if filename:
                path   = filename if os.path.isabs(filename) else os.path.abspath(filename)
                _gfile = Gio.File.new_for_path(path)
                event_system.emit("keyboard_open_file", (_gfile,))

        chooser.destroy()
