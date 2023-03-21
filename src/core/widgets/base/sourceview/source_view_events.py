# Python imports

# Lib imports

# Application imports



class SourceViewEventsMixin:
    def _create_default_tag(self):
        self._general_style_tag = self._buffer.create_tag('general_style')
        self._general_style_tag.set_property('size', 100)
        self._general_style_tag.set_property('scale', 100)

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

    def _on_cursor_move(self, buf, cursor_iter, mark, user_data = None):
        if mark != buf.get_insert():
            return

        self.update_cursor_position()

    def update_cursor_position(self):
        iter  = self._buffer.get_iter_at_mark(self._buffer.get_insert())
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


    # https://github.com/ptomato/inform7-ide/blob/main/src/actions.c
    def action_uncomment_selection(self):
        ...

    def action_comment_out_selection(self):
        pass
