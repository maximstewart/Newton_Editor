# Python imports

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
# from .auto_indenter import AutoIndenter
from .key_input_controller import KeyInputController
from .source_view_events import SourceViewEventsMixin
from .custom_completion_providers.example_completion_provider import ExampleCompletionProvider
from .custom_completion_providers.python_completion_provider import PythonCompletionProvider



class SourceView(KeyInputController, SourceViewEventsMixin, GtkSource.View):
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

        self._skip_file_load         = False
        self._ignore_internal_change = False
        self._loading_file           = False
        self._completion             = self.get_completion()
        self._px_value               = settings.theming.default_zoom

        self._multi_insert_marks      = []
        self.freeze_multi_line_insert = False

        self._setup_styling()
        self._setup_signals()
        self._set_up_dnd()
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
        # NOTE: Add back once we move to Gtk 4 and use GtkSource 5
        # self.set_indenter( AutoIndenter() )

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

        buffer = self.get_buffer()
        buffer.connect('changed', self._is_modified)
        buffer.connect("mark-set", self._on_cursor_move)
        buffer.connect('insert-text', self._insert_text)
        buffer.connect('modified-changed', self._buffer_modified_changed)


    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...


    def _document_loaded(self, line: int = 0):
        for provider in self._completion.get_providers():
            self._completion.remove_provider(provider)

        file   = self._current_file.get_path()
        buffer = self.get_buffer()

        word_completion = GtkSource.CompletionWords.new("word_completion")
        word_completion.register(buffer)
        self._completion.add_provider(word_completion)

        # TODO: actually load a meaningful provider based on file type...
        # example_completion_provider = ExampleCompletionProvider()
        # self._completion.add_provider(example_completion_provider)

        # py_completion_provider = PythonCompletionProvider(file)
        # self._completion.add_provider(py_completion_provider)
        self.got_to_line(buffer, line)


    def _create_default_tag(self, buffer):
        general_style_tag = buffer.create_tag('general_style')
        general_style_tag.set_property('size', 100)
        general_style_tag.set_property('scale', 100)

    def _is_modified(self, *args):
        buffer = self.get_buffer()

        if not self._loading_file:
            event_system.emit("buffer_changed", (buffer, ))
        else:
            event_system.emit("buffer_changed_first_load", (buffer, ))

        self.update_cursor_position(buffer)

    def _insert_text(self, buffer, location_itr, text_str, len_int):
        if self.freeze_multi_line_insert: return

        self.begin_user_action(buffer)
        with buffer.freeze_notify():
            GLib.idle_add(self._update_multi_line_markers, *(buffer, text_str,))

    def _buffer_modified_changed(self, buffer):
        tab_widget = self.get_parent().get_tab_widget()
        tab_widget.set_status(changed = True if buffer.get_modified() else False)


    def _button_press_event(self, widget = None, eve = None, user_data = None):
        if eve.type == Gdk.EventType.BUTTON_PRESS and eve.button == 1 :   # l-click
            if eve.state & Gdk.ModifierType.CONTROL_MASK:
                self.button_press_insert_mark(eve)
                return True
            else:
                self.keyboard_clear_marks()
        elif eve.type == Gdk.EventType.BUTTON_RELEASE and eve.button == 3: # r-click
            ...

    def _scroll_event(self, widget, eve):
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        x, y, z    = eve.get_scroll_deltas()
        if eve.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            buffer = self.get_buffer()
            if z > 0:
                self.scale_down_text(buffer)
            else:
                self.scale_up_text(buffer)

            return True

        if eve.state & accel_mask == Gdk.ModifierType.SHIFT_MASK:
            adjustment  = self.get_hadjustment()
            current_val = adjustment.get_value()
            step_val    = adjustment.get_step_increment()

            if z > 0: # NOTE: scroll left
                adjustment.set_value(current_val - step_val * 2)
            else:     # NOTE: scroll right
                adjustment.set_value(current_val + step_val * 2)

            return True

    def _focus_in_event(self, widget, eve = None):
        event_system.emit("set_active_src_view", (self,))
        self.get_parent().get_parent().is_editor_focused = True

    def _on_widget_focus(self, widget, eve = None):
        tab_view = self.get_parent().get_parent()
        path     = self._current_file if self._current_file else ""

        event_system.emit('focused_target_changed', (tab_view.NAME,))
        event_system.emit("set_path_label", (path,))
        event_system.emit("set_encoding_label")
        event_system.emit("set_file_type_label", (self._current_filetype,))

        return False

    def _on_cursor_move(self, buffer, cursor_iter, mark, user_data = None):
        if mark != buffer.get_insert(): return

        self.update_cursor_position(buffer)

        # NOTE: Not sure but this might not be efficient if the map reloads the same view...
        event_system.emit(f"set_source_view", (self,))