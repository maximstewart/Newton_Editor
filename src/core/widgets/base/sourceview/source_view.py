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



class SourceView(SourceViewEventsMixin, GtkSource.View):
    def __init__(self):
        super(SourceView, self).__init__()

        self._language_manager     = GtkSource.LanguageManager()
        self._style_scheme_manager = GtkSource.StyleSchemeManager()

        self._general_style_tag    = None
        self._file_watcher         = None
        self._is_changed           = False

        self._current_file: Gio.File = None
        self._file_loader = None
        self._buffer      = self.get_buffer()

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
        # self.completion.add_provider(srcCompleteonSnippets)
        # self.completion.add_provider(srcCompleteonWords)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _is_modified(self, *args):
        self._is_changed = True
        self.update_cursor_position()

    def get_file_watcher(self):
        return self._file_watcher

    def create_file_watcher(self, file_path = None):
        if not file_path:
            return

        if self._file_watcher:
            self._file_watcher.cancel()
            self._file_watcher = None

        self._file_watcher = Gio.File.new_for_path(file_path) \
                                        .monitor_file([
                                                        Gio.FileMonitorFlags.WATCH_MOVES,
                                                        Gio.FileMonitorFlags.WATCH_HARD_LINKS
                                                    ], Gio.Cancellable())

        self._file_watcher.connect("changed", self.file_watch_updates)

    def file_watch_updates(self, file_monitor, file, other_file=None, eve_type=None, data=None):
        if settings.is_debug():
            logger.debug(eve_type)

        if eve_type in [Gio.FileMonitorEvent.CREATED,
                        Gio.FileMonitorEvent.DELETED,
                        Gio.FileMonitorEvent.RENAMED]:
            ...

        if eve_type in [ Gio.FileMonitorEvent.CHANGED ]:
            ...

    def _set_up_dnd(self):
        URI_TARGET_TYPE  = 80
        uri_target       = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)
        targets          = [ uri_target ]
        self.drag_dest_set_target_list(targets)

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
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


    def open_file(self, gfile, *args):
        self._current_file = gfile

        self.load_file_info(gfile)
        self.load_file_async(gfile)
        self.grab_focus()

    def load_file_info(self, gfile):
        info         = gfile.query_info("standard::*", 0, cancellable=None)
        content_type = info.get_content_type()
        display_name = info.get_display_name()
        tab_widget   = self.get_parent().get_tab_widget()

        try:
            lm = self._language_manager.guess_language(None, content_type)
            self.set_buffer_language( lm.get_id() )
        except Exception as e:
            ...

        logger.debug(f"Detected Content Type: {content_type}")
        tab_widget.set_tab_label(display_name)
        event_system.emit("set_bottom_labels", (gfile, info))

    def load_file_async(self, gfile):
        file = GtkSource.File()
        file.set_location(gfile)
        self._file_loader = GtkSource.FileLoader.new(self._buffer, file)

        def finish_load_callback(obj, res, user_data=None):
            self._file_loader.load_finish(res)
            self._is_changed = False

        self._file_loader.load_async(io_priority=98,
                            cancellable=None,
                            progress_callback=None,
                            progress_callback_data=None,
                            callback=finish_load_callback,
                            user_data=(None))
