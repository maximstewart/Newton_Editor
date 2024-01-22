# Python imports
import os
import base64

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
        event_system.subscribe(f"handle_file_event_{self.INDEX}", self.handle_file_event)

    def set_pre_drop_dnd(self, gfiles):
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
                    content
                )
            )

    def handle_file_event(self, event):
        match event.topic:
            case "save":
                content  = base64.b64decode( event.content.encode() ).decode("utf-8")
                basename = self.save_session(event.target, content)

                if basename:
                    event_system.emit(f"updated_tab_{event.originator}", (event.target, basename,))
            case "close":
                event_system.emit(f"close_tab_{event.originator}", (event.target))
            case "load_buffer":
                self.load_buffer(event.target)
                event_system.emit(f"add_tab_{event.originator}", (event.target, "buffer",))
            case "load_file":
                content  = base64.b64decode( event.content.encode() ).decode("utf-8")
                event_system.emit(f"add_tab_with_name_{event.originator}", (event.target, content,))
            case _:
                return

    def load_buffer(self, fhash):
        self.opened_files[fhash] = {"file": None, "ftype": "buffer"}

    def save_session(self, fhash, content):
        ftype = self.opened_files[fhash]["ftype"]
        gfile = event_system.emit_and_await(
            "save_file_dialog", ("", None)
        ) if fhash == "buffer" else self.opened_files[fhash]["file"]

        file_written = self.write_to_file(fhash, gfile, content)
        if fhash == "buffer" and file_written:
            self.update_session(fhash, gfile)
            return gfile.get_basename()

    def update_session(self, fhash, gfile):
        info  = gfile.query_info("standard::*", 0, cancellable = None)
        ftype = info.get_content_type().replace("x-", "").split("/")[1]

        self.opened_files[fhash] = {"file": gfile, "ftype": ftype}

        return ftype, fhash

    def write_to_file(self, fhash, gfile, content):
        with open(gfile.get_path(), 'w') as outfile:
            try:
                outfile.write(content)
            except Exception as e:
                message = f"[Error]: Could NOT save {gfile.get_basename()} ..."
                event_system.emit("ui_message", (message, "error",))
                return False

        return True