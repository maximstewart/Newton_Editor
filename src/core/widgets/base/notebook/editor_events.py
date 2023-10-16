# Python imports

# Lib imports

# Application imports
from ..sourceview_container import SourceViewContainer



class EditorEventsMixin:
    def create_view(self, widget = None, eve = None, gfile = None, line: int = 0):
        container = SourceViewContainer(self.close_tab)
        page_num  = self.append_page(container, container.get_tab_widget())

        self.set_tab_detachable(container, True)

        ctx = self.get_style_context()
        ctx.add_class("notebook-unselected-focus")
        self.set_tab_reorderable(container, True)

        self.show_all()
        self.set_current_page(page_num)

        if gfile:
            source_view = container.get_source_view()
            source_view.open_file(gfile, line)
            source_view.grab_focus()

    def open_file(self, gfile):
        page_num    = self.get_current_page()
        container   = self.get_nth_page( page_num )
        source_view = container.get_source_view()

        if source_view._current_filename == "":
            source_view.open_file(gfile)
        else:
            self.create_view(None, None, gfile)

    def close_tab(self, button, container, source_view, eve = None):
        if self.NAME == "notebook_1" and self.get_n_pages() == 1:
            return

        page_num = self.page_num(container)
        source_view._cancel_current_file_watchers()
        self.remove_page(page_num)

        if self.NAME == "notebook_2" and self.get_n_pages() == 0:
            self.hide()

    def keyboard_prev_tab(self, page_num):
        page_num = self.get_n_pages() - 1 if page_num == 0 else page_num - 1
        self.set_current_page(page_num)

    def keyboard_next_tab(self, page_num):
        page_num = 0 if self.get_n_pages() - 1 == page_num else page_num + 1
        self.set_current_page(page_num)

    def keyboard_move_tab_to_1(self, page_num):
        notebook = self.builder.get_object("notebook_1")
        if self.NAME == "notebook_1":
            if self.get_n_pages() == 1:
                return

            notebook = self.builder.get_object("notebook_2")

        page = self.get_nth_page(page_num)
        tab  = page.get_tab_widget()
        self.detach_tab(page)

        notebook.insert_page(page, tab, -1)
        notebook.show()

    def keyboard_move_tab_to_2(self, page_num):
        if self.NAME == "notebook_1" and self.get_n_pages() == 1:
            return

        notebook = self.builder.get_object("notebook_2")
        if self.NAME == "notebook_2":
            notebook = self.builder.get_object("notebook_1")

        page = self.get_nth_page(page_num)
        tab  = page.get_tab_widget()
        self.detach_tab(page)

        notebook.insert_page(page, tab, -1)
        notebook.show()
        if self.NAME == "notebook_2" and self.get_n_pages() == 0:
            self.hide()

    def keyboard_move_tab_left(self, page_num):
        page     = self.get_nth_page(page_num)
        page_num = self.get_n_pages() - 1 if page_num == 0 else page_num - 1
        self.reorder_child(page, page_num)

    def keyboard_move_tab_right(self, page_num):
        page     = self.get_nth_page(page_num)
        page_num = 0 if self.get_n_pages() - 1 == page_num else page_num + 1
        self.reorder_child(page, page_num)




    # NOTE: These feel bad being here man...
    def keyboard_undo(self, source_view):
        source_view.keyboard_undo()

    def keyboard_redo(self, source_view):
        source_view.keyboard_redo()

    def scale_up_text(self, source_view):
        source_view.scale_up_text()

    def scale_down_text(self, source_view):
        source_view.scale_down_text()

    def toggle_highlight_line(self, source_view):
        source_view.toggle_highlight_line()

    def keyboard_insert_mark(self, source_view):
        source_view.keyboard_insert_mark()

    def keyboard_clear_marks(self, source_view):
        source_view.keyboard_clear_marks()

    def move_lines_up(self, source_view):
        source_view.move_lines_up()

    def move_lines_down(self, source_view):
        source_view.move_lines_down()

    def set_buffer_language(self, source_view, language = "python3"):
        source_view.set_buffer_language(language)

    def set_buffer_style(self, source_view, style = settings.theming.syntax_theme):
        source_view.set_buffer_style(style)