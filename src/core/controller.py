# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports
from .mixins.dummy_mixin import DummyMixin
from .controller_data import ControllerData
from .core_widget import CoreWidget




class Controller(DummyMixin, ControllerData):
    def __init__(self, args, unknownargs):
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()

        self.setup_controller_data()
        self.print_hello_world() # A mixin method from the DummyMixin file

        logger.info(f"Made it past {self.__class__} loading...")


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...


    def _subscribe_to_events(self):
        event_system.subscribe("handle_file_from_ipc", self.handle_file_from_ipc)

    def handle_file_from_ipc(self, path: str) -> None:
        print(f"Path From IPC: {path}")

    def load_glade_file(self):
        self.builder     = Gtk.Builder()
        self.builder.add_from_file(settings.get_glade_file())
        self.builder.expose_object("main_window", self.window)

        settings.set_builder(self.builder)
        self.core_widget = CoreWidget()

        settings.register_signals_to_builder([self, self.core_widget])

    def get_core_widget(self):
        return self.core_widget


    def on_global_key_release_controller(self, widget: type, event: type) -> None:
        """Handler for keyboard events"""
        keyname = Gdk.keyval_name(event.keyval).lower()
        if keyname.replace("_l", "").replace("_r", "") in ["control", "alt", "shift"]:
            if "control" in keyname:
                self.ctrl_down    = False
            if "shift" in keyname:
                self.shift_down   = False
            if "alt" in keyname:
                self.alt_down     = False


        mapping = keybindings.lookup(event)
        if mapping:
            getattr(self, mapping)()
            return True
        else:
            print(f"on_global_key_release_controller > key > {keyname}")
            print(f"Add logic or remove this from: {self.__class__}")
