# Python imports

# Lib imports

# Application imports



class EditorControllerMixin:
    def get_active_view(self):
        page_num    = self.get_current_page()
        container   = self.get_nth_page( page_num )
        source_view = container.get_source_view()
        return page_num, container, source_view

    def action_controller(self, action = "", query = ""):
        # NOTE: Not efficent here as multiple same calls
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        page_num, container, source_view = self.get_active_view()
        if action == "close_tab":
            self.close_tab(None, container, source_view)
        if action == "keyboard_prev_tab":
            self.keyboard_prev_tab(page_num)
        if action == "keyboard_next_tab":
            self.keyboard_next_tab(page_num)
        if action == "keyboard_move_tab_left":
            self.keyboard_move_tab_left(page_num)
        if action == "keyboard_move_tab_right":
            self.keyboard_move_tab_right(page_num)
        if action == "keyboard_move_tab_to_1":
            self.keyboard_move_tab_to_1(page_num)
        if action == "keyboard_move_tab_to_2":
            self.keyboard_move_tab_to_2(page_num)


        # NOTE: These feel bad being here man...
        if action == "scale_up_text":
            self.scale_up_text(source_view)
        if action == "scale_down_text":
            self.scale_down_text(source_view)
        if action == "toggle_highlight_line":
            self.toggle_highlight_line(source_view)
        if action == "keyboard_insert_mark":
            self.keyboard_insert_mark(source_view)
        if action == "keyboard_clear_marks":
            self.keyboard_clear_marks(source_view)
        if action == "move_lines_up":
            self.move_lines_up(source_view)
        if action == "move_lines_down":
            self.move_lines_down(source_view)
        if action == "keyboard_tggl_comment":
            self.keyboard_tggl_comment(source_view)
        if action == "set_buffer_language":
            self.set_buffer_language(source_view, query)
        if action == "set_buffer_style":
            self.set_buffer_style(source_view, query)
        if action == "save_file":
            source_view.save_file()
        if action == "save_file_as":
            source_view.save_file_as()
