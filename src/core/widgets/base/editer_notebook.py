# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..tab_header_widget import TabHeaderWidget
from .source_view import SourceView



class EditorNotebook(Gtk.Notebook):
    def __init__(self):
        super(EditorNotebook, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self.create_view()

    def create_view(self):
        scroll_view = Gtk.ScrolledWindow()
        source_view = SourceView()
        tab_widget  = TabHeaderWidget(scroll_view, source_view, self.close_tab)
        scroll_view.add(source_view)

        index = self.append_page(scroll_view, tab_widget)
        self.set_tab_detachable(scroll_view, True)
        self.set_current_page(index)

        ctx = self.get_style_context()
        ctx.add_class("notebook-unselected-focus")
        self.set_tab_reorderable(scroll_view, True)

    def close_tab(self, button, scroll_view, source_view, eve=None):
        if self.get_n_pages() == 1:
            return

        page_num = self.page_num(scroll_view)
        watcher  = source_view.get_file_watcher()
        if watcher:
            watcher.cancel()

        self.remove_page(page_num)
