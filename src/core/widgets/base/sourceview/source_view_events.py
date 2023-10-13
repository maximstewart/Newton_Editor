# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .source_file_events_mixin import FileEventsMixin
from .source_marks_events_mixin import MarkEventsMixin



class SourceViewEventsMixin(MarkEventsMixin, FileEventsMixin):

    def set_buffer_language(self, language = "python3"):
        self._buffer.set_language( self._language_manager.get_language(language) )

    def set_buffer_style(self, style = settings.theming.syntax_theme):
        self._buffer.set_style_scheme( self._style_scheme_manager.get_scheme(style) )

    def toggle_highlight_line(self, widget = None, eve = None):
        self.set_highlight_current_line( not self.get_highlight_current_line() )

    def scale_up_text(self, scale_step = 10):
        ctx = self.get_style_context()

        if self._px_value < 99:
            self._px_value += 1
            ctx.add_class(f"px{self._px_value}")

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

        if self._px_value > 1:
            ctx.remove_class(f"px{self._px_value}")
            self._px_value -= 1
            ctx.add_class(f"px{self._px_value}")

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

    def keyboard_tggl_comment(self):
        logger.info("SourceViewEventsMixin > keyboard_tggl_comment > stub...")

    def keyboard_undo(self):
        self._buffer.undo()

    def keyboard_redo(self):
        self._buffer.redo()

    def move_lines_up(self):
        self.emit("move-lines", *(False,))

    def move_lines_down(self):
        self.emit("move-lines", *(True,))

    def update_labels(self, gfile = None):
        if not gfile: return

        tab_widget = self.get_parent().get_tab_widget()
        tab_widget.set_tab_label(self._current_filename)
        self.set_bottom_labels(gfile)

    def set_bottom_labels(self, gfile = None):
        if not gfile: return

        event_system.emit("set_bottom_labels", (gfile, None, self._current_filetype, None))
        self.update_cursor_position()
