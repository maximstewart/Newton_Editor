# Python imports
import os
import base64

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports



class FilesController:
    def __init__(self, index):

        self.INDEX        = index
        self.opened_files = {}

        self._setup_signals()
        self._subscribe_to_events()


    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe(f"set_pre_drop_dnd_{self.INDEX}", self.set_pre_drop_dnd)
        event_system.subscribe("handle_file_from_ipc", self.handle_file_from_ipc)
        event_system.subscribe(f"handle_file_event_{self.INDEX}", self.handle_file_event)

    def set_pre_drop_dnd(self, gfiles, line: int = 0):
        for gfile in gfiles:
            fname   = gfile.get_basename()
            fpath   = gfile.get_path()
            content = None

            with open(fpath) as f:
                content = base64.b64encode( f.read().encode(), altchars = None ).decode("utf-8")

            info  = gfile.query_info("standard::*", 0, cancellable = None)
            ftype = info.get_content_type().replace("x-", "").split("/")[1]
            event_system.emit(
                f"load_file_{self.INDEX}",
                (
                    ftype,
                    fname,
                    fpath,
                    content,
                    line
                )
            )

    def handle_file_from_ipc(self, path: str) -> None:
        logger.debug(f"Path From IPC: {path}")
        line  = "0"
        fpath = ""

        try:
            fpath, line = path.split(":")
        except:
            fpath = path

        print(fpath)
        gfile = Gio.File.new_for_path(fpath)

        try:
            logger.info(f"Line:  {line}")
            self.set_pre_drop_dnd([gfile], int(line))
        except Exception as e:
            logger.info(repr(e))

    def handle_file_event(self, event):
        match event.topic:
            case "save":
                content             = base64.b64decode( event.content.encode() ).decode("utf-8")
                ftype, fname, fpath = self.save_session(event.ftype, event.fpath, content)

                if ftype and fname and fpath:
                    event_system.emit(f"update_tab_{event.originator}", (event.fhash, fname,))
                    event_system.emit(f"updated_session_{event.originator}", (event.fhash, ftype, fname, fpath))
            case "close":
                event_system.emit(f"close_tab_{event.originator}", (event.fhash))
            case "load_buffer":
                self.load_buffer(event.fhash)
                # event_system.emit(f"add_tab_{event.originator}", (event.fhash, "buffer",))
            case "load_file":
                content  = base64.b64decode( event.content.encode() ).decode("utf-8")
                # event_system.emit(f"add_tab_with_name_{event.originator}", (event.fhash, content,))
            case _:
                return

    def load_buffer(self, fhash):
        self.opened_files[fhash] = {"file": None, "ftype": "buffer"}


    def save_session(self, ftype, fpath, content):
        gfile = event_system.emit_and_await(
            "save_file_dialog", ("", None)
        ) if ftype == "buffer" else Gio.File.new_for_path(fpath)

        file_written = self.write_to_file(gfile, content)
        if ftype == "buffer" and file_written:
            info  = gfile.query_info("standard::*", 0, cancellable = None)
            ftype = info.get_content_type().replace("x-", "").split("/")[1]

            return ftype, gfile.get_basename(), gfile.get_path()

    def update_session(self, fhash, gfile):
        info  = gfile.query_info("standard::*", 0, cancellable = None)
        ftype = info.get_content_type().replace("x-", "").split("/")[1]

        self.opened_files[fhash] = {"file": gfile, "ftype": ftype}

        return ftype, fhash

    def write_to_file(self, gfile, content):
        with open(gfile.get_path(), 'w') as outfile:
            try:
                outfile.write(content)
            except Exception as e:
                message = f"[Error]: Could NOT save {gfile.get_basename()} ..."
                event_system.emit("ui_message", (message, "error",))
                return False

        return True