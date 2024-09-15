# Python imports
import threading

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import GtkSource

# Application imports
from .source_view_controller import SourceViewControllerMixin

# from .custom_completion_providers.example_completion_provider import ExampleCompletionProvider
# from .custom_completion_providers.python_completion_provider import PythonCompletionProvider



class SourceView(SourceViewControllerMixin, GtkSource.View):
    def __init__(self):
        super(SourceView, self).__init__()

        self._language_manager       = GtkSource.LanguageManager()
        self._style_scheme_manager   = GtkSource.StyleSchemeManager()

        self._file_loader            = None
        self._file_change_watcher    = None
        self._current_file: Gio.File = None

        self._current_filename: str  = ""
        self._current_filepath: str  = None
        self._current_filetype: str  = "buffer"
        self._cut_buffer: str        = ""
        self._timer: threading.Timer = None
        self._idle_id: int           = None
        self._version_id: int        = 1

        self._skip_file_load         = False
        self._ignore_internal_change = False
        self._loading_file           = False
        self._completion             = self.get_completion()
        self._px_value               = settings.theming.default_zoom

        self._multi_insert_marks      = []
        self.freeze_multi_line_insert = False

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("source-view")
        ctx.add_class(f"px{self._px_value}")

        self.set_vexpand(True)

        self.set_show_line_marks(True)
        self.set_show_line_numbers(True)
        self.set_smart_backspace(True)
        self.set_indent_on_tab(True)
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_auto_indent(True)
        self.set_monospace(True)
        self.set_tab_width(4)
        self.set_show_right_margin(True)
        self.set_right_margin_position(80)
        self.set_background_pattern(0) # 0 = None, 1 = Grid

        buffer = self.get_buffer()
        self._create_default_tag(buffer)
        self.set_buffer_language(buffer)
        self.set_buffer_style(buffer)


    def _setup_signals(self):
        self.connect("focus", self._on_widget_focus)
        self.connect("focus-in-event", self._focus_in_event)

        self.connect("drag-data-received", self._on_drag_data_received)
        self.connect("key-press-event", self._key_press_event)
        self.connect("key-release-event", self._key_release_event)
        self.connect("button-press-event", self._button_press_event)
        self.connect("scroll-event", self._scroll_event)
        self.connect("show-completion", self._show_completion)

        buffer = self.get_buffer()
        buffer.connect('changed', self._is_modified)
        buffer.connect("mark-set", self._on_cursor_move)
        buffer.connect('insert-text', self._insert_text)
        buffer.connect('modified-changed', self._buffer_modified_changed)

    def _show_completion(self, source_view):
        event_system.emit("textDocument/completion", (source_view, ))

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self._set_up_dnd()

    def cancel_timer(self):
        if self._timer:
            self._timer.cancel()
            GLib.idle_remove_by_data(self._idle_id)

    def delay_cut_buffer_clear_glib(self):
        self._idle_id = GLib.idle_add(self._clear_cut_buffer)

    def clear_cut_buffer_delayed(self):
        self._timer = threading.Timer(15, self.delay_cut_buffer_clear_glib, ())
        self._timer.daemon = True
        self._timer.start()

    def _clear_cut_buffer(self):
        self._cut_buffer = ""