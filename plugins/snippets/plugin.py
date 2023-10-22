# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Snippets"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                              #       where self.name should not be needed for message comms


    def generate_reference_ui_element(self):
        button = Gtk.Button(label=self.name)
        button.connect("button-release-event", self.send_message)
        return button

    def run(self):
        ...

    def send_message(self, widget=None, eve=None):
        message = "Hello, World!"
        event_system.emit("display_message", ("warning", message, None))