# Python imports
import os
import json

# Lib imports

# Application imports


from plugins.plugin_base import PluginBase
from .lsp_controller import LSPController



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name                     = "LSP Client"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                #       where self.name should not be needed for message comms
        self.lsp_config_path: str     = os.path.dirname(os.path.realpath(__file__)) + "/../../lsp_servers_config.json"
        self.lsp_servers_config: dict = {}
        self.lsp_controller           = None
        self.lsp_client               = None
        self.lsp_disabled             = False

    def generate_reference_ui_element(self):
        ...

    def run(self):
        if os.path.exists(self.lsp_config_path):
            with open(self.lsp_config_path, "r") as f:
                self.lsp_servers_config = json.load(f)
        else:
            self.lsp_disabled = True
            text      = f"LSP NOT Enabled.\nFile:\n\t{self.lsp_config_path}\ndoes no exsist..."
            self._event_system.emit("bubble_message", ("warning", self.name, text,))
        
        if not self.lsp_disabled:
            self.lsp_controller = LSPController()

        # language_id = pylspclient.lsp_structs.LANGUAGE_IDENTIFIER.C
        # version     = 1
        # self.lsp_client.didOpen(pylspclient.lsp_structs.TextDocumentItem(uri, language_id, version, text))
        # try:
            # symbols = self.lsp_client.documentSymbol(pylspclient.lsp_structs.TextDocumentIdentifier(uri))
            # for symbol in symbols:
                # print(symbol.name)
        # except pylspclient.lsp_structs.ResponseError:
            # documentSymbol is supported from version 8.
            # print("Failed to document symbols")
            # ...

        # self.lsp_client.definition(pylspclient.lsp_structs.TextDocumentIdentifier(uri), pylspclient.lsp_structs.Position(14, 4))
        # self.lsp_client.signatureHelp(pylspclient.lsp_structs.TextDocumentIdentifier(uri), pylspclient.lsp_structs.Position(14, 4))
        # self.lsp_client.definition(pylspclient.lsp_structs.TextDocumentIdentifier(uri), pylspclient.lsp_structs.Position(14, 4))
        # self.lsp_client.completion(pylspclient.lsp_structs.TextDocumentIdentifier(uri), pylspclient.lsp_structs.Position(14, 4), pylspclient.lsp_structs.CompletionContext(pylspclient.lsp_structs.CompletionTriggerKind.Invoked))



    def subscribe_to_events(self):
        self._event_system.subscribe("shutting_down", self._shutting_down)
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)
        self._event_system.subscribe("buffer_changed_first_load", self._buffer_changed_first_load)
        self._event_system.subscribe("buffer_changed", self._buffer_changed)

        self._event_system.subscribe("do_goto", self._do_goto)
        self._event_system.subscribe("do_get_implementation", self._do_get_implementation)

    def _shutting_down(self):
        if self.lsp_controller:
            self.lsp_controller._shutting_down()

    def _set_active_src_view(self, source_view):
        if self.lsp_disabled: return

        self._active_src_view = source_view
        self._buffer          = source_view.get_buffer()
        self._file_type       = source_view.get_filetype()
        
        if self._file_type in self.lsp_servers_config.keys():
            self.set_lsp_server()
        else:
            text      = f"LSP could not be created for file type:  {self._file_type}  ..."
            self._event_system.emit("bubble_message", ("warning", self.name, text,))
    
    def set_lsp_server(self):
        if self._file_type in self.lsp_controller.lsp_clients.keys():
            self.lsp_client = self.lsp_controller.lsp_clients[self._file_type]
        else:
            self.lsp_client = self.load_lsp_server()

    def load_lsp_server(self):
        command = self.lsp_servers_config[self._file_type]["command"]
        if command:
            server_proc    = self.lsp_controller.create_lsp_server(command)
            client_created = self.lsp_controller.create_client(self._file_type, server_proc)

            if client_created:
                return self.lsp_controller.lsp_clients[self._file_type]
            else:
                text      = f"LSP could not be created for file type:  {self._file_type}  ..."
                self._event_system.emit("bubble_message", ("warning", self.name, text,))

        return None


    def _buffer_changed_first_load(self, buffer):
        if self.lsp_disabled: return

        self._buffer = buffer

    def _buffer_changed(self, buffer):
        if self.lsp_disabled: return

    def _do_goto(self):
        if self.lsp_disabled: return

        iter   = self._buffer.get_iter_at_mark( self._buffer.get_insert() )
        line   = iter.get_line() + 1
        offset = iter.get_line_offset() + 1
        uri    = self._active_src_view.get_current_filepath().get_uri()
        result = self.lsp_client.declaration(pylspclient.lsp_structs.TextDocumentIdentifier(uri), pylspclient.lsp_structs.Position(line, offset))

        print(result)


    def _do_get_implementation(self):
        if self.lsp_disabled: return