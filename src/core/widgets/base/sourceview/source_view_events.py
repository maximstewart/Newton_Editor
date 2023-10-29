# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .source_file_events_mixin import FileEventsMixin
from .source_marks_events_mixin import MarkEventsMixin



class SourceViewEventsMixin(MarkEventsMixin, FileEventsMixin):

    def set_buffer_language(self, buffer, language = "python3"):
        buffer.set_language( self._language_manager.get_language(language) )

    def set_buffer_style(self, buffer, style = settings.theming.syntax_theme):
        buffer.set_style_scheme( self._style_scheme_manager.get_scheme(style) )

    def toggle_highlight_line(self, widget = None, eve = None):
        self.set_highlight_current_line( not self.get_highlight_current_line() )

    def scale_up_text(self, buffer, scale_step = 10):
        ctx = self.get_style_context()

        if self._px_value < 99:
            self._px_value += 1
            ctx.add_class(f"px{self._px_value}")

        # NOTE: Hope to bring this or similar back after we decouple scaling issues coupled with the miniview.
        # tag_table = buffer.get_tag_table()
        # start_itr = buffer.get_start_iter()
        # end_itr   = buffer.get_end_iter()
        # tag       = tag_table.lookup('general_style')
        #
        # tag.set_property('scale', tag.get_property('scale') + scale_step)
        # buffer.apply_tag(tag, start_itr, end_itr)

    def scale_down_text(self, buffer, scale_step = 10):
        ctx = self.get_style_context()

        if self._px_value > 1:
            ctx.remove_class(f"px{self._px_value}")
            self._px_value -= 1
            ctx.add_class(f"px{self._px_value}")

        # NOTE: Hope to bring this or similar back after we decouple scaling issues coupled with the miniview.
        # tag_table = buffer.get_tag_table()
        # start_itr = buffer.get_start_iter()
        # end_itr   = buffer.get_end_iter()
        # tag       = tag_table.lookup('general_style')
        #
        # tag.set_property('scale', tag.get_property('scale') - scale_step)
        # buffer.apply_tag(tag, start_itr, end_itr)

    def update_cursor_position(self, buffer = None):
        buffer = self.get_buffer() if not buffer else buffer
        iter   = buffer.get_iter_at_mark( buffer.get_insert() )
        chars  = iter.get_offset()
        row    = iter.get_line() + 1
        col    = self.get_visual_column(iter) + 1

        event_system.emit("set_line_char_label", (f"{row}:{col}",))

    def got_to_line(self, buffer = None, line: int = 0):
        buffer    = self.get_buffer() if not buffer else buffer
        line_itr  = buffer.get_iter_at_line(line)
        char_iter = buffer.get_iter_at_line_offset(line, line_itr.get_bytes_in_line())

        buffer.place_cursor(char_iter)
        if not buffer.get_mark("starting_cursor"):
             buffer.create_mark("starting_cursor", char_iter, True)
        self.scroll_to_mark( buffer.get_mark("starting_cursor"), 0.0, True, 0.0, 0.0 )

    def keyboard_undo(self):
        buffer = self.get_buffer()
        buffer.undo()

    def keyboard_redo(self):
        buffer = self.get_buffer()
        buffer.redo()

    def keyboard_move_lines_up(self):
        buffer = self.get_buffer()

        self.begin_user_action(buffer)

        self.emit("move-lines", *(False,))
        # unindent_lines
        # self.emit("move-words", *(self, 4,))

        self.end_user_action(buffer)

    def keyboard_move_lines_down(self):
        buffer = self.get_buffer()

        self.begin_user_action(buffer)

        self.emit("move-lines", *(True,))
        # self.emit("move-words", *(self, -4,))

        self.end_user_action(buffer)

    def update_labels(self, gfile = None):
        if not gfile: return

        tab_widget = self.get_parent().get_tab_widget()
        tab_widget.set_tab_label(self._current_filename)
        self.set_bottom_labels(gfile)

    def set_bottom_labels(self, gfile = None):
        if not gfile: return

        event_system.emit("set_bottom_labels", (gfile, None, self._current_filetype, None))
        self.update_cursor_position()