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
        ctx = self.get_style_context()

        if self.px_value < 99:
            self.px_value += 1

        ctx.add_class(f"px{self.px_value}")

        # NOTE: Hope to bring this or similar back after we decouple scaling issues coupled with the miniview.
        # tag_table = self._buffer.get_tag_table()
        # start_itr = self._buffer.get_start_iter()
        # end_itr   = self._buffer.get_end_iter()
        # tag       = tag_table.lookup('general_style')
        #
        # tag.set_property('scale', tag.get_property('scale') + scale_step)
        # self._buffer.apply_tag(tag, start_itr, end_itr)

    def scale_down_text(self, scale_step = 10):
        ctx = self.get_style_context()

        ctx.remove_class(f"px{self.px_value}")
        if self.px_value > 1:
            self.px_value -= 1

        ctx.add_class(f"px{self.px_value}")

        # NOTE: Hope to bring this or similar back after we decouple scaling issues coupled with the miniview.
        # tag_table = self._buffer.get_tag_table()
        # start_itr = self._buffer.get_start_iter()
        # end_itr   = self._buffer.get_end_iter()
        # tag       = tag_table.lookup('general_style')
        #
        # tag.set_property('scale', tag.get_property('scale') - scale_step)
        # self._buffer.apply_tag(tag, start_itr, end_itr)

    def update_cursor_position(self):
        iter  = self._buffer.get_iter_at_mark( self._buffer.get_insert() )
        chars = iter.get_offset()
        row   = iter.get_line() + 1
        col   = self.get_visual_column(iter) + 1

        event_system.emit("set_line_char_label", (f"{row}:{col}",))

    def keyboard_tggl_comment(self):
        logger.info("SourceViewEventsMixin > keyboard_tggl_comment > stub...")

    def keyboard_insert_mark(self):
        iter  = self._buffer.get_iter_at_mark( self._buffer.get_insert() )
        mark  = Gtk.TextMark.new(name = f"multi_insert_{len(self._multi_insert_marks)}", left_gravity = False)

        self._buffer.add_mark(mark, iter)
        self._multi_insert_marks.append(mark)
        mark.set_visible(True)

    def keyboard_clear_marks(self):
        self._buffer.begin_user_action()

        for mark in self._multi_insert_marks:
            mark.set_visible(False)
            self._buffer.delete_mark(mark)

        self._multi_insert_marks.clear()
        self._buffer.end_user_action()

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

    def move_lines_up(self):
        self.emit("move-lines", *(False,))

    def move_lines_down(self):
        self.emit("move-lines", *(True,))

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
