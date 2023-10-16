# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from plugins.plugin_base import PluginBase
from .color_converter_mixin import ColorConverterMixin



class Plugin(ColorConverterMixin, PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Colorize"    # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                #       where self.name should not be needed for message comms
        self.tag_stub_name      = "colorize_tag"

    def run(self):
        ...

    def generate_reference_ui_element(self):
        ...

    def subscribe_to_events(self):
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)
        self._event_system.subscribe("buffer_changed_first_load", self._buffer_changed_first_load)
        self._event_system.subscribe("buffer_changed", self._buffer_changed)


    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view

    def _buffer_changed_first_load(self, buffer):
        self._do_colorize(buffer)


    def _buffer_changed(self, buffer):
        tag_table = buffer.get_tag_table()
        mark      = buffer.get_insert()
        iter      = buffer.get_iter_at_mark(mark)
        tags      = iter.get_tags()

        iter.forward_line()  # NOTE: Jump to start of next line
        end   = iter.copy()
        iter.backward_line() # NOTE: To now easily get start of prior line
        start = iter.copy()

        for tag in tags:
            if tag.props.name and self.tag_stub_name in tag.props.name:
                buffer.remove_tag(tag, start, end)
                tag_table.remove(tag)

        self._do_colorize(buffer, start, end)


    def _do_colorize(self, buffer = None, start_itr = None, end_itr = None):
        # rgb(a), hsl, hsv
        results = self.finalize_non_hex_matches( self.collect_preliminary_results(buffer, start_itr, end_itr) )
        self.process_results(buffer, results)

        # hex color search
        results = self.finalize_hex_matches( self.collect_preliminary_hex_results(buffer, start_itr, end_itr) )
        self.process_results(buffer, results)


    def collect_preliminary_results(self, buffer = None, start_itr = None, end_itr = None):
        if not buffer: return []

        if not start_itr:
            start_itr = buffer.get_start_iter()

        results1  = self.search(start_itr, end_itr, "rgb")
        results2  = self.search(start_itr, end_itr, "hsl")
        results3  = self.search(start_itr, end_itr, "hsv")

        return results1 + results2 + results3

    def collect_preliminary_hex_results(self, buffer = None, start_itr = None, end_itr = None):
        if not buffer: return []

        if not start_itr:
            start_itr = buffer.get_start_iter()

        results1  = self.search(start_itr, end_itr, "#")

        return results1

    def search(self, start_itr = None, end_itr = None, query = None):
        if not start_itr or not query: return None, None

        results = []
        flags   = Gtk.TextSearchFlags.VISIBLE_ONLY | Gtk.TextSearchFlags.TEXT_ONLY
        while True:
            result = start_itr.forward_search(query, flags, end_itr)
            if not result: break

            results.append(result)
            start_itr = result[1]

        return results

    def finalize_non_hex_matches(self, result_hits: [] = []):
        results = []

        for start, end in result_hits:
            if end.get_char() == "a":
                end.forward_char()

            if end.get_char() != "(":
                continue

            end.forward_chars(21)
            if end.get_char() == ")":
                end.forward_char()
                results.append([start, end])
                continue

            while end.get_char() != "(":
                if end.get_char() == ")":
                    end.forward_char()
                    results.append([start, end])
                    break

                end.forward_chars(-1)

        return results

    def finalize_hex_matches(self, result_hits: [] = []):
        results = []

        for start, end in result_hits:
            while not end.get_char() in [";", " "]:
                end.forward_char()

            results.append([start, end])

        return results

    def process_results(self, buffer, results):
        # NOTE: HSV and HSL parsing are available in Gtk 4.0. Not lower...
        for start, end in results:
            text  = self.get_color_text(buffer, start, end)
            color = Gdk.RGBA()
            if color.parse(text):
                tag = self.get_colorized_tag(buffer, text, color)
                buffer.apply_tag(tag, start, end)

    def get_colorized_tag(self, buffer, tag, color: Gdk.RGBA):
        tag_table    = buffer.get_tag_table()
        colorize_tag = f"{self.tag_stub_name}_{tag}"
        search_tag   = tag_table.lookup(colorize_tag)
        if not search_tag:
            search_tag = buffer.create_tag(colorize_tag, background_rgba = color)

        return search_tag
