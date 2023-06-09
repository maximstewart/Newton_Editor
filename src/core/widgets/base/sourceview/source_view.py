# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
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

        self._general_style_tag      = None
        self._file_loader            = None
        self._file_change_watcher    = None
        self._file_cdr_watcher       = None
        self._last_eve_in_queue      = None
        self._current_file: Gio.File = None

        self._current_filename: str  = ""
        self._current_filepath: str  = None
        self._current_filetype: str  = "buffer"

        self._is_changed             = False
        self._ignore_internal_change = False
        self._buffer                 = self.get_buffer()
        self._completion             = self.get_completion()

        self._file_filter_text = Gtk.FileFilter()
        self._file_filter_text.set_name("Text Files")
        # TODO: Need to externalize to settings file...
        pattern = ["*.txt", "*.py", "*.c", "*.h", "*.cpp", "*.csv", "*.m3*", "*.lua", "*.js", "*.toml", "*.xml", "*.pom", "*.htm", "*.md" "*.vala", "*.tsv", "*.css", "*.html", ".json", "*.java", "*.go", "*.php", "*.ts", "*.rs"]
        for p in pattern:
            self._file_filter_text.add_pattern(p)

        self._file_filter_all = Gtk.FileFilter()
        self._file_filter_all.set_name("All Files")
        self._file_filter_all.add_pattern("*.*")

        self._setup_styling()
        self._setup_signals()
        self._set_up_dnd()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
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
        self.connect("drag-data-received", self._on_drag_data_received)
        self._buffer.connect("mark-set", self._on_cursor_move)
        self._buffer.connect('changed', self._is_modified)

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


    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _create_default_tag(self):
        self._general_style_tag = self._buffer.create_tag('general_style')
        self._general_style_tag.set_property('size', 100)
        self._general_style_tag.set_property('scale', 100)

    def _is_modified(self, *args):
        self._is_changed = True
        self.update_cursor_position()

    def _on_cursor_move(self, buf, cursor_iter, mark, user_data = None):
        if mark != buf.get_insert(): return

        target = self.get_parent().get_parent().NAME
        path   = self._current_file if self._current_file else ""

        event_system.emit('focused_target_changed', (target,))
        event_system.emit("set_path_label", (path,))
        event_system.emit("set_encoding_label")
        event_system.emit("set_file_type_label", (self._current_filetype,))
        self.update_cursor_position()

    def _set_up_dnd(self):
        WIDGET_TARGET_TYPE = 70
        URI_TARGET_TYPE    = 80
        widget_target      = Gtk.TargetEntry.new('dummy', Gtk.TargetFlags(0), WIDGET_TARGET_TYPE)
        uri_target         = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)
        targets            = [ widget_target, uri_target ]
        self.drag_dest_set_target_list(targets)

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 70:
            print(drag_context)
            print(data)
            print(info)
            # detach_tab(child)
            return

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

                event_system.emit('create_view', (None, None, gfile,))


    def _create_file_watcher(self, gfile = None):
        if not gfile: return

        self._cancel_current_file_watchers()
        self._file_change_watcher = gfile.monitor(Gio.FileMonitorFlags.NONE, Gio.Cancellable())
        self._file_change_watcher.connect("changed", self._file_monitor)

    def _file_monitor(self, file_monitor, file, other_file = None, eve_type = None, data = None):
        if not file.get_path() == self._current_file.get_path():
            return

        if eve_type in [Gio.FileMonitorEvent.CREATED,
                        Gio.FileMonitorEvent.DELETED,
                        Gio.FileMonitorEvent.RENAMED,
                        Gio.FileMonitorEvent.MOVED_IN,
                        Gio.FileMonitorEvent.MOVED_OUT]:
            self._is_changed = True

        if eve_type in [ Gio.FileMonitorEvent.CHANGES_DONE_HINT ]:
            if self._ignore_internal_change:
                self._ignore_internal_change = False
                return

            # TODO: Any better way to load the difference??
            if self._current_file.query_exists():
                self.load_file_async(self._current_file)

    def _cancel_current_file_watchers(self):
        if self._file_change_watcher:
            self._file_change_watcher.cancel()
            self._file_change_watcher = None

        if self._file_cdr_watcher:
            self._file_cdr_watcher.cancel()
            self._file_cdr_watcher = None

    def _write_file(self, gfile, save_as = False):
        with open(gfile.get_path(), 'w') as f:
            if not save_as:
                self._ignore_internal_change = True
                self._is_changed = False

            start_itr = self._buffer.get_start_iter()
            end_itr   = self._buffer.get_end_iter()
            text      = self._buffer.get_text(start_itr, end_itr, True)

            f.write(text)
            f.close()

            if (self._current_filename == "" and save_as) or \
                (self._current_filename != "" and not save_as):
                    self.open_file(gfile)
            else:
                event_system.emit("create_view", (None, None, gfile,))
