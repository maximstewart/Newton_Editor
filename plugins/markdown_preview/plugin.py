# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import WebKit2

# Application imports
from plugins.plugin_base import PluginBase



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Markdown Preview"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                      #       where self.name should not be needed for message comms
        self.path               = os.path.dirname(os.path.realpath(__file__))
        self._GLADE_FILE        = f"{self.path}/markdown_preview.glade"
        
        WebKit2.WebView()       # Need one initialized for webview to work from glade file


    def run(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(self._GLADE_FILE)
        self._connect_builder_signals(self, self._builder)

        separator_right         = self._ui_objects[0]
        self._markdown_dialog   = self._builder.get_object("markdown_preview_dialog")
        self._web_view_settings = self._builder.get_object("web_view_settings")


    def generate_reference_ui_element(self):
        ...

    def subscribe_to_events(self):
        self._event_system.subscribe("tggle_markdown_preview", self._tggle_markdown_preview)

    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = self._active_src_view.get_buffer()

    def _pause_preview_updates(self):
        ...

    def _resume_preview_updates(self):
        ...

    def _handle_ettings(self):
        ...

    def _tggle_markdown_preview(self, widget = None, eve = None):
        is_visible = self._markdown_dialog.is_visible()
        buffer     = self._active_src_view.get_buffer()
        data       = None

        if not is_visible:
            self._markdown_dialog.popup();
        elif not data and is_visible:
            self._markdown_dialog.popdown()