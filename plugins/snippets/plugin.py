# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase
from . import cson



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name                 = "Snippets"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                #       where self.name should not be needed for message comms
        self.snippet_data         = None
        self._file_type           = None
        self.active_snippit_group = None
        self.snippit_groups       = []
        self.snippit_prefixes     = []
        self.snippit_group_keys   = []


    def generate_reference_ui_element(self):
        ...

    def run(self):
        with open('snippets.cson', 'rb') as f:
            self.snippet_data   = cson.load(f)
            self.snippit_groups = self.snippet_data.keys()

    def subscribe_to_events(self):
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)
        self._event_system.subscribe("show_snippets_ui", self._show_snippets_ui)
        self._event_system.subscribe("buffer_changed_first_load", self._buffer_changed_first_load)
        self._event_system.subscribe("buffer_changed", self._buffer_changed)


    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = source_view.get_buffer()
        self._file_type       = source_view.get_filetype()
        self._tag_table       = self._buffer.get_tag_table()

        self.load_target_snippt_group()

    def load_target_snippt_group(self):
        self.active_snippit_group = None
        for group in self.snippit_groups:
            if group in self._file_type:
                self.active_snippit_group = group
                break

        if self.active_snippit_group:
            self.snippit_prefixes.clear()
            keys = self.snippet_data[self.active_snippit_group].keys()
            
            self.snippit_group_keys.clear()
            for key in keys:
                self.snippit_group_keys.append(key)
                prefix = self.snippet_data[self.active_snippit_group][key]["prefix"]
                self.snippit_prefixes.append(prefix)

    def _buffer_changed_first_load(self, buffer):
        self._buffer = buffer
        self._handle_update(buffer)

    def _buffer_changed(self, buffer):
        self._event_system.emit("pause_event_processing")
        self._handle_update(buffer)
        self._event_system.emit("resume_event_processing")


    def _show_snippets_ui(self):
        print(f"Data:  {self.snippit_groups}")

    def _handle_update(self, buffer):
        if not self.active_snippit_group: return

        end_iter   = buffer.get_iter_at_mark( buffer.get_insert() )
        start_iter = end_iter.copy()
        start_iter.backward_word_start()

        matches = []
        text    = buffer.get_text(start_iter, end_iter, include_hidden_chars = False)
        for prefix in self.snippit_prefixes:
            if text in prefix:
                matches.append(prefix)

        snippits = []
        for _match in matches:
            for key in self.snippit_group_keys:
                prefix = self.snippet_data[self.active_snippit_group][key]["prefix"]
                if prefix == _match: 
                    body = self.snippet_data[self.active_snippit_group][key]["body"]
                    snippits.append(body)

        print(snippits)