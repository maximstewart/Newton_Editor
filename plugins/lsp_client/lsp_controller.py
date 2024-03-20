# Python imports
import subprocess
import threading

# Lib imports
from . import pylspclient

# Application imports
from .capabilities import Capabilities



class ReadPipe(threading.Thread):
    def __init__(self, pipe):
        threading.Thread.__init__(self)

        self.daemon = True
        self.pipe   = pipe


    def run(self):
        line = self.pipe.readline().decode('utf-8')
        while line:
            line = self.pipe.readline().decode('utf-8')


class LSPController:
    def __init__(self, lsp_servers_config = {}):
        super().__init__()
        
        self.lsp_servers_config = lsp_servers_config
        self.lsp_clients = {}
    

    def _blame(self, response):
        for d in response['diagnostics']:
            if d['severity'] == 1:
                print(f"An error occurs in {response['uri']} at {d['range']}:")
                print(f"\t[{d['source']}] {d['message']}")

    def _shutting_down(self):
        keys = self.lsp_clients.keys()
        for key in keys:
            print(f"LSP Server: ( {key} ) Shutting Down...")
            self.lsp_clients[key].shutdown()
            self.lsp_clients[key].exit()

    def _generate_client(self, language = "", server_proc = None):
        if not language or not server_proc: return False

        json_rpc_endpoint  = pylspclient.JsonRpcEndpoint(server_proc.stdin, server_proc.stdout)

        callbacks = {
            "window/showMessage": print,
            "textDocument/symbolStatus": print,
            "textDocument/publishDiagnostics": self._blame,
        }

        lsp_endpoint       = pylspclient.LspEndpoint(json_rpc_endpoint, notify_callbacks = callbacks)
        lsp_client         = pylspclient.LspClient(lsp_endpoint)

        self.lsp_clients[language] = lsp_client
        return lsp_client

    def create_client(self, language = "", server_proc = None, initialization_options = None):
        if not language or not server_proc: return False

        root_path         = None
        # root_uri          = 'file:///home/abaddon/Coding/Projects/Active/Python_Projects/000_Usable/gtk/Newton_Editor/src/'
        # workspace_folders = [{'name': 'python-lsp', 'uri': root_uri}]
        root_uri          = ''
        workspace_folders = [{'name': '', 'uri': root_uri}]

        lsp_client        = self._generate_client(language, server_proc)
        lsp_client.initialize(
            processId = server_proc.pid, \
            rootPath  = root_path, \
            rootUri   = root_uri, \
            initializationOptions = initialization_options, \
            capabilities = Capabilities.data, \
            trace = "off", \
            # trace = "on", \
            workspaceFolders = workspace_folders
        )

        lsp_client.initialized()

        return True

    def create_lsp_server(self, server_command: [] = []):
        if not server_command: return None

        server_proc = subprocess.Popen(server_command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        read_pipe   = ReadPipe(server_proc.stderr)
        read_pipe.start()

        return server_proc


    def do_open(self, language_id, uri):
        if language_id in self.lsp_clients.keys():
            lsp_client = self.lsp_clients[language_id]
        else:
            lsp_client = self.load_lsp_server(language_id)

        if lsp_client:
            self.register_opened_file(language_id, uri, lsp_client)

    def do_save(self, language_id, uri):
        if language_id in self.lsp_clients.keys():
            self.lsp_clients[language_id].didSave(
                pylspclient.lsp_structs.TextDocumentIdentifier(uri)
            )

    def do_close(self, language_id, uri):
        if language_id in self.lsp_clients.keys():
            self.lsp_clients[language_id].didClose(
                pylspclient.lsp_structs.TextDocumentIdentifier(uri)
            )

    def do_goto(self, language_id, uri, line, offset):
        if language_id in self.lsp_clients.keys():
            return self.lsp_clients[language_id].definition(
                            pylspclient.lsp_structs.TextDocumentIdentifier(uri),
                            pylspclient.lsp_structs.Position(line, offset)
                    )
        
        return []

    def do_change(self, uri, language_id, line, start, end, text):
        if language_id in self.lsp_clients.keys():

            start_pos     = pylspclient.lsp_structs.Position(line, start.get_line_offset())
            end_pos       = pylspclient.lsp_structs.Position(line, end.get_line_offset())
            range_info    = pylspclient.lsp_structs.Range(start_pos, end_pos)
            text_length   = len(text)
            text_document = pylspclient.lsp_structs.TextDocumentItem(uri, language_id, 1, text)
            change_event  = pylspclient.lsp_structs.TextDocumentContentChangeEvent(range_info, text_length, text)

            return self.lsp_clients[language_id].didChange( text_document, change_event )
        
        return []

    def do_completion(self, language_id, uri, line, offset, _char, is_invoked = False):
        if language_id in self.lsp_clients.keys():
            trigger = pylspclient.lsp_structs.CompletionTriggerKind.TriggerCharacter

            if _char in [".", " "]:
                trigger = pylspclient.lsp_structs.CompletionTriggerKind.TriggerCharacter
            elif is_invoked:
                trigger = pylspclient.lsp_structs.CompletionTriggerKind.Invoked
            else:
                trigger = pylspclient.lsp_structs.CompletionTriggerKind.TriggerForIncompleteCompletions

            return self.lsp_clients[language_id].completion(
                            pylspclient.lsp_structs.TextDocumentIdentifier(uri),
                            pylspclient.lsp_structs.Position(line, offset),
                            None
                            # pylspclient.lsp_structs.CompletionContext(trigger, _char)
                    )

        return []


    def load_lsp_server(self, language_id):
        if not language_id in self.lsp_servers_config.keys():
            return

        command         = self.lsp_servers_config[language_id]["command"]
        config_options  = self.lsp_servers_config[language_id]["initialization_options"]

        if command:
            server_proc = self.create_lsp_server(command)
            if self.create_client(language_id, server_proc, config_options):
                return self.lsp_clients[language_id]

        return None

    def register_opened_file(self, language_id = "", uri = "", lsp_client = None):
            if not language_id or not uri: return

            text    = open(uri[7:], "r").read()
            version = 1

            lsp_client.didOpen(
                pylspclient.lsp_structs.TextDocumentItem(uri, language_id, version, text)
            )