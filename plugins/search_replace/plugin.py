# Python imports
import os

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

        self._search_replace_dialog  = None
        self._find_entry             = None
        self._replace_entry          = None
        self._active_src_view        = None

        self.use_regex               = False
        self.use_case_sensitive      = False
        self.use_selection_only_scan = False
        self.use_fuzzy_search        = False
        self.highlight_color         = "#FBF719"
        self.text_color              = "#000000"


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
        self.search_for_string(self._find_entry)

    def _show_search_replace(self, widget = None, eve = None):
        self._search_replace_dialog.popup()

    def _tggl_search_replace(self, widget = None, eve = None):
        is_visible = self._search_replace_dialog.is_visible()
        if not is_visible:
            self._search_replace_dialog.popup();
            self._find_entry.grab_focus()
        else:
            self._search_replace_dialog.popdown()

    def tggle_regex(self, widget):
        self.use_regex = not widget.get_active()
        self._set_find_options_lbl()

    def tggle_case_sensitive(self, widget):
        self.use_case_sensitive = not widget.get_active()
        self._set_find_options_lbl()

    def tggle_selection_only_scan(self, widget):
        self.use_selection_only_scan = not widget.get_active()
        self._set_find_options_lbl()

    def tggle_fuzzy_search(self, widget):
        self.use_fuzzy_search =  not widget.get_active()
        self._set_find_options_lbl()

    def _set_find_options_lbl(self):
        # Finding with Options: Case Insensitive
        # Finding with Options: Regex, Case Sensitive, Within Current Selection, Whole Word
        # Finding with Options: Regex, Case Inensitive, Within Current Selection, Whole Word
        # f"Finding with Options: {regex}, {case}, {selection}, {word}"
        ...

    def _update_status_lbl(self, total_count: int = None, query: str = None):
        if not total_count or not query: return

        count  = total_count if total_count > 0 else "No"
        plural = "s" if total_count > 1 else ""
        self._find_status_lbl.set_label(f"{count} results{plural} found for '{query}'")

    def get_search_tag(self, buffer):
        tag_table  = buffer.get_tag_table()
        search_tag = tag_table.lookup("search_tag")
        if not search_tag:
            search_tag = buffer.create_tag("search_tag", background = self.highlight_color, foreground = self.text_color)

        buffer.remove_tag_by_name("search_tag", buffer.get_start_iter(), buffer.get_end_iter())
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
        for start, end in results:
            buffer.apply_tag(search_tag, start, end)
        self._update_status_lbl(total_count, query)

    def search(self, start_itr = None, query = None):
        if not start_itr or not query: return None, None

        if not self.use_case_sensitive:
            _flags = Gtk.TextSearchFlags.VISIBLE_ONLY & Gtk.TextSearchFlags.TEXT_ONLY & Gtk.TextSearchFlags.CASE_INSENSITIVE
        else:
            _flags = Gtk.TextSearchFlags.VISIBLE_ONLY & Gtk.TextSearchFlags.TEXT_ONLY

        results = []
        while True:
            result = start_itr.forward_search(query, flags = _flags, limit = None)
            if not result: break

            results.append(result)
            start_itr = result[1]

        return results, len(results)







    def find_next(self):
        ...

    def find_all(self):
        ...

    def replace_next(self):
        ...

    def replace_all(self):
        ...
