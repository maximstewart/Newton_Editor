# Python imports

# Lib imports

# Application imports



class EditorControllerMixin:
    def action_controller(self, action = "", query = ""):
        page_num    = self.get_current_page()
        container   = self.get_nth_page( page_num )
        source_view = container.get_source_view()

        if action == "do_text_search":
            self.do_text_search(source_view, query)
        if action == "set_buffer_language":
            self.set_buffer_language(source_view, query)
        if action == "set_buffer_style":
            self.set_buffer_style(source_view, query)
        if action == "toggle_highlight_line":
            self.toggle_highlight_line(source_view)
        if action == "scale_up_text":
            self.scale_up_text(source_view)
        if action == "scale_down_text":
            self.scale_down_text(source_view)
        if action == "close_tab":
            self.close_tab(None, container, source_view)
        if action == "keyboard_prev_tab":
            self.keyboard_prev_tab(page_num)
        if action == "keyboard_next_tab":
            self.keyboard_next_tab(page_num)
