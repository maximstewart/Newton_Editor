# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from plugins.plugin_base import PluginBase
from .codecomment_tags import CodeCommentTags
from .remove_comment_mixin import RemoveCommentMixin
from .add_comment_mixin import AddCommentMixin



class Plugin(AddCommentMixin, RemoveCommentMixin, CodeCommentTags, PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Commentzar"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                #       where self.name should not be needed for message comms


    def generate_reference_ui_element(self):
        ...

    def run(self):
        ...

    def subscribe_to_events(self):
        self._event_system.subscribe("keyboard_tggl_comment", self._keyboard_tggl_comment)
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)

    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = self._active_src_view.get_buffer()
        self._tag_table       = self._buffer.get_tag_table()


    def _keyboard_tggl_comment(self):
        buffer = self._buffer
        lang   = buffer.get_language()
        if lang is None:
            return

        (start_tag, end_tag) = self.get_comment_tags(lang)
        if not start_tag and not end_tag:
            return

        sel = buffer.get_selection_bounds()
        currentPosMark = buffer.get_insert()
        oldPos = 0

        # if user selected chars or multilines
        if sel != ():
            deselect = False
            (start, end) = sel
            if not start.starts_line():
                start.set_line_offset(0)
            if not end.ends_line():
                end.forward_to_line_end()
        else:
            deselect = True
            start    = buffer.get_iter_at_mark(currentPosMark)
            oldPos   = buffer.get_iter_at_mark(currentPosMark).get_offset()
            start.set_line_offset(0)
            end = start.copy()

            if not end.ends_line():
                end.forward_to_line_end()

        if start.get_offset() == end.get_offset():
            buffer.begin_user_action()
            buffer.insert(start, start_tag)
            buffer.insert(start, " ")
            buffer.end_user_action()
            return

        new_code = self.add_comment_characters(buffer, start_tag, end_tag, start, end, deselect, oldPos)


    def discard_white_spaces(self, iter):
        count = 0
        while not iter.ends_line():
            c = iter.get_char()
            if not c in (" ", "\t"):
                return (iter, count)

            iter.forward_char()
            count += 1

        return (iter, 0)

    def is_commented(self, comment_pos_iter, start_tag):
        head_iter = comment_pos_iter.copy()
        self.forward_tag(head_iter, start_tag)
        s = comment_pos_iter.get_slice(head_iter)
        if s == start_tag:
            return True

        return False

    def forward_tag(self, iter, tag):
        iter.forward_chars(len(tag))

    def backward_tag(self, iter, tag):
        iter.backward_chars(len(tag))

    def get_tag_position_in_line(self, tag, head_iter, iter):
        while not iter.ends_line():
            s = iter.get_slice(head_iter)
            if s == tag:
                return True
            else:
                head_iter.forward_char()
                iter.forward_char()
        return False
