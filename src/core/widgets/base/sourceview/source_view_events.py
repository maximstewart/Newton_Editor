# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports
from .mixins.source_view_dnd_mixin import SourceViewDnDMixin
from .mixins.source_file_events_mixin import FileEventsMixin
from .mixins.source_mark_events_mixin import MarkEventsMixin


class SourceViewEvents(SourceViewDnDMixin, MarkEventsMixin, FileEventsMixin):
    def _create_default_tag(self, buffer):
        general_style_tag = buffer.create_tag('general_style')
        general_style_tag.set_property('size', 100)
        general_style_tag.set_property('scale', 100)

    def _is_modified(self, *args):
        buffer    = self.get_buffer()
        file_type = self.get_filetype()

        if not self._loading_file:
            event_system.emit("buffer_changed", (buffer, ))
            # event_system.emit("textDocument/didChange", (file_type, buffer, ))
            # event_system.emit("textDocument/completion", (self, ))

        self.update_cursor_position(buffer)

    def _insert_text(self, buffer, location_itr, text_str, len_int):
        if self.freeze_multi_line_insert: return

        self.begin_user_action(buffer)
        with buffer.freeze_notify():
            GLib.idle_add(self._update_multi_line_markers, *(buffer, text_str,))

    def _buffer_modified_changed(self, buffer):
        tab_widget = self.get_parent().get_tab_widget()
        tab_widget.set_status(changed = True if buffer.get_modified() else False)


    def _button_press_event(self, widget = None, eve = None, user_data = None):
        if eve.type == Gdk.EventType.BUTTON_PRESS and eve.button == 1 :   # l-click
            if eve.state & Gdk.ModifierType.CONTROL_MASK:
                self.button_press_insert_mark(eve)
                return True
            else:
                self.keyboard_clear_marks()
        elif eve.type == Gdk.EventType.BUTTON_RELEASE and eve.button == 3: # r-click
            ...

    def _scroll_event(self, widget, eve):
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        x, y, z    = eve.get_scroll_deltas()
        if eve.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            buffer = self.get_buffer()
            if z > 0:
                self.scale_down_text(buffer)
            else:
                self.scale_up_text(buffer)

            return True

        if eve.state & accel_mask == Gdk.ModifierType.SHIFT_MASK:
            adjustment  = self.get_hadjustment()
            current_val = adjustment.get_value()
            step_val    = adjustment.get_step_increment()

            if z > 0: # NOTE: scroll left
                adjustment.set_value(current_val - step_val * 2)
            else:     # NOTE: scroll right
                adjustment.set_value(current_val + step_val * 2)

            return True

    def _focus_in_event(self, widget, eve = None):
        event_system.emit("set_active_src_view", (self,))
        self.get_parent().get_parent().is_editor_focused = True

    def _on_widget_focus(self, widget, eve = None):
        tab_view = self.get_parent().get_parent()
        path     = self._current_file if self._current_file else ""

        event_system.emit('focused_target_changed', (tab_view.NAME,))
        event_system.emit("set_path_label", (path,))
        event_system.emit("set_encoding_label")
        event_system.emit("set_file_type_label", (self._current_filetype,))

        return False

    def _on_cursor_move(self, buffer, cursor_iter, mark, user_data = None):
        if mark != buffer.get_insert(): return

        self.update_cursor_position(buffer)

        # NOTE: Not sure but this might not be efficient if the map reloads the same view...
        event_system.emit(f"set_source_view", (self,))