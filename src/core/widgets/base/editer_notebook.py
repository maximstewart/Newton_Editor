# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .sourceview_container import SourceViewContainer



class EditorNotebook(Gtk.Notebook):
    def __init__(self):
        super(EditorNotebook, self).__init__()

        self.set_group_name("editor_widget")

        self._add_action_widgets()
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_scrollable(True)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        # event_system.subscribe("set_buffer_language", self.action_controller, *("set_buffer_language",))
        event_system.subscribe("create_view", self.create_view)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("set_buffer_language", self.action_controller)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("open_files", self._open_files)
        event_system.subscribe("toggle_highlight_line", self.action_controller)
        event_system.subscribe("keyboard_scale_up_text", self._keyboard_scale_up_text)
        event_system.subscribe("keyboard_scale_down_text", self._keyboard_scale_down_text)
        event_system.subscribe("keyboard_create_tab", self.create_view)
        event_system.subscribe("keyboard_close_tab", self._keyboard_close_tab)

    def _open_files(self):
        print("Open file stub...")

    def _add_action_widgets(self):
        start_box = Gtk.Box()
        end_box   = Gtk.Box()

        search = Gtk.SearchEntry()
        search.set_placeholder_text("Search...")
        search.connect("changed", self._text_search)

        add_btn = Gtk.Button()
        add_btn.set_image( Gtk.Image.new_from_icon_name("add", 4) )
        add_btn.set_always_show_image(True)
        add_btn.connect("released", self.create_view)

        end_box.add(add_btn)
        end_box.add(search)

        start_box.show_all()
        end_box.show_all()

        # PACKTYPE: 0 Start, 1 = End
        self.set_action_widget(start_box, 0)
        self.set_action_widget(end_box, 1)

    def _load_widgets(self):
        self.create_view()

    def create_view(self, widget = None, eve = None, gfile = None):
        container =  SourceViewContainer(self.close_tab)

        index = self.append_page(container, container.get_tab_widget())
        self.set_tab_detachable(container, True)

        ctx = self.get_style_context()
        ctx.add_class("notebook-unselected-focus")
        self.set_tab_reorderable(container, True)

        if gfile:
            source_view = container.get_source_view()
            source_view.open_file(gfile)

        self.show_all()
        self.set_current_page(index)

    def close_tab(self, button, container, source_view, eve = None):
        if self.get_n_pages() == 1:
            return

        page_num = self.page_num(container)
        watcher  = source_view.get_file_watcher()
        if watcher:
            watcher.cancel()

        self.remove_page(page_num)

    def _keyboard_close_tab(self):
        self.action_controller("close_tab")

    def _keyboard_scale_up_text(self):
        self.action_controller("scale_up_text")

    def _keyboard_scale_down_text(self):
        self.action_controller("scale_down_text")

    def _text_search(self, widget = None, eve = None):
        self.action_controller("do_text_search", widget.get_text())

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

    def do_text_search(self, query = ""):
        source_view.scale_down_text()

    def set_buffer_language(self, source_view, language = "python3"):
        source_view.set_buffer_language(language)

    def set_buffer_style(self, source_view, style = "tango"):
        source_view.set_buffer_style(style)

    def scale_up_text(self, source_view):
        source_view.scale_up_text()

    def scale_down_text(self, source_view):
        source_view.scale_down_text()

    def toggle_highlight_line(self, source_view):
        source_view.toggle_highlight_line()
