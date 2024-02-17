# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports
from libs.mixins.keyboard_signals_mixin import KeyboardSignalsMixin

from ..containers.base_container import BaseContainer

from .base_controller_data import BaseControllerData
from .bridge_controller import BridgeController



class BaseController(KeyboardSignalsMixin, BaseControllerData):
    def __init__(self, args, unknownargs):
        self.collect_files_dirs(args, unknownargs)

        self.setup_controller_data()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_controllers()

        if args.no_plugins == "false":
            self.plugins.launch_plugins()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.window.connect("focus-out-event", self.unset_keys_and_data)
        # self.window.connect("key-press-event", self.on_global_key_press_controller)
        # self.window.connect("key-release-event", self.on_global_key_release_controller)

    def _subscribe_to_events(self):
        event_system.subscribe("shutting_down", lambda: print("Shutting down..."))
        event_system.subscribe("set_active_src_view", self.set_active_src_view)
        event_system.subscribe("get_active_src_view", self.get_active_src_view)

    def _load_controllers(self):
        BridgeController()

    def load_glade_file(self):
        self.builder     = Gtk.Builder()
        self.builder.add_from_file(settings_manager.get_glade_file())
        self.builder.expose_object("main_window", self.window)

        settings_manager.set_builder(self.builder)
        self.core_widget = BaseContainer()

        settings_manager.register_signals_to_builder([self, self.core_widget])

    def get_core_widget(self):
        return self.core_widget