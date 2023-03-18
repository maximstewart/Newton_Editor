# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource
from gi.repository import Gio

# Application imports



class SourceView(GtkSource.View):
    def __init__(self):
        super(SourceView, self).__init__()

        self._language_manager     = GtkSource.LanguageManager()
        self._style_scheme_manager = GtkSource.StyleSchemeManager()
        self._general_style_tag    = None
        self._file_watcher         = None

        self._buffer = self.get_buffer()

        self._setup_styling()
        self._setup_signals()
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
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        ...

    def _create_default_tag(self):
        self._general_style_tag = self._buffer.create_tag('general_style')
        self._general_style_tag.set_property('size', 100)
        self._general_style_tag.set_property('scale', 100)

    def set_buffer_language(self, language = "python3"):
        self._buffer.set_language( self._language_manager.get_language(language) )

    def set_buffer_style(self, style = "tango"):
        self._buffer.set_style_scheme( self._style_scheme_manager.get_scheme(style) )


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


    def toggle_highlight_line(self, widget = None, eve = None):
        self.set_highlight_current_line( not self.get_highlight_current_line() )

    def scale_up_text(self, scale_step = 10):
        current_scale = self._general_style_tag.get_property('scale')
        start_itr     = self._buffer.get_start_iter()
        end_itr       = self._buffer.get_end_iter()

        self._general_style_tag.set_property('scale',  current_scale + scale_step)
        self._buffer.apply_tag(self._general_style_tag, start_itr, end_itr)

    def scale_down_text(self, scale_step = 10):
        tag_table = self._buffer.get_tag_table()
        start_itr = self._buffer.get_start_iter()
        end_itr   = self._buffer.get_end_iter()
        tag       = tag_table.lookup('general_style')

        tag.set_property('scale', tag.get_property('scale') - scale_step)
        self._buffer.apply_tag(tag, start_itr, end_itr)
