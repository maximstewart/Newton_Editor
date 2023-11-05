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
        self.pipe = pipe

    def run(self):
        line = self.pipe.readline().decode('utf-8')
        while line:
            line = self.pipe.readline().decode('utf-8')



class LSPController:
    def __init__(self):
        super().__init__()
        
        self.lsp_clients = {}
    

    def create_client(self, language = "", server_proc = None, initialization_options = None):
        if not language or not server_proc: return False

        root_path         = None
        root_uri          = 'file:///home/abaddon/Coding/Projects/Active/C_n_CPP_Projects/gtk/Newton/src/'
        workspace_folders = [{'name': 'python-lsp', 'uri': root_uri}]

        lsp_client        = self._generate_client(language, server_proc)
        lsp_client.initialize(
            processId = server_proc.pid, \
            rootPath  = root_path, \
            rootUri   = root_uri, \
            initializationOptions = initialization_options, \
            capabilities = Capabilities.data, \
            trace = "off", \
            workspaceFolders = workspace_folders
        )

        lsp_client.initialized()

        return True
    
    def _generate_client(self, language = "", server_proc = None):
        if not language or not server_proc: return False

        json_rpc_endpoint  = pylspclient.JsonRpcEndpoint(server_proc.stdin, server_proc.stdout)
        lsp_endpoint       = pylspclient.LspEndpoint(json_rpc_endpoint)
        lsp_client         = pylspclient.LspClient(lsp_endpoint)

        self.lsp_clients[language] = lsp_client
        return lsp_client


    def create_lsp_server(self, server_command: [] = []):
        if not server_command: return None

        server_proc = subprocess.Popen(server_command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        read_pipe   = ReadPipe(server_proc.stderr)
        read_pipe.start()

        return server_proc

    def _shutting_down(self):
        keys = self.lsp_clients.keys()
        for key in keys:
            print(f"LSP Server: ( {key} ) Shutting Down...")
            self.lsp_clients[key].shutdown()
            self.lsp_clients[key].exit()

