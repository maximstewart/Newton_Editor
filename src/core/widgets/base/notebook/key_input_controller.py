# Python imports

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

# Application imports



class KeyInputController:
    def _key_press_event(self, widget, eve):
        keyname    = Gdk.keyval_name(eve.keyval)
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False

        try:
            is_alt = True if modifiers & Gdk.ModifierType.ALT_MASK else False
        except Exception:
            is_alt = True if modifiers & Gdk.ModifierType.MOD1_MASK else False


    def _key_release_event(self, widget, eve):
        keyname    = Gdk.keyval_name(eve.keyval)
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False

        try:
            is_alt = True if modifiers & Gdk.ModifierType.ALT_MASK else False
        except Exception:
            is_alt = True if modifiers & Gdk.ModifierType.MOD1_MASK else False

        page_num, container, source_view = self.get_active_view()
        if is_control:
            if is_shift:
                if keyname in ["Up", "Down"]:
                    if keyname == "Up":
                        self.keyboard_move_tab_to_1(page_num)
                    if keyname == "Down":
                        self.keyboard_move_tab_to_2(page_num)

                return True

            if keyname in ["w", "t", "o"]:
                if keyname == "w":
                    self.close_tab(None, container, source_view)
                if keyname == "t":
                    self._create_view()
                if keyname == "o":
                    page_num, container, source_view = self.get_active_view()
                    file    = source_view.get_current_file()
                    _gfiles = event_system.emit_and_await("open_files", (source_view, None, file if file else None))

                    event_system.emit("keyboard_open_file", (_gfiles,))

                return True

        if is_alt:
            if keyname in ["Up", "Down", "Left", "Right"]:
                if keyname == "Up":
                    self.keyboard_prev_tab(page_num)
                if keyname == "Down":
                    self.keyboard_next_tab(page_num)
                if keyname == "Left":
                    self.keyboard_move_tab_left(page_num)
                if keyname == "Right":
                    self.keyboard_move_tab_right(page_num)

                return True