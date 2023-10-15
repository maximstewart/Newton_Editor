# Python imports
import os
import re

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase




class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Search/Replace"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                    #       where self.name should not be needed for message comms
        self.path               = os.path.dirname(os.path.realpath(__file__))
        self._GLADE_FILE        = f"{self.path}/search_replace.glade"

        self._search_replace_dialog   = None
        self._find_entry              = None
        self._replace_entry           = None
        self._active_src_view         = None
        self._buffer                  = None
        self._tag_table               = None

        self.use_regex                = False
        self.use_case_sensitive       = False
        self.search_only_in_selection = False
        self.use_whole_word_search    = False

        self.search_tag               = "search_tag"
        self.highlight_color          = "#FBF719"
        self.text_color               = "#000000"
        self.alpha_num_under          = re.compile(r"[a-zA-Z0-9_]")


    def run(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(self._GLADE_FILE)
        self._connect_builder_signals(self, self._builder)

        separator_botton            = self._ui_objects[0]
        self._search_replace_dialog = self._builder.get_object("search_replace_dialog")
        self._find_status_lbl       = self._builder.get_object("find_status_lbl")
        self._find_options_lbl      = self._builder.get_object("find_options_lbl")

        self._find_entry            = self._builder.get_object("find_entry")
        self._replace_entry         = self._builder.get_object("replace_entry")

        self._search_replace_dialog.set_relative_to(separator_botton)
        self._search_replace_dialog.set_hexpand(True)

    def generate_reference_ui_element(self):
        ...

    def subscribe_to_events(self):
        self._event_system.subscribe("tggl_search_replace", self._tggl_search_replace)
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)

    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = self._active_src_view.get_buffer()
        self._tag_table       = self._buffer.get_tag_table()
        self.search_for_string(self._find_entry)

    def _show_search_replace(self, widget = None, eve = None):
        self._search_replace_dialog.popup()

    def _tggl_search_replace(self, widget = None, eve = None):
        is_visible = self._search_replace_dialog.is_visible()
        buffer     = self._active_src_view.get_buffer()
        data       = None

        if buffer.get_has_selection():
            start, end = buffer.get_selection_bounds()
            data       = buffer.get_text(start, end, include_hidden_chars = False)

        if data:
            self._find_entry.set_text(data)

        if not is_visible:
            self._search_replace_dialog.popup();
            self._find_entry.grab_focus()
        elif not data and is_visible:
            self._search_replace_dialog.popdown()
            self._find_entry.set_text("")

    def tggle_regex(self, widget):
        self.use_regex = not widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def tggle_case_sensitive(self, widget):
        self.use_case_sensitive = widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def tggle_selection_only_scan(self, widget):
        self.search_only_in_selection = widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def tggle_whole_word_search(self, widget):
        self.use_whole_word_search = widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def _set_find_options_lbl(self):
        # Finding with Options: Case Insensitive
        # Finding with Options: Regex, Case Sensitive, Within Current Selection, Whole Word
        # Finding with Options: Regex, Case Inensitive, Within Current Selection, Whole Word
        # f"Finding with Options: {regex}, {case}, {selection}, {word}"
        ...

    def _update_status_lbl(self, total_count: int = 0, query: str = None):
        if not query: return

        count  = total_count if total_count > 0 else "No"
        plural = "s" if total_count > 1 else ""
        self._find_status_lbl.set_label(f"{count} results{plural} found for '{query}'")

    def get_search_tag(self, buffer):
        tag_table  = buffer.get_tag_table()
        search_tag = tag_table.lookup(self.search_tag)
        if not search_tag:
            search_tag = buffer.create_tag(self.search_tag, background = self.highlight_color, foreground = self.text_color)

        buffer.remove_tag_by_name(self.search_tag, buffer.get_start_iter(), buffer.get_end_iter())
        return search_tag

    def search_for_string(self, widget):
        query      = widget.get_text()
        buffer     = self._active_src_view.get_buffer()
        # Also clears tag from buffer so if no query we're clean in ui
        search_tag = self.get_search_tag(buffer)

        if not query:
            self._find_status_lbl.set_label(f"Find in current buffer")
            return

        start_itr  = buffer.get_start_iter()
        end_itr    = buffer.get_end_iter()

        results, total_count = self.search(start_itr, query)
        self._update_status_lbl(total_count, query)
        for start, end in results:
            buffer.apply_tag(search_tag, start, end)

    def search(self, start_itr = None, query = None, limit = None):
        if not start_itr or not query: return None, None

        flags = Gtk.TextSearchFlags.VISIBLE_ONLY | Gtk.TextSearchFlags.TEXT_ONLY
        if not self.use_case_sensitive:
            flags = flags | Gtk.TextSearchFlags.CASE_INSENSITIVE

        if self.search_only_in_selection and self._buffer.get_has_selection():
            start_itr, limit = self._buffer.get_selection_bounds()

        _results = []
        while True:
            result = start_itr.forward_search(query, flags, limit)
            if not result: break

            _results.append(result)
            start_itr = result[1]

        results = self.apply_filters(_results, query)
        return results, len(results)

    def apply_filters(self, _results, query):
        results = []
        for start, end in _results:
            text = self._buffer.get_slice(start, end, include_hidden_chars = False)
            if self.use_whole_word_search:
                end.forward_char()
                start.backward_char()

                match = self.alpha_num_under.match( start.get_char() )
                if not match is None:
                    continue

                match = self.alpha_num_under.match( end.get_char() )
                if not match is None:
                    continue

                end.backward_char()
                start.forward_char()

            results.append([start, end])

        return results

    def find_next(self, widget, eve = None, use_data = None):
        mark = self._buffer.get_insert()
        iter = self._buffer.get_iter_at_mark(mark)
        iter.forward_line()

        search_tag     = self._tag_table.lookup(self.search_tag)
        next_tag_found = iter.forward_to_tag_toggle(search_tag)
        if not next_tag_found:
            self._buffer.place_cursor( self._buffer.get_start_iter() )
            mark = self._buffer.get_insert()
            iter = self._buffer.get_iter_at_mark(mark)
            iter.forward_to_tag_toggle(search_tag)

        self._buffer.place_cursor(iter)
        self._active_src_view.scroll_to_mark( self._buffer.get_insert(), 0.0, True, 0.0, 0.0 )


    def find_all(self, widget):
        ...

    def replace(self, widget):
        ...

    def replace_all(self, widget):
        ...