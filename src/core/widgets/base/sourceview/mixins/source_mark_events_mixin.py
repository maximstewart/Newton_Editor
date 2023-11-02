# Python imports
import random

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class MarkEventsMixin:

    def keyboard_insert_mark(self, target_iter = None, is_keyboard_insert = True):
        buffer = self.get_buffer()

        if not target_iter:
            target_iter  = buffer.get_iter_at_mark( buffer.get_insert() )

        found_mark  = self.check_for_insert_marks(target_iter, is_keyboard_insert)
        if not found_mark:
            random_bits = random.getrandbits(128)
            hash = "%032x" % random_bits
            mark = Gtk.TextMark.new(name = f"multi_insert_{hash}", left_gravity = False)

            buffer.add_mark(mark, target_iter)
            self._multi_insert_marks.append(mark)
            mark.set_visible(True)

    def button_press_insert_mark(self, eve):
        data = self.window_to_buffer_coords(Gtk.TextWindowType.TEXT , eve.x, eve.y)
        is_over_text, target_iter, is_trailing = self.get_iter_at_position(data.buffer_x, data.buffer_y)

        if not is_over_text:
            # NOTE: Trying to put at very end of line if not over text (aka, clicking right of text)
            target_iter.forward_visible_line()
            target_iter.backward_char()

        self.keyboard_insert_mark(target_iter, is_keyboard_insert = False)

    def check_for_insert_marks(self, target_iter, is_keyboard_insert):
        marks      = target_iter.get_marks()
        buffer     = self.get_buffer()
        found_mark = False

        for mark in marks:
            for _mark in self._multi_insert_marks:
                if _mark == mark:
                    mark.set_visible(False)
                    buffer.delete_mark(mark)
                    found_mark = True
                    break

            if found_mark:
                self._multi_insert_marks.remove(mark)
                break

        if not is_keyboard_insert:
            for mark in marks:
                if "insert" in mark.get_name():
                    found_mark = True

        return found_mark

    def keyboard_clear_marks(self):
        buffer = self.get_buffer()

        buffer.begin_user_action()

        for mark in self._multi_insert_marks:
            mark.set_visible(False)
            buffer.delete_mark(mark)

        self._multi_insert_marks.clear()
        buffer.end_user_action()


    def _update_multi_line_markers(self, buffer, text_str):
        for mark in self._multi_insert_marks:
            iter = buffer.get_iter_at_mark(mark)
            buffer.insert(iter, text_str, -1)

        self.end_user_action(buffer)

    def _delete_on_multi_line_markers(self, buffer):
        iter = buffer.get_iter_at_mark( buffer.get_insert() )
        buffer.backspace(iter, interactive = True, default_editable = True)

        for mark in self._multi_insert_marks:
            iter = buffer.get_iter_at_mark(mark)
            buffer.backspace(iter, interactive = True, default_editable = True)

        self.end_user_action(buffer)
    
    def _new_line_on_multi_line_markers(self, buffer):
        iter = buffer.get_iter_at_mark( buffer.get_insert() )
        self._base_indent(buffer, iter)
        self.insert_indent_handler(buffer, iter)

        for mark in self._multi_insert_marks:
            iter = buffer.get_iter_at_mark(mark)
            self._base_indent(buffer, iter)
            self.insert_indent_handler(buffer, iter)

    def insert_indent_handler(self, buffer, iter = None):
        if not iter:
            iter   = buffer.get_iter_at_mark( buffer.get_insert() )

        iter_copy  = iter.copy()
        iter_copy.backward_sentence_start()
        iter_copy.forward_sentence_end()
        iter_copy.backward_char()

        # Note: Need to compare line nums too because  backward_sentence_start
        #     and forward_sentence_end can go farther back if just spaces inbetween...
        line_start   = iter.get_line()
        line_end  = iter_copy.get_line()

        _char = iter_copy.get_char()
        if _char in ["{", ":"] and (line_start - line_end) == 1:
            self._indent_deeper(buffer, iter)
    
    def _base_indent(self, buffer, iter):
        line_num  = iter.get_line()
        iter_copy = buffer.get_iter_at_line(line_num)

        spaces = ""
        _char  = iter_copy.get_char()
        while _char == " ":
            spaces += " "
            iter_copy.forward_char()
            _char = iter_copy.get_char()

        buffer.insert(iter, f"\n{spaces}")


    def _indent_deeper(self, buffer, iter):
        buffer.insert(iter, "    ")



    def begin_user_action(self, buffer):
        if len(self._multi_insert_marks) > 0:
            buffer.begin_user_action()
            self.freeze_multi_line_insert = True

    def end_user_action(self, buffer):
        if len(self._multi_insert_marks) > 0:
            buffer.end_user_action()
            self.freeze_multi_line_insert = False