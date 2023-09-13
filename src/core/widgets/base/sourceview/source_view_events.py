# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GtkSource

# Application imports



class SourceViewEventsMixin:
    def get_current_file(self):
        return self._current_file

    def set_buffer_language(self, language = "python3"):
        self._buffer.set_language( self._language_manager.get_language(language) )

    def set_buffer_style(self, style = "tango"):
        self._buffer.set_style_scheme( self._style_scheme_manager.get_scheme(style) )

    def toggle_highlight_line(self, widget = None, eve = None):
        self.set_highlight_current_line( not self.get_highlight_current_line() )

    def scale_up_text(self, scale_step = 10):
        current_scale = self._general_style_tag.get_property('scale')
        start_itr     = self._buffer.get_start_iter()
        end_itr       = self._buffer.get_end_iter()

        self._general_style_tag.set_property('scale',  current_scale + scale_step)
        self._buffer.apply_tag(self._general_style_tag, start_itr, end_itr)

    def scale_down_text(self, scale_step = 10):
        tag_table = self._buffer.get_tag_table()
        start_itr = self._buffer.get_start_iter()
        end_itr   = self._buffer.get_end_iter()
        tag       = tag_table.lookup('general_style')

        tag.set_property('scale', tag.get_property('scale') - scale_step)
        self._buffer.apply_tag(tag, start_itr, end_itr)

    def update_cursor_position(self):
        iter  = self._buffer.get_iter_at_mark( self._buffer.get_insert() )
        chars = iter.get_offset()
        row   = iter.get_line() + 1
        col   = self.get_visual_column(iter) + 1

        classes = self._buffer.get_context_classes_at_iter(iter)
        classes_str = ""

        i = 0
        for c in classes:
            if len(classes) != i + 1:
                classes_str += c + ", "
            else:
                classes_str += c

        cursor_data = f"char: {chars}, line: {row}, column: {col}, classes: {classes_str}"
        logger.debug(cursor_data)
        event_system.emit("set_line_char_label", (f"{row}:{col}",))

    def got_to_line(self, line: int = 0):
        index     = line - 1
        buffer    = self.get_buffer()
        line_itr  = buffer.get_iter_at_line(index)
        char_iter = buffer.get_iter_at_line_offset(index, line_itr.get_bytes_in_line())

        buffer.place_cursor(char_iter)
        if not buffer.get_mark("starting_cursor"):
             buffer.create_mark("starting_cursor", char_iter, True)
        self.scroll_to_mark( buffer.get_mark("starting_cursor"), 0.0, True, 0.0, 0.0 )

    # https://github.com/ptomato/inform7-ide/blob/main/src/actions.c
    def action_uncomment_selection(self):
        ...

    def action_comment_out_selection(self):
        ...

    def open_file(self, gfile, line: int = 0, *args):
        self._current_file = gfile

        self.load_file_info(gfile)
        self.load_file_async(gfile, line)
        self._create_file_watcher(gfile)

    def save_file(self):
        self.skip_file_load = True
        gfile = self.save_file_dialog() if not self._current_file else self._current_file

        if not gfile:
            self.skip_file_load = False
            return

        self.open_file( self._write_file(gfile) )
        self.skip_file_load = False

    def save_file_as(self):
        gfile = self.save_file_dialog()
        self._write_file(gfile, True)
        event_system.emit("create_view", (gfile,))

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
        if self.skip_file_load:
            self.update_labels(gfile)
            return

        file = GtkSource.File()
        file.set_location(gfile)
        self._file_loader = GtkSource.FileLoader.new(self._buffer, file)

        def finish_load_callback(obj, res, user_data=None):
            self._file_loader.load_finish(res)
            self._is_changed = False
            self._document_loaded()
            self.got_to_line(line)
            self.update_labels(gfile)

        self._file_loader.load_async(io_priority = 98,
                            cancellable = None,
                            progress_callback = None,
                            progress_callback_data = None,
                            callback = finish_load_callback,
                            user_data = (None))


    def update_labels(self, gfile = None):
        if not gfile: return

        tab_widget = self.get_parent().get_tab_widget()
        tab_widget.set_tab_label(self._current_filename)
        self.set_bottom_labels(gfile)

    def set_bottom_labels(self, gfile = None):
        if not gfile: return

        event_system.emit("set_bottom_labels", (gfile, None, self._current_filetype, None))
        self.update_cursor_position()


    def save_file_dialog(self) -> str:
        # TODO: Move Chooser logic to own widget
        dlg = Gtk.FileChooserDialog(title = "Please choose a file...", parent = None, action = 1)

        dlg.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        dlg.set_do_overwrite_confirmation(True)
        dlg.add_filter(self._file_filter_text)
        dlg.add_filter(self._file_filter_all)

        if self._current_filename == "":
            dlg.set_current_name("new.txt")
        else:
            dlg.set_current_folder(self._current_file.get_parent().get_path())
            dlg.set_current_name(self._current_filename)

        response = dlg.run()
        file     = dlg.get_filename() if response == Gtk.ResponseType.OK else ""
        dlg.destroy()

        return Gio.File.new_for_path(file) if not file == "" else None
