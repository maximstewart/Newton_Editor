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
    
    # Note: Need to get parent instead given we pass the close_tab method
    #       from a potentially former notebook. 
    def close_tab(self, button, container, source_view, eve = None):
        notebook = container.get_parent()
        if notebook.NAME == "notebook_1" and notebook.get_n_pages() == 1:
            return

        file_type = source_view.get_filetype()
        if not file_type == "buffer": 
            uri = source_view.get_current_filepath().get_uri()
            event_system.emit("textDocument/didClose", (file_type, uri,))

        page_num = notebook.page_num(container)
        source_view._cancel_current_file_watchers()
        notebook.remove_page(page_num)

        if notebook.NAME == "notebook_2" and notebook.get_n_pages() == 0:
            notebook.hide()
            event_system.emit("focused_target_changed", ("notebook_1",))

    def keyboard_prev_tab(self, page_num):
        page_num = self.get_n_pages() - 1 if page_num == 0 else page_num - 1
        self.set_current_page(page_num)

    def keyboard_next_tab(self, page_num):
        page_num = 0 if self.get_n_pages() - 1 == page_num else page_num + 1
        self.set_current_page(page_num)

    def keyboard_focus_1st_pane(self):
        if self.NAME == "notebook_1":
            return

        notebook = self.builder.get_object("notebook_1")
        i        = notebook.get_current_page()
        page     = notebook.get_nth_page(i)

        self.set_page_focus_after_move(page, notebook)

    def keyboard_focus_2nd_pane(self):
        if self.NAME == "notebook_2":
            return

        notebook = self.builder.get_object("notebook_2")
        if not notebook.is_visible():
            notebook.show()
            notebook.create_view()

        i        = notebook.get_current_page()
        page     = notebook.get_nth_page(i)

        self.set_page_focus_after_move(page, notebook)

    def keyboard_move_tab_to_1(self, page_num):
        if self.NAME == "notebook_1": return

        notebook = self.builder.get_object("notebook_1")
        page     = self.get_nth_page(page_num)
        tab      = page.get_tab_widget()

        self.detach_tab(page)
        notebook.show()
        notebook.insert_page(page, tab, -1)

        if self.get_n_pages() == 0:
            self.hide()

        self.set_page_focus_after_move(page, notebook)

    def keyboard_move_tab_to_2(self, page_num):
        if self.NAME == "notebook_2":
            return

        if self.NAME == "notebook_1" and self.get_n_pages() == 1:
            return

        notebook = self.builder.get_object("notebook_2")
        page     = self.get_nth_page(page_num)
        tab      = page.get_tab_widget()

        self.detach_tab(page)
        notebook.show()
        notebook.insert_page(page, tab, -1)

        self.set_page_focus_after_move(page, notebook)

    def set_page_focus_after_move(self, page, notebook):
        self.is_editor_focused = False
        notebook.set_current_page(-1)
        page.get_children()[0].grab_focus()
        notebook.is_editor_focused = True
        

    def keyboard_move_tab_left(self, page_num):
        page     = self.get_nth_page(page_num)
        page_num = self.get_n_pages() - 1 if page_num == 0 else page_num - 1
        self.reorder_child(page, page_num)

    def keyboard_move_tab_right(self, page_num):
        page     = self.get_nth_page(page_num)
        page_num = 0 if self.get_n_pages() - 1 == page_num else page_num + 1
        self.reorder_child(page, page_num)


    # NOTE: These feel bad being here man...
    def scale_up_text(self, source_view):
        source_view.scale_up_text()

    def scale_down_text(self, source_view):
        source_view.scale_down_text()

    def set_buffer_language(self, source_view, language = "python3"):
        source_view.set_buffer_language(language)

    def set_buffer_style(self, source_view, style = settings.theming.syntax_theme):
        buffer = source_view.get_buffer()
        source_view.set_buffer_style(buffer, style)