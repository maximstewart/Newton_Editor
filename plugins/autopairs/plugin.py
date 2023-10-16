# Python imports
import os
import threading
import subprocess
import time

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase




# NOTE: Threads WILL NOT die with parent's destruction.
def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=False).start()
    return wrapper

# NOTE: Threads WILL die with parent's destruction.
def daemon_threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return wrapper




class Plugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Autopairs"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                               #       where self.name should not be needed for message comms

        self.chars = {
            "quotedbl": "\"",
            "apostrophe": "'",
            "parenleft": "(",
            "bracketleft": "[",
            "braceleft": "{",
            "less": "<",
            "grave": "`",
        }

        self.close = {
            "\"": "\"",
            "'": "'",
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
            "`": "`",
        }

    def generate_reference_ui_element(self):
        ...

    def run(self):
        ...

    def subscribe_to_events(self):
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)
        self._event_system.subscribe("autopairs", self._autopairs)

    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = self._active_src_view.get_buffer()
        self._tag_table       = self._buffer.get_tag_table()

    def _buffer_changed_first_load(self, buffer):
        self._do_colorize(buffer)


    def _buffer_changed(self, buffer):
        tag_table = buffer.get_tag_table()
        mark      = buffer.get_insert()
        iter      = buffer.get_iter_at_mark(mark)
        tags      = iter.get_tags()

    def _autopairs(self, keyval_name, ctrl, alt, shift):
        if keyval_name in self.chars:
            return self.text_insert(self._buffer, keyval_name)
        elif ctrl and keyval_name == "Return":
            self.move_to_next_line(self._buffer)

    # NOTE: All of below to EOF, lovingly taken from Hamad Al Marri's Gamma
    #       text editor. I did do some cleanup of comments but otherwise pretty
    #       much the same code just fitted to my plugin architecture.
    # Link: https://gitlab.com/hamadmarri/gamma-text-editor
    def move_to_next_line(self, buffer):
        selection = buffer.get_selection_bounds()
        if selection != (): return False

        position = buffer.get_iter_at_mark(buffer.get_insert())

        if position.ends_line(): return False

        position.forward_to_line_end()
        buffer.place_cursor(position)

        return False

    def text_insert(self, buffer, text):
        selection = buffer.get_selection_bounds()
        if selection == ():
            return self.add_close(buffer, text, )
        else:
            return self.add_enclose(buffer, text, selection)

    def add_close(self, buffer, text):
        text = self.chars[text]
        text += self.close[text]

        position = buffer.get_iter_at_mark(buffer.get_insert())

        c = position.get_char()
        if not c in (" ", "", ";", ":", "\t", ",", ".", "\n", "\r") \
            and not c in list(self.close.values()):
            return False

        buffer.insert(position, text)

        position = buffer.get_iter_at_mark(buffer.get_insert())
        position.backward_char()
        buffer.place_cursor(position)

        return True

    def add_enclose(self, buffer, text, selection):
        (start, end) = selection
        selected = buffer.get_text(start, end, False)
        if len(selected) <= 3 and selected in ("<", ">", ">>>"
                                                "<<", ">>",
                                                "\"", "'", "`",
                                                "(", ")",
                                                "[", "]",
                                                "{", "}",
                                                "=", "==",
                                                "!=", "==="):
            return False

        start_mark = buffer.create_mark("startclose", start, False)
        end_mark = buffer.create_mark("endclose", end, False)

        buffer.begin_user_action()

        t = self.chars[text]
        buffer.insert(start, t)
        end = buffer.get_iter_at_mark(end_mark)
        t = self.close[t]
        buffer.insert(end, t)

        start = buffer.get_iter_at_mark(start_mark)
        end   = buffer.get_iter_at_mark(end_mark)
        end.backward_char()
        buffer.select_range(start, end)

        buffer.end_user_action()

        return True
