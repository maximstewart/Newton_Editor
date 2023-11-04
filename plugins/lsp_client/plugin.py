# Python imports

# Lib imports

# Application imports


from plugins.plugin_base import PluginBase
from .lsp_controller import LSPController



class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name           = "LSP Client"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                            #       where self.name should not be needed for message comms
        self.lsp_controller = None


    def generate_reference_ui_element(self):
        ...

    def run(self):
        self.lsp_controller = LSPController()
        server_proc    = self.lsp_controller.create_lsp_server(["/usr/bin/clangd"])
        client_created = self.lsp_controller.create_client("c,cpp", server_proc)
        if not client_created:
            file_type = "dummy"
            text      = f"LSP could not be created for file type:  {file_type}  ..."
            self._event_system.emit("bubble_message", ("warning", self.name, text,))

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
        self.lsp_controller._shutting_down()

    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = source_view.get_buffer()
        self._file_type       = source_view.get_filetype()

    def _buffer_changed_first_load(self, buffer):
        self._buffer = buffer

    def _buffer_changed(self, buffer):
        ...

    def _do_goto(self):
        ...
    
    def _do_get_implementation(self):
        ...