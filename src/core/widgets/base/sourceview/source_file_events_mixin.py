# Python imports
import random

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GtkSource

# Application imports



class FileEventsMixin:

    def get_current_file(self):
        return self._current_file

    def open_file(self, gfile, line: int = 0, *args):
        self._current_file = gfile

        self.load_file_info(gfile)
        self.load_file_async(gfile, line)
        self._create_file_watcher(gfile)

    def save_file(self):
        self._skip_file_load = True
        gfile = event_system.emit_and_await("save_file_dialog", (self._current_filename, self._current_file)) if not self._current_file else self._current_file

        if not gfile:
            self._skip_file_load = False
            return

        self.open_file( self._write_file(gfile) )
        self._skip_file_load = False

    def save_file_as(self):
        gfile = event_system.emit_and_await("save_file_dialog", (self._current_filename, self._current_file))
        self._write_file(gfile, True)
        if gfile: event_system.emit("create_view", (gfile,))

    def load_file_info(self, gfile):
        info         = gfile.query_info("standard::*", 0, cancellable=None)
        content_type = info.get_content_type()
        display_name = info.get_display_name()
        self._current_filename = display_name

        try:
            lm = self._language_manager.guess_language(None, content_type)
            self._current_filetype = lm.get_id()
            self.set_buffer_language(self._current_filetype)
        except Exception as e:
            ...

        logger.debug(f"Detected Content Type: {content_type}")
        if self._current_filetype == "buffer":
            self._current_filetype = info.get_content_type()

    def load_file_async(self, gfile, line: int = 0):
        if self._skip_file_load:
            self.update_labels(gfile)
            return

        file = GtkSource.File()
        file.set_location(gfile)
        self._file_loader = GtkSource.FileLoader.new(self._buffer, file)

        def finish_load_callback(obj, res, user_data=None):
            self._file_loader.load_finish(res)
            self._document_loaded()
            self.got_to_line(line)
            self.update_labels(gfile)

        self._file_loader.load_async(io_priority = 70,
                            cancellable = None,
                            progress_callback = None,
                            progress_callback_data = None,
                            callback = finish_load_callback,
                            user_data = (None))

    def _create_file_watcher(self, gfile = None):
        if not gfile: return

        self._cancel_current_file_watchers()
        self._file_change_watcher = gfile.monitor(Gio.FileMonitorFlags.NONE, Gio.Cancellable())
        self._file_change_watcher.connect("changed", self._file_monitor)

    def _file_monitor(self, file_monitor, file, other_file = None, eve_type = None, data = None):
        if not file.get_path() == self._current_file.get_path(): return

        if eve_type in [Gio.FileMonitorEvent.CREATED,
                        Gio.FileMonitorEvent.DELETED,
                        Gio.FileMonitorEvent.RENAMED,
                        Gio.FileMonitorEvent.MOVED_IN,
                        Gio.FileMonitorEvent.MOVED_OUT]:
            self._buffer.set_modified(True)

        if eve_type in [ Gio.FileMonitorEvent.CHANGES_DONE_HINT ]:
            if self._ignore_internal_change:
                self._ignore_internal_change = False
                return

            # TODO: Any better way to load the difference??
            if self._current_file.query_exists():
                self.load_file_async(self._current_file)

    def _cancel_current_file_watchers(self):
        if self._file_change_watcher:
            self._file_change_watcher.cancel()
            self._file_change_watcher = None

    def _write_file(self, gfile, save_as = False):
        if not gfile: return

        with open(gfile.get_path(), 'w') as f:
            if not save_as:
                self._ignore_internal_change = True

            start_itr = self._buffer.get_start_iter()
            end_itr   = self._buffer.get_end_iter()
            text      = self._buffer.get_text(start_itr, end_itr, True)

            f.write(text)
            f.close()

        self._buffer.set_modified(False)
        return gfile