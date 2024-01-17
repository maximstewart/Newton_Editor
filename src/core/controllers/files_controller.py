# Python imports
import os
import base64

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class FilesController:
    def __init__(self):

        self.opened_files = {}

        self._setup_signals()
        self._subscribe_to_events()


    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("set_pre_drop_dnd", self.set_pre_drop_dnd)
        event_system.subscribe("handle_file_event", self.handle_file_event)

    def set_pre_drop_dnd(self, gfiles):
        keys = self.opened_files.keys()

        for gfile in gfiles:
            fhash = str(gfile.hash())
            if fhash in keys: continue

            ftype, fhash = self.insert_to_sessions(fhash, gfile)

            content = None
            path    = gfile.get_path()
            with open(path) as f:
                content = base64.b64encode( f.read().encode(), altchars = None ).decode("utf-8")

            event_system.emit("load_file", (ftype, fhash, gfile.get_basename(), content))

    def handle_file_event(self, event):
        match event.topic:
            case "save":
                content = base64.b64decode( event.content.encode() ).decode("utf-8")
                self.save_session(event.target, content)
            case "close":
                self.close_session(event.target)
            case _:
                return

    def save_session(self, fhash, content):
        keys  = self.opened_files.keys()
        gfile = event_system.emit_and_await(
            "save_file_dialog", ("", None)
        ) if not fhash in keys else self.opened_files[fhash]["file"]

        if not gfile: return

        file_written = self.write_to_file(fhash, gfile, content)
        if not fhash in keys and file_written:
            self.insert_to_sessions(fhash, gfile)
            event_system.emit(
                "updated_tab",
                (
                    self.opened_files[fhash]["ftype"],
                    gfile.get_basename(),
                )
            )


    def close_session(self, target):
        del self.opened_files[target]

    def insert_to_sessions(self, fhash, gfile):
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

