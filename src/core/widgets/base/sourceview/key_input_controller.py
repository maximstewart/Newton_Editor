# Python imports

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from gi.repository import GLib

# Application imports



class KeyInputController:

    # NOTE: Mostly sinking pre-bound keys here to let our keybinder control instead...
    def _key_press_event(self, widget, eve):
        keyname    = Gdk.keyval_name(eve.keyval)
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False
        buffer     = self.get_buffer()

        try:
            is_alt = True if modifiers & Gdk.ModifierType.ALT_MASK else False
        except Exception:
            is_alt = True if modifiers & Gdk.ModifierType.MOD1_MASK else False

        if is_control:
            if is_shift:
                if keyname in [ "Up", "Down" ]:
                    return True

            if keyname in [ "slash", "Up", "Down", "m", "z", "y" ]:
                return True

        if is_alt:
            if keyname in [ "Up", "Down", "Left", "Right" ]:
                return True


        if len(self._multi_insert_marks) > 0:
            if keyname == "BackSpace":
                self.begin_user_action(buffer)

                with buffer.freeze_notify():
                    GLib.idle_add(self._delete_on_multi_line_markers, *(buffer,))

                self.end_user_action(buffer)

            return True

        # NOTE: if a plugin recieves the call and handles, it will be the final decider for propigation
        return event_system.emit_and_await("autopairs", (keyname, is_control, is_alt, is_shift))



    def _key_release_event(self, widget, eve):
        if self.freeze_multi_line_insert: return

        keyname    = Gdk.keyval_name(eve.keyval)
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False
        buffer     = self.get_buffer()

        try:
            is_alt = True if modifiers & Gdk.ModifierType.ALT_MASK else False
        except Exception:
            is_alt = True if modifiers & Gdk.ModifierType.MOD1_MASK else False

        can_continue = self.can_proceed(keyname, is_control, is_shift, is_alt)
        if not can_continue:
            return can_continue


        if is_control:
            if is_shift:
                if keyname in ["S"]:
                    if keyname == "S":
                        self.save_file_as()

                    return True

            if keyname in ["z", "y", "m", "s", "h", "equal", "minus", "Up", "Down"]:
                if keyname == "z":
                    self.keyboard_undo()
                if keyname == "y":
                    self.keyboard_redo()
                if keyname == "m":
                    self.keyboard_insert_mark()
                if keyname == "s":
                    self.save_file()
                if keyname == "h":
                    self.toggle_highlight_line()

                if keyname == "equal":
                    self.scale_up_text()
                if keyname == "minus":
                    self.scale_down_text()

                if keyname == "Up":
                    self.keyboard_move_lines_up()
                if keyname == "Down":
                    self.keyboard_move_lines_down()

                return True

            # Note: Sink these requets
            if keyname in ["Slash"]:
                return True

        if is_alt:
            if keyname == "m":
                self.keyboard_clear_marks()


        if keyname in {"Return", "Enter"}:
            if len(self._multi_insert_marks) > 0:
                self.begin_user_action(buffer)
                with buffer.freeze_notify():
                    GLib.idle_add(self._new_line_on_multi_line_markers, *(buffer,))

                return

            has_selection = buffer.get_has_selection()
            if not has_selection:
                return self.insert_indent_handler(buffer)


    def can_proceed(self, keyname, is_control, is_shift, is_alt):
        if is_control:
            if is_shift:
                if keyname in ["Up", "Down"]:
                    return False

            if keyname in ["w", "t", "o"]:
                return False

        if is_alt:
            if keyname in ["Up", "Down", "Left", "Right"]:
                return False

        return True