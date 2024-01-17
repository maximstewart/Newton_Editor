# Python imports
import os
import json
import threading

# Lib imports
from gi.repository import GLib

# Application imports


from plugins.plugin_base import PluginBase
from .lsp_controller import LSPController



class LSPPliginException(Exception):
    ...



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name                     = "LSP Client"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                #       where self.name should not be needed for message comms
        self.lsp_config_path: str     = os.path.dirname(os.path.realpath(__file__)) + "/../../lsp_servers_config.json"
        self.lsp_servers_config: dict = {}
        self.lsp_controller           = None
        self.timer                    = None


    def generate_reference_ui_element(self):
        ...

    def run(self):
        if os.path.exists(self.lsp_config_path):
            with open(self.lsp_config_path, "r") as f:
                self.lsp_servers_config = json.load(f)
        else:
            text      = f"LSP NOT Enabled.\nFile:\n\t{self.lsp_config_path}\ndoes no exsist..."
            self._event_system.emit("bubble_message", ("warning", self.name, text,))
            return

        if len(self.lsp_servers_config.keys()) > 0:
            self.lsp_controller = LSPController(self.lsp_servers_config)
            self.inner_subscribe_to_events()

    def subscribe_to_events(self):
        ...
    
    def inner_subscribe_to_events(self):
        self._event_system.subscribe("shutting_down", self._shutting_down)

        # self._event_system.subscribe("textDocument/didChange", self._buffer_changed)
        self._event_system.subscribe("textDocument/didOpen", self.lsp_controller.do_open)
        self._event_system.subscribe("textDocument/didSave", self.lsp_controller.do_save)
        self._event_system.subscribe("textDocument/didClose", self.lsp_controller.do_close)
        self._event_system.subscribe("textDocument/definition", self._do_goto)
        self._event_system.subscribe("textDocument/completion", self.completion)

    def _shutting_down(self):
        self.lsp_controller._shutting_down()

    def cancel_timer(self):
        if self.timer:
            self.timer.cancel()
            GLib.idle_remove_by_data(None)

    def delay_completion_glib(self, source_view, context, callback):
        GLib.idle_add(self._do_completion, source_view, context, callback)

    def delay_completion(self, source_view, context, callback):
        self.timer = threading.Timer(0.8, self.delay_completion_glib, (source_view, context, callback,))
        self.timer.daemon = True
        self.timer.start()
        
    def _buffer_changed(self, language_id, buffer):
        iter   = buffer.get_iter_at_mark( buffer.get_insert() )
        line   = iter.get_line()
        start  = iter.copy()
        end    = iter.copy()

        start.backward_line()
        start.forward_line()
        end.forward_to_line_end()

        text   = buffer.get_text(start, end, include_hidden_chars = False)        
        result = self.lsp_controller.do_change(language_id, line, start, end, text)

    def completion(self, source_view, context, callback):
        self.cancel_timer()
        self.delay_completion(source_view, context, callback)

    def _do_completion(self, source_view, context, callback):
        filepath  = source_view.get_current_file()

        if not filepath: return

        uri       = filepath.get_uri()
        buffer    = source_view.get_buffer()
        iter      = buffer.get_iter_at_mark( buffer.get_insert() )
        line      = iter.get_line() + 1

        _char     = iter.get_char()
        # if iter.backward_char():
        #     _char = iter.get_char()

        offset    = iter.get_line_index() + 1
        # offset    = iter.get_line_offset()
        result    = self.lsp_controller.do_completion(source_view.get_filetype(), uri, line, offset, _char)
        callback(context, result)

    def _do_goto(self, language_id, uri, line, offset):
        results = self.lsp_controller.do_goto(language_id, uri, line, offset)

        if len(results) == 1:
            result  = results[0]
            file    = result.uri[7:]
            line    = result.range.end.line
            message = f"FILE|{file}:{line}"
            self._event_system.emit("post_file_to_ipc", message)