# Python imports
import subprocess
import json

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase
from .websockets.sync.client import connect 



class Plugin(PluginBase):
    def __init__(self):

        super().__init__()
        self.name             = "LSP Manager"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                               #       where self.name should not be needed for message comms
        self.ws_config_file   = "config.json"
        self.ws_config: dict  = {}
        self.lsp_manager_proc = None
        self.lsp_window       = None


    def generate_reference_ui_element(self):
        ...

    def run(self):
        try:
            with open(self.ws_config_file) as f:
                self.ws_config = json.load(f)["websocket"]
        except Exception as e:
            raise Exception(f"Couldn't load config.json...\n{repr(e)}")

        self.lsp_window = Gtk.Window()
        box1            = Gtk.Box()
        box2            = Gtk.Box()
        start_btn       = Gtk.Button(label = "Start LSP Manager")
        stop_btn        = Gtk.Button(label = "Stop LSP Manager")
        pid_label       = Gtk.Label(label = "LSP PID: ")

        box1.set_orientation( Gtk.Orientation.VERTICAL )

        self.lsp_window.set_deletable(False)
        self.lsp_window.set_skip_pager_hint(True)
        self.lsp_window.set_skip_taskbar_hint(True)
        self.lsp_window.set_title("LSP Manager")
        self.lsp_window.set_size_request(480, 320)

        start_btn.connect("clicked", self.start_lsp_manager)
        stop_btn.connect("clicked", self.stop_lsp_manager)

        box1.add(pid_label)
        box2.add(start_btn)
        box2.add(stop_btn)
        box1.add(box2)
        self.lsp_window.add(box1)

        box1.show_all()

        self.inner_subscribe_to_events()

    def _shutting_down(self):
        self.stop_lsp_manager()

    def _tear_down(self, widget, eve):
        return True

    def _tggl_lsp_window(self):
        if not self.lsp_window.is_visible():
            self.lsp_window.show()
        else:
            self.lsp_window.hide()

    def subscribe_to_events(self):
        self._event_system.subscribe("tggl_lsp_window", self._tggl_lsp_window)

    def inner_subscribe_to_events(self):
        self._event_system.subscribe("shutting_down", self._shutting_down)

        self._event_system.subscribe("textDocument/didOpen",    self._lsp_did_open)
        # self._event_system.subscribe("textDocument/didSave",    self._lsp_did_save)
        # self._event_system.subscribe("textDocument/didClose",   self._lsp_did_close)
        self._event_system.subscribe("textDocument/didChange",  self._lsp_did_change)
        self._event_system.subscribe("textDocument/definition", self._lsp_goto)
        self._event_system.subscribe("textDocument/completion", self._lsp_completion)

    def start_lsp_manager(self, button):
        if self.lsp_manager_proc: return
        self.lsp_manager_proc = subprocess.Popen(["lsp-manager"])

    def stop_lsp_manager(self, button = None):
        if not self.lsp_manager_proc: return
        if not self.lsp_manager_proc.poll() is None:
            self.lsp_manager_proc = None
            return

        self.lsp_manager_proc.terminate()
        self.lsp_manager_proc = None

    def _lsp_did_open(self, language_id, uri, text):
        if not self.lsp_manager_proc: return

        data = {
            "method": "textDocument/didOpen",
            "language_id": language_id,
            "uri": uri,
            "text": text,
            "line": -1,
            "column": -1,
            "char": ""
        }

        self.send_message(data)

    def _lsp_did_save(self):
        if not self.lsp_manager_proc: return

    def _lsp_did_close(self):
        if not self.lsp_manager_proc: return

    def _lsp_did_change(self, language_id, buffer):
        if not self.lsp_manager_proc: return

        iter   = buffer.get_iter_at_mark( buffer.get_insert() )
        line   = iter.get_line()
        start  = iter.copy()
        end    = iter.copy()

        start.backward_line()
        start.forward_line()
        end.forward_to_line_end()

        text   = buffer.get_text(start, end, include_hidden_chars = False)
        data   = {
            "method": "textDocument/didChange",
            "language_id": language_id,
            "uri": uri,
            "text": text
            "line": -1,
            "column": -1,
            "char": ""
        }

        self.send_message(data)

    def _lsp_goto(self, language_id, uri, line, column):
        if not self.lsp_manager_proc: return

        data = {
            "method": "textDocument/definition",
            "language_id": language_id,
            "uri": uri,
            "text": "",
            "line": line,
            "column": column,
            "char": ""
        }

        self.send_message(data)

    def _lsp_completion(self, source_view):
        if not self.lsp_manager_proc: return

        filepath  = source_view.get_current_file()
        if not filepath: return

        uri       = filepath.get_uri()
        buffer    = source_view.get_buffer()
        iter      = buffer.get_iter_at_mark( buffer.get_insert() )
        line      = iter.get_line()

        char      = iter.get_char()
        if iter.backward_char():
            char = iter.get_char()

        column = iter.get_line_offset()
        data   = {
            "method": "textDocument/completion",
            "language_id": source_view.get_filetype(),
            "uri": uri,
            "text": "",
            "line": line,
            "column": column,
            "char": char
        }

        self.send_message(data)


    def send_message(self, data: dict):
        with connect(f"ws://{ self.ws_config['host'] }:{ self.ws_config['port'] }") as websocket:
            websocket.send(
                json.dumps(data)
            )
            message = websocket.recv()
            print(f"Received: {message}")