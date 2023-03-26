# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports
from .controller_data import ControllerData
from .core_widget import CoreWidget
from .mixins.signals_mixins import SignalsMixins



class Controller(SignalsMixins, ControllerData):
    def __init__(self, args, unknownargs):
        self.setup_controller_data()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()

        if args.no_plugins == "false":
            self.plugins.launch_plugins()

        for arg in unknownargs + [args.new_tab,]:
            if os.path.isfile(arg):
                message = f"FILE|{arg}"
                event_system.emit("post_file_to_ipc", message)


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.window.connect("focus-out-event", self.unset_keys_and_data)
        self.window.connect("key-press-event", self.on_global_key_press_controller)
        self.window.connect("key-release-event", self.on_global_key_release_controller)

    def _subscribe_to_events(self):
        event_system.subscribe("handle_file_from_ipc", self.handle_file_from_ipc)

    def load_glade_file(self):
        self.builder     = Gtk.Builder()
        self.builder.add_from_file(settings.get_glade_file())
        self.builder.expose_object("main_window", self.window)

        settings.set_builder(self.builder)
        self.core_widget = CoreWidget()

        settings.register_signals_to_builder([self, self.core_widget])

    def get_core_widget(self):
        return self.core_widget
