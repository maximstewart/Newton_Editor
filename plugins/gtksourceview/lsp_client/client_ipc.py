# Python imports
import traceback
import os
import threading
import time
import json
import base64
from multiprocessing.connection import Client
from multiprocessing.connection import Listener

# Lib imports
import gi
from gi.repository import GLib

# Application imports
from .lsp_message_structs import LSPResponseRequest
from .lsp_message_structs import LSPResponseNotification, LSPIDResponseNotification
from .lsp_message_structs import get_message_obj



class ClientIPC:
    """ Create a Messenger so talk to LSP Manager. """
    def __init__(self, ipc_address: str = '127.0.0.1', conn_type: str = "socket"):
        self.is_ipc_alive     = False
        self._ipc_port        = 4848
        self._ipc_address     = ipc_address
        self._conn_type       = conn_type
        self._ipc_authkey         = b'' + bytes(f'lsp-client-endpoint-ipc', 'utf-8')
        self._manager_ipc_authkey = b'' + bytes(f'lsp-manager-endpoint-ipc', 'utf-8')
        self._ipc_timeout     = 15.0
        self._event_system    = None

        if conn_type == "socket":
            self._ipc_address         = f'/tmp/lsp-client-endpoint-ipc.sock'
            self._manager_ipc_address = f'/tmp/lsp-manager-endpoint-ipc.sock'
        elif conn_type == "full_network":
            self._ipc_address = '0.0.0.0'
        elif conn_type == "full_network_unsecured":
            self._ipc_authkey = None
            self._ipc_address = '0.0.0.0'
        elif conn_type == "local_network_unsecured":
            self._ipc_authkey = None


    def set_event_system(self, event_system):
        self._event_system = event_system

    def create_ipc_listener(self) -> None:
        if self._conn_type == "socket":
            if os.path.exists(self._ipc_address) and settings_manager.is_dirty_start():
                os.unlink(self._ipc_address)

            listener = Listener(address=self._ipc_address, family="AF_UNIX", authkey=self._ipc_authkey)
        elif "unsecured" not in self._conn_type:
            listener = Listener((self._ipc_address, self._ipc_port), authkey=self._ipc_authkey)
        else:
            listener = Listener((self._ipc_address, self._ipc_port))


        self.is_ipc_alive = True
        self._run_ipc_loop(listener)

    @daemon_threaded
    def _run_ipc_loop(self, listener) -> None:
        # NOTE: Not thread safe if using with Gtk. Need to import GLib and use idle_add
        while self.is_ipc_alive:
            try:
                conn       = listener.accept()
                start_time = time.perf_counter()
                self._handle_ipc_message(conn, start_time)
            except Exception as e:
                logger.debug( traceback.print_exc() )

        listener.close()

    def _handle_ipc_message(self, conn, start_time) -> None:
        while self.is_ipc_alive:
            msg = conn.recv()

            if "MANAGER|" in msg:
                data = msg.split("MANAGER|")[1].strip()

                if data:
                    data_str     = base64.b64decode(data.encode("utf-8")).decode("utf-8")
                    lsp_response = None
                    keys         = None

                    try:
                        lsp_response = json.loads(data_str)
                        keys         = lsp_response.keys()
                    except Exception as e:
                        raise e

                    if "result" in keys:
                        lsp_response = LSPResponseRequest(**get_message_obj(data_str))

                    if "method" in keys:
                        lsp_response = LSPResponseNotification( **get_message_obj(data_str) ) if not "id" in keys else LSPIDResponseNotification( **get_message_obj(data_str) )

                    if "notification" in keys:
                        ...

                    if "response" in keys:
                        ...

                    if "ignorable" in keys:
                        ...

                    if lsp_response:
                        GLib.idle_add(self._do_emit, lsp_response)

                conn.close()
                break

            if msg in ['close connection', 'close server']:
                conn.close()
                break

            # NOTE: Not perfect but insures we don't lock up the connection for too long.
            end_time = time.perf_counter()
            if (end_time - start_time) > self._ipc_timeout:
                conn.close()
                break

    def _do_emit(self, lsp_response):
        self._event_system.emit("handle-lsp-message", (lsp_response,))

    def send_manager_ipc_message(self, message: str) -> None:
        try:
            if self._conn_type == "socket":
                if not os.path.exists(self._manager_ipc_address):
                    logger.error(f"Socket:  {self._manager_ipc_address}  doesn't exist. NOT sending message...")
                    return

                conn = Client(address=self._manager_ipc_address, family="AF_UNIX", authkey=self._manager_ipc_authkey)
            elif "unsecured" not in self._conn_type:
                conn = Client((self._ipc_address, self._ipc_port), authkey=self._ipc_authkey)
            else:
                conn = Client((self._ipc_address, self._ipc_port))

            conn.send( f"CLIENT|{ base64.b64encode(message.encode('utf-8')).decode('utf-8')  }" )
            conn.close()
        except ConnectionRefusedError as e:
            logger.error("Connection refused...")
        except Exception as e:
            logger.error( repr(e) )


    def send_ipc_message(self, message: str = "Empty Data...") -> None:
        try:
            if self._conn_type == "socket":
                conn = Client(address=self._ipc_address, family="AF_UNIX", authkey=self._ipc_authkey)
            elif "unsecured" not in self._conn_type:
                conn = Client((self._ipc_address, self._ipc_port), authkey=self._ipc_authkey)
            else:
                conn = Client((self._ipc_address, self._ipc_port))

            conn.send(message)
            conn.close()
        except ConnectionRefusedError as e:
            logger.error("Connection refused...")
        except Exception as e:
            logger.error( repr(e) )

    def send_test_ipc_message(self, message: str = "Empty Data...") -> None:
        try:
            if self._conn_type == "socket":
                conn = Client(address=self._ipc_address, family="AF_UNIX", authkey=self._ipc_authkey)
            elif "unsecured" not in self._conn_type:
                conn = Client((self._ipc_address, self._ipc_port), authkey=self._ipc_authkey)
            else:
                conn = Client((self._ipc_address, self._ipc_port))

            conn.send(message)
            conn.close()
        except ConnectionRefusedError as e:
            if self._conn_type == "socket":
                logger.error("LSP Socket no longer valid.... Removing.")
                os.unlink(self._ipc_address)
        except Exception as e:
            logger.error( repr(e) )