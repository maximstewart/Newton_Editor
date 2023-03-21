# Python imports

# Lib imports

# Application imports



class EditorEventsMixin:
    def _toggle_highlight_line(self):
        self.action_controller("toggle_highlight_line")

    def _keyboard_close_tab(self):
        self.action_controller("close_tab")

    def _keyboard_create_tab(self, _gfile):
        self.create_view(gfile=_gfile)

    def _keyboard_next_tab(self):
        self.action_controller("keyboard_next_tab")

    def _keyboard_prev_tab(self):
        self.action_controller("keyboard_prev_tab")

    def _keyboard_scale_up_text(self):
        self.action_controller("scale_up_text")

    def _keyboard_scale_down_text(self):
        self.action_controller("scale_down_text")

    def _keyboard_save_file(self):
        ...

    def _keyboard_save_file_as(self):
        ...

    def _text_search(self, widget = None, eve = None):
        self.action_controller("do_text_search", widget.get_text())

    def do_text_search(self, query = ""):
        source_view.scale_down_text()

    def set_buffer_language(self, source_view, language = "python3"):
        source_view.set_buffer_language(language)

    def set_buffer_style(self, source_view, style = "tango"):
        source_view.set_buffer_style(style)

    def keyboard_prev_tab(self, page_num):
        page_num = self.get_n_pages() - 1 if page_num == 0 else page_num - 1
        self.set_current_page(page_num)

    def keyboard_next_tab(self, page_num):
        page_num = 0 if self.get_n_pages() - 1 == page_num else page_num + 1
        self.set_current_page(page_num)

    def scale_up_text(self, source_view):
        source_view.scale_up_text()

    def scale_down_text(self, source_view):
        source_view.scale_down_text()

    def toggle_highlight_line(self, source_view):
        source_view.toggle_highlight_line()
