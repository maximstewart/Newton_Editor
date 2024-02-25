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

    def _open_files(self, widget = None, eve = None, fpath = None):
        start_dir = None
        gfile     = Gio.File.new_for_path(fpath)
        _gfiles   = []

        if gfile.query_exists():
            start_dir = gfile.get_parent()

        chooser = Gtk.FileChooserDialog("Open File(s)...", None,
                                        Gtk.FileChooserAction.OPEN,
                                        (
                                            Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN,
                                            Gtk.ResponseType.OK
                                        )
        )

        chooser.set_select_multiple(True)

        try:
            folder = widget.get_current_file().get_parent() if not start_dir else start_dir 
            chooser.set_current_folder( folder.get_path() )
        except Exception as e:
            ...

        response = chooser.run()
        if not response == Gtk.ResponseType.OK:
            chooser.destroy()
            return _gfiles

        filenames = chooser.get_filenames()
        if not filenames:
            chooser.destroy()
            return _gfiles

        for file in filenames:
            path    = file if os.path.isabs(file) else os.path.abspath(file)
            _gfiles.append( Gio.File.new_for_path(path) )

        chooser.destroy()

        return _gfiles
