# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio

# Application imports
from .editor_controller import EditorControllerMixin
from .editor_events import EditorEventsMixin



# NOTE: https://github.com/Axel-Erfurt/TextEdit/tree/b65f09be945196eb05bef83d81a6abcd129b4eb0

class EditorNotebook(EditorEventsMixin, EditorControllerMixin, Gtk.Notebook):
    ccount = 0

    def __new__(cls, *args, **kwargs):
        obj        = super(EditorNotebook, cls).__new__(cls)
        cls.ccount += 1

        return obj

    def __init__(self):
        super(EditorNotebook, self).__init__()

        self.NAME              = f"notebook_{self.ccount}"
        self.builder           = settings_manager.get_builder()
        self.is_editor_focused = False

        self.set_group_name("editor_widget")
        self.builder.expose_object(self.NAME, self)

        self._add_action_widgets()
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()

        if self.NAME == "notebook_1":
            self.is_editor_focused = True

        if self.NAME == "notebook_2":
            self.hide()


    def _setup_styling(self):
        self.set_scrollable(True)

    def _setup_signals(self):
        self.connect("switch-page", self._switch_page_update)
        # self.connect("button-press-event", self._dbl_click_create_view)
        ...

    def _subscribe_to_events(self):
        # event_system.subscribe("set_buffer_language", self.action_controller, *("set_buffer_language",))
        event_system.subscribe("create_view", self._create_view)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("set_buffer_language", self.action_controller)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("toggle_highlight_line", self._toggle_highlight_line)
        event_system.subscribe("keyboard_create_tab", self._keyboard_create_tab)
        event_system.subscribe("keyboard_open_file", self._keyboard_open_file)
        event_system.subscribe("keyboard_close_tab", self._keyboard_close_tab)
        event_system.subscribe("keyboard_prev_tab", self._keyboard_prev_tab)
        event_system.subscribe("keyboard_next_tab", self._keyboard_next_tab)
        event_system.subscribe("keyboard_move_tab_left", self._keyboard_move_tab_left)
        event_system.subscribe("keyboard_move_tab_right", self._keyboard_move_tab_right)
        event_system.subscribe("keyboard_move_tab_to_1", self._keyboard_move_tab_to_1)
        event_system.subscribe("keyboard_move_tab_to_2", self._keyboard_move_tab_to_2)
        event_system.subscribe("keyboard_scale_up_text", self._keyboard_scale_up_text)
        event_system.subscribe("keyboard_scale_down_text", self._keyboard_scale_down_text)
        event_system.subscribe("keyboard_save_file", self._keyboard_save_file)
        event_system.subscribe("keyboard_save_file_as", self._keyboard_save_file_as)
        event_system.subscribe("focused_target_changed", self._focused_target_changed)


    def _focused_target_changed(self, target):
        self.is_editor_focused = True if target == self.NAME else False

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
        if self.NAME == "notebook_1" and not settings_manager.is_starting_with_file():
            self.create_view()

    def _dbl_click_create_view(self, notebook, eve):
        if eve.type == Gdk.EventType.DOUBLE_BUTTON_PRESS and eve.button == 1:   # l-click
            ...

    def _switch_page_update(self, notebook, page, page_num):
        source_view = page.get_source_view()
        gfile       = source_view.get_current_file()
        if not gfile:
            event_system.emit("set_path_label", ("",))
            event_system.emit("set_file_type_label", (source_view._current_filetype,))
        else:
            source_view.load_file_info(gfile)
            source_view.update_cursor_position()
            source_view.set_bottom_labels(gfile)

    def _create_view(self, gfile = None, line: int = 0):
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        if isinstance(gfile, str):
            parts = gfile.split(":")
            gfile = Gio.File.new_for_path(parts[0])
            try:
                line = int(parts[1]) if len(parts) > 1 else 0
            except Exception as e:
                ...

        self.create_view(None, None, gfile, line)

    def _keyboard_open_file(self, gfile):
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        self.open_file(gfile)

    def _keyboard_create_tab(self, _gfile = None):
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        self.create_view(gfile = _gfile)


    def _keyboard_close_tab(self):
        self.action_controller("close_tab")

    def _toggle_highlight_line(self):
        self.action_controller("toggle_highlight_line")

    def _keyboard_next_tab(self):
        self.action_controller("keyboard_next_tab")

    def _keyboard_move_tab_left(self):
        self.action_controller("keyboard_move_tab_left")

    def _keyboard_move_tab_right(self):
        self.action_controller("keyboard_move_tab_right")

    def _keyboard_move_tab_to_1(self):
        self.action_controller("keyboard_move_tab_to_1")

    def _keyboard_move_tab_to_2(self):
        self.action_controller("keyboard_move_tab_to_2")

    def _keyboard_prev_tab(self):
        self.action_controller("keyboard_prev_tab")

    def _keyboard_scale_up_text(self):
        self.action_controller("scale_up_text")

    def _keyboard_scale_down_text(self):
        self.action_controller("scale_down_text")

    def _keyboard_save_file(self):
        self.action_controller("save_file")

    def _keyboard_save_file_as(self):
        self.action_controller("save_file_as")

    def _text_search(self, widget = None, eve = None):
        self.action_controller("do_text_search", widget.get_text())
