# Python imports
import signal
import subprocess
import json

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase
from .client_ipc import ClientIPC



class Plugin(PluginBase):
    def __init__(self):

        super().__init__()
        self.name            = "LSP Client"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                             #       where self.name should not be needed for message comms
        self.config_file     = "config.json"
        self.config: dict    = {}
        self.lsp_client_proc = None
        self.lsp_window      = None


    def generate_reference_ui_element(self):
        ...

    def run(self):
        try:
            with open(self.config_file) as f:
                self.config = json.load(f)
        except Exception as e:
            raise Exception(f"Couldn't load config.json...\n{repr(e)}")

        self.lsp_window = Gtk.Window()
        box1            = Gtk.Box()
        box2            = Gtk.Box()
        start_btn       = Gtk.Button(label = "Start LSP Client")
        stop_btn        = Gtk.Button(label = "Stop LSP Client")
        pid_label       = Gtk.Label(label  = "LSP PID: ")

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

    def _tggl_lsp_window(self, widget = None):
        if not self.lsp_window.is_visible():
            self.lsp_window.show()
        else:
            self.lsp_window.hide()


    def subscribe_to_events(self):
        self._event_system.subscribe("tggl_lsp_window", self._tggl_lsp_window)

    def inner_subscribe_to_events(self):
        self._event_system.subscribe("shutting_down", self._shutting_down)

        self._event_system.subscribe("textDocument/didOpen",    self._lsp_did_open)
        self._event_system.subscribe("textDocument/didSave",    self._lsp_did_save)
        self._event_system.subscribe("textDocument/didClose",   self._lsp_did_close)
        self._event_system.subscribe("textDocument/didChange",  self._lsp_did_change)
        self._event_system.subscribe("textDocument/definition", self._lsp_goto)
        self._event_system.subscribe("textDocument/completion", self._lsp_completion)

    def start_lsp_manager(self, button):
        if self.lsp_client_proc: return
        self.lsp_client_proc = subprocess.Popen(self.config["lsp_manager_start_command"])
        self._load_client_ipc_server()

    def _load_client_ipc_server(self):
        self.client_ipc = ClientIPC()
        self.client_ipc.set_event_system(self._event_system)
        self._ipc_realization_check(self.client_ipc)

        if not self.client_ipc.is_ipc_alive:
            raise AppLaunchException(f"LSP IPC Server Already Exists...")

    def _ipc_realization_check(self, ipc_server):
        try:
            ipc_server.create_ipc_listener()
        except Exception:
            ipc_server.send_test_ipc_message()

        try:
            ipc_server.create_ipc_listener()
        except Exception as e:
            ...

    def stop_lsp_manager(self, button = None):
        if not self.lsp_client_proc: return
        if not self.lsp_client_proc.poll() is None:
            self.lsp_client_proc = None
            return

        self.lsp_client_proc.terminate()
        self.client_ipc.is_ipc_alive = False
        self.lsp_client_proc = None

    def _lsp_did_open(self, language_id: str, uri: str, text: str):
        if not self.lsp_client_proc: return

        data = {
            "method": "textDocument/didOpen",
            "language_id": language_id,
            "uri": uri,
            "version": -1,
            "text": text,
            "line": -1,
            "column": -1,
            "char": ""
        }

        self.send_message(data)

    def _lsp_did_save(self, uri: str, text: str):
        if not self.lsp_client_proc: return

        data = {
            "method": "textDocument/didSave",
            "language_id": "",
            "uri": uri,
            "version": -1,
            "text": text,
            "line": -1,
            "column": -1,
            "char": ""
        }

        self.send_message(data)

    def _lsp_did_close(self, uri: str):
        if not self.lsp_client_proc: return

        data = {
            "method": "textDocument/didClose",
            "language_id": "",
            "uri": uri,
            "version": -1,
            "text": "",
            "line": -1,
            "column": -1,
            "char": ""
        }

        self.send_message(data)

    def _lsp_did_change(self, language_id: str, uri: str, buffer):
        if not self.lsp_client_proc: return

        iter       = buffer.get_iter_at_mark( buffer.get_insert() )
        line       = iter.get_line()
        column     = iter.get_line_offset()

        start, end = buffer.get_bounds()

        text   = buffer.get_text(start, end, include_hidden_chars = True)
        data   = {
            "method": "textDocument/didChange",
            "language_id": language_id,
            "uri": uri,
            "version": buffer.version_id,
            "text": text,
            "line": line,
            "column": column,
            "char": ""
        }

        self.send_message(data)


#    def _lsp_did_change(self, language_id: str, uri: str, buffer):
#        if not self.lsp_client_proc: return

#        iter   = buffer.get_iter_at_mark( buffer.get_insert() )
#        line   = iter.get_line()
#        column = iter.get_line_offset()
#        start  = iter.copy()
#        end    = iter.copy()

#        start.backward_line()
#        start.forward_line()
#        end.forward_line()

#        text   = buffer.get_text(start, end, include_hidden_chars = True)
#        data   = {
#            "method": "textDocument/didChange",
#            "language_id": language_id,
#            "uri": uri,
#            "version": buffer.version_id,
#            "text": text,
#            "line": line,
#            "column": column,
#            "char": ""
#        }

#        self.send_message(data)


    def _lsp_goto(self, language_id: str, uri: str, line: int, column: int):
        if not self.lsp_client_proc: return

        data = {
            "method": "textDocument/definition",
            "language_id": language_id,
            "uri": uri,
            "version": -1,
            "text": "",
            "line": line,
            "column": column,
            "char": ""
        }

        self.send_message(data)

    def _lsp_completion(self, source_view):
        if not self.lsp_client_proc: return

        filepath  = source_view.get_current_file()
        if not filepath: return

        uri       = filepath.get_uri()
        buffer    = source_view.get_buffer()
        iter      = buffer.get_iter_at_mark( buffer.get_insert() )
        line      = iter.get_line()
        column    = iter.get_line_offset()
        char      = iter.get_char()

        data   = {
            "method": "textDocument/completion",
            "language_id": source_view.get_filetype(),
            "uri": uri,
            "version": source_view.get_version_id(),
            "text": "",
            "line": line,
            "column": column,
            "char": char
        }

        self.send_message(data)

    def send_message(self, data: dict):
        self.client_ipc.send_manager_ipc_message( json.dumps(data) )
