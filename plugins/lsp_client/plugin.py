# Python imports
import os
import json

# Lib imports

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
        
        self.lsp_controller = LSPController(self.lsp_servers_config)
        self.inner_subscribe_to_events()

    def subscribe_to_events(self):
        ...
    
    def inner_subscribe_to_events(self):
        self._event_system.subscribe("shutting_down", self._shutting_down)
        self._event_system.subscribe("buffer_changed", self._buffer_changed)

        self._event_system.subscribe("textDocument/didOpen", self.lsp_controller.do_open)
        self._event_system.subscribe("textDocument/didSave", self.lsp_controller.do_save)
        self._event_system.subscribe("textDocument/didClose", self.lsp_controller.do_close)
        self._event_system.subscribe("textDocument/definition", self._do_goto)

    def _shutting_down(self):
        if self.lsp_controller:
            self.lsp_controller._shutting_down()


    def _buffer_changed(self, buffer):
        # self._do_completion()
        ...


    def _do_completion(self, is_invoked = False):
        fpath   = self._active_src_view.get_current_filepath()

        if not fpath: return

        uri     = fpath.get_uri()
        iter    = self._buffer.get_iter_at_mark( self._buffer.get_insert() )
        line    = iter.get_line()
        offset  = iter.get_line_offset()
        trigger = pylspclient.lsp_structs.CompletionTriggerKind.TriggerCharacter
        _char   = iter.get_char()
        trigger = None

        if _char in [".", " "]:
            trigger = pylspclient.lsp_structs.CompletionTriggerKind.TriggerCharacter
        elif is_invoked:
            trigger = pylspclient.lsp_structs.CompletionTriggerKind.Invoked
        else:
            trigger = pylspclient.lsp_structs.CompletionTriggerKind.TriggerForIncompleteCompletions

        result = self.lsp_controller.completion(
                        pylspclient.lsp_structs.TextDocumentIdentifier(uri),
                        pylspclient.lsp_structs.Position(line, offset),
                        pylspclient.lsp_structs.CompletionContext(trigger, _char)
                )
        
        if result.items:
            for item in result.items:
                print(item.label)
        else:
            print(result.label)

    def _do_goto(self, language_id, uri, line, offset):
        results = self.lsp_controller.do_goto(language_id, uri, line, offset)

        if len(results) == 1:
            result  = results[0]
            file    = result.uri[7:]
            line    = result.range.end.line
            message = f"FILE|{file}:{line}"
            self._event_system.emit("post_file_to_ipc", message)

