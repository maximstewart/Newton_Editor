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
from .source_view_events import SourceViewEventsMixin
from .custom_completion_providers.example_completion_provider import ExampleCompletionProvider
from .custom_completion_providers.python_completion_provider import PythonCompletionProvider



class SourceView(SourceViewEventsMixin, GtkSource.View):
    def __init__(self):
        super(SourceView, self).__init__()

        self._language_manager       = GtkSource.LanguageManager()
        self._style_scheme_manager   = GtkSource.StyleSchemeManager()

        self._file_loader            = None
        self._file_change_watcher    = None
        self._file_cdr_watcher       = None
        self._current_file: Gio.File = None

        self._current_filename: str  = ""
        self._current_filepath: str  = None
        self._current_filetype: str  = "buffer"

        self._skip_file_load         = False
        self._is_changed             = False
        self._ignore_internal_change = False
        self._buffer                 = self.get_buffer()
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

        self._create_default_tag()
        self.set_buffer_language()
        self.set_buffer_style()

        self.set_vexpand(True)


    def _setup_signals(self):
        self.connect("focus", self._on_widget_focus)
        self.connect("focus-in-event", self._focus_in_event)

        self.connect("drag-data-received", self._on_drag_data_received)
        self.connect("button-press-event", self._button_press_event)

        self._buffer.connect('changed', self._is_modified)
        self._buffer.connect("mark-set", self._on_cursor_move)
        self._buffer.connect('insert-text', self._insert_text)


    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...


    def _document_loaded(self):
        for provider in self._completion.get_providers():
            self._completion.remove_provider(provider)

        # TODO: actually load a meaningful provider based on file type...
        file = self._current_file.get_path()
        word_completion = GtkSource.CompletionWords.new("word_completion")
        word_completion.register(self._buffer)
        self._completion.add_provider(word_completion)

        # example_completion_provider = ExampleCompletionProvider()
        # self._completion.add_provider(example_completion_provider)

        py_completion_provider = PythonCompletionProvider(file)
        self._completion.add_provider(py_completion_provider)


    def _create_default_tag(self):
        general_style_tag = self._buffer.create_tag('general_style')
        general_style_tag.set_property('size', 100)
        general_style_tag.set_property('scale', 100)

    def _is_modified(self, *args):
        self._is_changed = True
        self.update_cursor_position()

    def _insert_text(self, text_buffer, location_itr, text_str, len_int):
        if self.freeze_multi_line_insert: return

        if len(self._multi_insert_marks) > 0:
            self._buffer.begin_user_action()
            self.freeze_multi_line_insert = True

        with self._buffer.freeze_notify():
            GLib.idle_add(self._update_multi_line_markers, *(text_str,))

    def _button_press_event(self, widget = None, eve = None, user_data = None):
        if eve.type == Gdk.EventType.BUTTON_PRESS and eve.button == 1 :   # l-click
            if eve.state & Gdk.ModifierType.CONTROL_MASK:
                self.button_press_insert_mark(eve)
                return True
            else:
                self.keyboard_clear_marks()
        elif eve.type == Gdk.EventType.BUTTON_RELEASE and eve.button == 3: # r-click
            ...

    def _focus_in_event(self, widget, eve = None):
        event_system.emit("set_active_src_view", (self,))
        self.get_parent().get_parent().is_editor_focused = True

    def _on_widget_focus(self, widget, eve = None):
        target = self.get_parent().get_parent().NAME
        path   = self._current_file if self._current_file else ""

        event_system.emit('focused_target_changed', (target,))
        event_system.emit("set_path_label", (path,))
        event_system.emit("set_encoding_label")
        event_system.emit("set_file_type_label", (self._current_filetype,))

        return False

    def _on_cursor_move(self, buf, cursor_iter, mark, user_data = None):
        if mark != buf.get_insert(): return

        self.update_cursor_position()

        # NOTE: Not sure but this might not be efficient if the map reloads the same view...
        event_system.emit(f"set_source_view", (self,))

    def _set_up_dnd(self):
        PLAIN_TEXT_TARGET_TYPE = 70
        URI_TARGET_TYPE        = 80
        text_target        = Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags(0), PLAIN_TEXT_TARGET_TYPE)
        uri_target         = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)
        targets            = [ text_target, uri_target ]
        self.drag_dest_set_target_list(targets)

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 70: return

        if info == 80:
            uris  = data.get_uris()

            if len(uris) == 0:
                uris = data.get_text().split("\n")

            if self._is_changed:
                # TODO: Impliment change detection and offer to save as new file
                # Need to insure self._current_file gets set for further flow logic to work
                # self.maybe_saved()
                ...

            if not self._current_file:
                gfile = Gio.File.new_for_uri(uris[0])
                self.open_file(gfile)
                uris.pop(0)

            for uri in uris:
                gfile = None
                try:
                    gfile = Gio.File.new_for_uri(uri)
                except Exception as e:
                    gfile = Gio.File.new_for_path(uri)

                event_system.emit('create_view', (gfile,))
