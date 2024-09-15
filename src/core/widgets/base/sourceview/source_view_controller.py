# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

# Application imports
from .key_input_controller import KeyInputController
from .source_view_events import SourceViewEvents



class SourceViewControllerMixin(KeyInputController, SourceViewEvents):
    def get_text(self):
        buffer = self.get_buffer()
        start_itr, end_itr = buffer.get_bounds()
        return buffer.get_text(start_itr, end_itr, True)

    def get_current_file(self):
        return self._current_file

    def get_filetype(self):
        return self._current_filetype

    def get_version_id(self):
        return self._version_id

    def set_buffer_language(self, buffer, language = "python3"):
        buffer.set_language( self._language_manager.get_language(language) )

    def set_buffer_style(self, buffer, style = settings.theming.syntax_theme):
        buffer.set_style_scheme( self._style_scheme_manager.get_scheme(style) )

    def go_to_call(self):
        buffer  = self.get_buffer()
        iter    = buffer.get_iter_at_mark( buffer.get_insert() )
        line    = iter.get_line()
        offset  = iter.get_line_offset()
        uri     = self.get_current_file().get_uri()

        event_system.emit("textDocument/definition", (self.get_filetype(), uri, line, offset,))

    def duplicate_line(self, buffer = None):
        buffer     = self.get_buffer() if not buffer else buffer
        itr        = buffer.get_iter_at_mark( buffer.get_insert() )
        start_itr  = itr.copy()
        end_itr    = itr.copy()
        start_line = itr.get_line() + 1
        start_char = itr.get_line_offset()

        start_itr.backward_visible_line()
        start_itr.forward_line()
        end_itr.forward_line()
        end_itr.backward_char()

        line_str     = buffer.get_slice(start_itr, end_itr, True)

        end_itr.forward_char()
        buffer.insert(end_itr, f"{line_str}\n", -1)

        new_itr      = buffer.get_iter_at_line_offset(start_line, start_char)
        buffer.place_cursor(new_itr)

    def cut_to_buffer(self, buffer = None):
        self.cancel_timer()

        buffer     = self.get_buffer() if not buffer else buffer
        itr        = buffer.get_iter_at_mark( buffer.get_insert() )
        start_itr  = itr.copy()
        end_itr    = itr.copy()
        start_line = itr.get_line() + 1
        start_char = itr.get_line_offset()

        start_itr.backward_visible_line()
        start_itr.forward_line()
        end_itr.forward_line()

        line_str     = buffer.get_slice(start_itr, end_itr, True)
        self._cut_buffer += f"{line_str}"
        buffer.delete(start_itr, end_itr)

        self.clear_cut_buffer_delayed()

    def paste_cut_buffer(self, buffer = None):
        self.cancel_timer()

        buffer     = self.get_buffer() if not buffer else buffer
        itr        = buffer.get_iter_at_mark( buffer.get_insert() )
        insert_itr = itr.copy()

        buffer.insert(insert_itr, self._cut_buffer, -1)

        self.clear_cut_buffer_delayed()

    def update_cursor_position(self, buffer = None):
        buffer = self.get_buffer() if not buffer else buffer
        iter   = buffer.get_iter_at_mark( buffer.get_insert() )
        chars  = iter.get_offset()
        row    = iter.get_line() + 1
        col    = self.get_visual_column(iter) + 1

        event_system.emit("set_line_char_label", (f"{row}:{col}",))

    def update_labels(self, gfile = None):
        if not gfile: return

        tab_widget = self.get_parent().get_tab_widget()
        tab_widget.set_tab_label(self._current_filename)
        self.set_bottom_labels(gfile)

    def set_bottom_labels(self, gfile = None):
        if not gfile: return

        event_system.emit("set_bottom_labels", (gfile, None, self._current_filetype, None))
        self.update_cursor_position()

    def got_to_line(self, buffer = None, line: int = 0):
        buffer    = self.get_buffer() if not buffer else buffer
        line_itr  = buffer.get_iter_at_line(line)
        char_iter = buffer.get_iter_at_line_offset(line, line_itr.get_bytes_in_line())

        buffer.place_cursor(char_iter)
        # Note: scroll_to_iter and scroll_to_mark depend on an idle recalculate of buffers after load to work
        GLib.idle_add(self.scroll_to_mark, buffer.get_insert(), 0.1, True, 0.0, 0.1)

    def toggle_highlight_line(self, widget = None, eve = None):
        self.set_highlight_current_line( not self.get_highlight_current_line() )

    def scale_up_text(self, buffer = None, scale_step = 10):
        if not buffer:
            buffer = self.get_buffer()

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

    def scale_down_text(self, buffer = None, scale_step = 10):
        if not buffer:
            buffer = self.get_buffer()

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

    def keyboard_undo(self):
        buffer = self.get_buffer()
        buffer.undo()

    def keyboard_redo(self):
        buffer = self.get_buffer()
        buffer.redo()

    def keyboard_move_lines_up(self):
        buffer           = self.get_buffer()

        self.begin_user_action(buffer)

        had_selection = buffer.get_has_selection()
        itr           = buffer.get_iter_at_mark( buffer.get_insert() )
        line          = itr.get_line() - 1
        line_index    = itr.get_line_index()
        selection_bounds = None

        if had_selection:
            selection_bounds = buffer.get_selection_bounds()
            sbounds_start    = selection_bounds[0].get_line_offset()
            sbounds_end      = selection_bounds[1].get_line_offset()

        self.emit("move-lines", *(False,))
        if not had_selection:
            self.emit("select-all", *(False,))
            line_itr  = buffer.get_iter_at_line_offset(line, line_index)
            self.get_buffer().place_cursor(line_itr)
        else:
            buffer    = self.get_buffer()
            sbounds   = buffer.get_selection_bounds()
            start_itr = buffer.get_iter_at_line_offset( sbounds[0].get_line(), sbounds_start)
            end_itr   = buffer.get_iter_at_line_offset( sbounds[1].get_line() - 1, sbounds_end)

            self.emit("select-all", *(False,))
            buffer.select_range(start_itr, end_itr)

        self.end_user_action(buffer)

    def keyboard_move_lines_down(self):
        buffer           = self.get_buffer()

        self.begin_user_action(buffer)

        had_selection    = buffer.get_has_selection()
        itr              = buffer.get_iter_at_mark( buffer.get_insert() )
        line             = itr.get_line() + 1
        line_index       = itr.get_line_index()
        selection_bounds = None
        sbounds_start    = None
        sbounds_end      = None

        if had_selection:
            selection_bounds = buffer.get_selection_bounds()
            sbounds_start    = selection_bounds[0].get_line_offset()
            sbounds_end      = selection_bounds[1].get_line_offset()

        self.emit("move-lines", *(True,))
        if not had_selection:
            self.emit("select-all", *(False,))
            line_itr  = buffer.get_iter_at_line_offset(line, line_index)
            self.get_buffer().place_cursor(line_itr)
        else:
            buffer    = self.get_buffer()
            sbounds   = buffer.get_selection_bounds()
            start_itr = buffer.get_iter_at_line_offset( sbounds[0].get_line(), sbounds_start)
            end_itr   = buffer.get_iter_at_line_offset( sbounds[1].get_line() - 1, sbounds_end)

            self.emit("select-all", *(False,))
            buffer.select_range(start_itr, end_itr)

        self.end_user_action(buffer)