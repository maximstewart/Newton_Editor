# Python imports
import random

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class MarkEventsMixin:

    def keyboard_insert_mark(self, target_iter = None, is_keyboard_insert = True):
        if not target_iter:
            target_iter  = self._buffer.get_iter_at_mark( self._buffer.get_insert() )

        found_mark  = self.check_for_insert_marks(target_iter, is_keyboard_insert)
        if not found_mark:
            random_bits = random.getrandbits(128)
            hash = "%032x" % random_bits
            mark = Gtk.TextMark.new(name = f"multi_insert_{hash}", left_gravity = False)

            self._buffer.add_mark(mark, target_iter)
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
        marks = target_iter.get_marks()
        found_mark = False
        for mark in marks:
            for _mark in self._multi_insert_marks:
                if _mark == mark:
                    mark.set_visible(False)
                    self._buffer.delete_mark(mark)
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
        self._buffer.begin_user_action()

        for mark in self._multi_insert_marks:
            mark.set_visible(False)
            self._buffer.delete_mark(mark)

        self._multi_insert_marks.clear()
        self._buffer.end_user_action()


    def _update_multi_line_markers(self, text_str):
        for mark in self._multi_insert_marks:
            iter = self._buffer.get_iter_at_mark(mark)
            self._buffer.insert(iter, text_str, -1)

        self.end_user_action()

    def _delete_on_multi_line_markers(self):
        iter = self._buffer.get_iter_at_mark( self._buffer.get_insert() )
        self._buffer.backspace(iter, interactive = True, default_editable = True)

        for mark in self._multi_insert_marks:
            iter = self._buffer.get_iter_at_mark(mark)
            self._buffer.backspace(iter, interactive = True, default_editable = True)

        self.end_user_action()

    def begin_user_action(self):
        if len(self._multi_insert_marks) > 0:
            self._buffer.begin_user_action()
            self.freeze_multi_line_insert = True

    def end_user_action(self):
        if len(self._multi_insert_marks) > 0:
            self._buffer.end_user_action()
            self.freeze_multi_line_insert = False
