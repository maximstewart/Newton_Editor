# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio

# Application imports
from ..sourceview_container import SourceViewContainer
from .editor_controller import EditorControllerMixin
from .editor_events import EditorEventsMixin



# NOTE: https://github.com/Axel-Erfurt/TextEdit/tree/b65f09be945196eb05bef83d81a6abcd129b4eb0

class EditorNotebook(EditorEventsMixin, EditorControllerMixin, Gtk.Notebook):
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
        # self.connect("button-press-event", self._dbl_click_create_view)
        ...

    def _subscribe_to_events(self):
        # event_system.subscribe("set_buffer_language", self.action_controller, *("set_buffer_language",))
        event_system.subscribe("create_view", self.create_view)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("set_buffer_language", self.action_controller)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("toggle_highlight_line", self._toggle_highlight_line)
        event_system.subscribe("keyboard_create_tab", self._keyboard_create_tab)
        event_system.subscribe("keyboard_open_file", self._keyboard_open_file)
        event_system.subscribe("keyboard_close_tab", self._keyboard_close_tab)
        event_system.subscribe("keyboard_prev_tab", self._keyboard_prev_tab)
        event_system.subscribe("keyboard_next_tab", self._keyboard_next_tab)
        event_system.subscribe("keyboard_scale_up_text", self._keyboard_scale_up_text)
        event_system.subscribe("keyboard_scale_down_text", self._keyboard_scale_down_text)
        event_system.subscribe("keyboard_save_file", self._keyboard_save_file)
        event_system.subscribe("keyboard_save_file_as", self._keyboard_save_file_as)

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

    def _dbl_click_create_view(self, notebook, eve):
        if eve.type == Gdk.EventType.DOUBLE_BUTTON_PRESS and eve.button == 1:   # l-click
            ...

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

    def open_file(self, gfile):
        page_num    = self.get_current_page()
        container   = self.get_nth_page( page_num )
        source_view = container.get_source_view()

        if source_view._current_filename == "":
            source_view.open_file(gfile)
        else:
            self.create_view(None, None, gfile)

    def close_tab(self, button, container, source_view, eve = None):
        if self.get_n_pages() == 1:
            return

        page_num = self.page_num(container)
        source_view._cancel_current_file_watchers()
        self.remove_page(page_num)
