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



class SourceView(GtkSource.View):
    def __init__(self):
        super(SourceView, self).__init__()

        self._language_manager     = GtkSource.LanguageManager()
        self._style_scheme_manager = GtkSource.StyleSchemeManager()

        self._general_style_tag    = None
        self._file_watcher         = None
        self._is_changed           = False

        self._buffer = self.get_buffer()

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
        # self.completion.add_provider(srcCompleteonSnippets)
        # self.completion.add_provider(srcCompleteonWords)

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
                # self.maybe_saved()
                ...

            gfile = Gio.File.new_for_uri(uris[0])
            self.open_file(gfile)

            uris.pop(0)
            for uri in uris:
                gfile = Gio.File.new_for_uri(uri)
                event_system.emit('create_view', (None, None, gfile,))


    def open_file(self, gfile, *args):
        info         = gfile.query_info("standard::*", 0, cancellable=None)
        content_type = info.get_content_type()
        display_name = info.get_display_name()
        tab_widget   = self.get_parent().get_tab_widget()
        lm           = self._language_manager.guess_language(None, content_type)

        tab_widget.set_tab_label(display_name)
        event_system.emit("set_bottom_labels", (gfile, info))

        logger.debug(f"Detected Content Type: {content_type}")
        with open(gfile.get_path(), 'r') as f:
            data = f.read()
            self._buffer.set_text(data)
            try:
                self.set_buffer_language( lm.get_id() )
            except Exception as e:
                ...

            # self.current_file = myfile
            # self.current_filename = myfile.rpartition("/")[2]
            # self.current_folder = path.dirname(myfile)
            f.close()
            # self.headerbar.set_subtitle(myfile)
            # self.status_label.set_text(f"'{myfile}' loaded")
            # self.headerbar.set_title("TextEdit")
            self.grab_focus()
            # self.is_changed = False



    def _on_cursor_move(self, buf, cursor_iter, mark, user_data = None):
        if mark != buf.get_insert():
            return

        self.update_cursor_position()


    def update_cursor_position(self):
        iter  = self._buffer.get_iter_at_mark(self._buffer.get_insert())
        chars = iter.get_offset()
        row   = iter.get_line() + 1
        col   = self.get_visual_column(iter) + 1

        classes = self._buffer.get_context_classes_at_iter(iter)
        classes_str = ""

        i = 0
        for c in classes:
            if len(classes) != i + 1:
                classes_str += c + ", "
            else:
                classes_str += c

        cursor_data = f"char: {chars}, line: {row}, column: {col}, classes: {classes_str}"
        logger.debug(cursor_data)
        event_system.emit("set_line_char_label", (f"{row}:{col}",))


    # https://github.com/ptomato/inform7-ide/blob/main/src/actions.c
    def action_uncomment_selection(self):
        ...

    def action_comment_out_selection(self):
        pass
