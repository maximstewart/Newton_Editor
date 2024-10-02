# Python imports
import zipfile

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio

# Application imports
from .editor_controller import EditorControllerMixin



# NOTE: https://github.com/Axel-Erfurt/TextEdit/tree/b65f09be945196eb05bef83d81a6abcd129b4eb0
class EditorNotebook(EditorControllerMixin, Gtk.Notebook):
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
        self.set_vexpand(True)
        self.set_hexpand(True)

    def _setup_signals(self):
        self.connect("switch-page", self._switch_page_update)
        self.connect("key-press-event", self._key_press_event)
        self.connect("key-release-event", self._key_release_event)

    def _subscribe_to_events(self):
        event_system.subscribe("handle-lsp-message", self._handle_lsp_message)

        event_system.subscribe("create_view", self._create_view)
        event_system.subscribe("set_buffer_style", self.action_controller)
        event_system.subscribe("set_buffer_language", self.action_controller)
        event_system.subscribe("focused_target_changed", self._focused_target_changed)

        event_system.subscribe("keyboard_open_file", self._keyboard_open_file)
        event_system.subscribe("keyboard_scale_up_text", self._keyboard_scale_up_text)
        event_system.subscribe("keyboard_scale_down_text", self._keyboard_scale_down_text)
        event_system.subscribe("keyboard_focus_1st_pane", self.keyboard_focus_1st_pane)
        event_system.subscribe("keyboard_focus_2nd_pane", self.keyboard_focus_2nd_pane)

    def _load_widgets(self):
        self._add_action_widgets()
        if self.NAME == "notebook_1" and not settings_manager.is_starting_with_file():
            self.create_view()

    def _dbl_click_create_view(self, notebook, eve):
        if eve.type == Gdk.EventType.DOUBLE_BUTTON_PRESS and eve.button == 1:   # l-click
            ...

    def _focused_target_changed(self, target):
        self.is_editor_focused = True if target == self.NAME else False
        if self.is_editor_focused:
            self.grab_focus()

    def _add_action_widgets(self):
        start_box = Gtk.Box()
        end_box   = Gtk.Box()

        add_btn = Gtk.Button()
        add_btn.set_image( Gtk.Image.new_from_icon_name("add", 4) )
        add_btn.set_always_show_image(True)
        add_btn.connect("released", self.create_view)

        end_box.add(add_btn)

        start_box.show_all()
        end_box.show_all()

        # PACKTYPE: 0 Start, 1 = End
        self.set_action_widget(start_box, 0)
        self.set_action_widget(end_box, 1)

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

        event_system.emit(f"set_source_view", (source_view,))

    def _create_view(self, gfile = None, line: int = 0):
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        if isinstance(gfile, str):
            parts = gfile.replace("file://", "").split(":")
            if len(parts) > 2:
                with zipfile.ZipFile(parts[0], 'r') as file:
                    file.extract(parts[1][1:], "/tmp/newton_extracts")

                gfile = Gio.File.new_for_path( f"/tmp/newton_extracts/{ parts[1][1:] }" )
                try:
                    line = int(parts[2])
                except Exception:
                    ...
            else:
                gfile = Gio.File.new_for_path(parts[0])
                try:
                    line = int(parts[1]) if len(parts) > 1 else 0
                except Exception:
                    ...

        self.create_view(None, None, gfile, line)

    def _keyboard_open_file(self, gfiles = []):
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        for gfile in gfiles:
            self.open_file(gfile)

    def _keyboard_scale_up_text(self):
        self.action_controller("scale_up_text")

    def _keyboard_scale_down_text(self):
        self.action_controller("scale_down_text")