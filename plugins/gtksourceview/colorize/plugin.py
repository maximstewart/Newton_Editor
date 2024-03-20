# Python imports
import random

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
        self._buffer = None


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
        self._buffer = buffer
        self._do_colorize(buffer)

    def _buffer_changed(self, buffer):
        self._event_system.emit("pause_event_processing")
        self._handle_colorize(buffer)
        self._event_system.emit("resume_event_processing")

    def _handle_colorize(self, buffer):
        self._buffer = buffer
        tag_table    = buffer.get_tag_table()
        mark         = buffer.get_insert()
        start        = None
        end          = buffer.get_iter_at_mark(mark)

        i            = 0
        walker_iter  = end.copy()
        working_tag  = self.find_working_tag(walker_iter, i)
        if working_tag:
            start = self.find_start_range(walker_iter, working_tag)

            self.find_end_range(end, working_tag)
            buffer.remove_tag(working_tag, start, end)
        else:
            start = self.traverse_backward_25_or_less(walker_iter)
            self.traverse_forward_25_or_less(end)

        self._do_colorize(buffer, start, end)



    def find_working_tag(self, walker_iter, i):
        tags = walker_iter.get_tags()
        for tag in tags:
            if tag.props.name and self.tag_stub_name in tag.props.name:
                return tag

        res = walker_iter.backward_char()

        if not res: return
        if i > 25: return
        return self.find_working_tag(walker_iter, i + 1)

    def find_start_range(self, walker_iter, working_tag):
        tags = walker_iter.get_tags()
        for tag in tags:
            if tag.props.name and working_tag.props.name in tag.props.name:
                res = walker_iter.backward_char()
                if res:
                    self.find_start_range(walker_iter, working_tag)

        return walker_iter

    def find_end_range(self, end, working_tag):
        tags = end.get_tags()
        for tag in tags:
            if tag.props.name and working_tag.props.name in tag.props.name:
                res = end.forward_char()
                if res:
                    self.find_end_range(end, working_tag)

    def traverse_backward_25_or_less(self, walker_iter):
        i = 1
        while i <= 25:
            res = walker_iter.backward_char()
            if not res: break
            i += 1

    def traverse_forward_25_or_less(self, end):
        i = 1
        while i <= 25:
            res = end.forward_char()
            if not res: break
            i += 1

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
            i   = 0
            _ch = end.get_char()
            ch  = ord(end.get_char()) if _ch else -1

            while ((ch >= 48 and ch <= 57) or (ch >= 65 and ch <= 70) or (ch >= 97 and ch <= 102)):
                if i > 16: break

                i += 1
                end.forward_char()
                _ch = end.get_char()
                ch  = ord(end.get_char()) if _ch else -1

            if i in [3, 4, 6, 8, 9, 12, 16]:
                results.append([start, end])

        return results

    def process_results(self, buffer, results):
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
