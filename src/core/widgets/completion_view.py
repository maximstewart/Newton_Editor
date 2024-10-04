# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

# Application imports
from .completion_item import CompletionItem



class CompletionView(Gtk.ScrolledWindow):
    def __init__(self):
        super(CompletionView, self).__init__()

        self.vadjustment = self.get_vadjustment()
        self.button_box  = None

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("completion-view")
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_size_request(320, -1)
        self.set_min_content_height(120)
        self.set_max_content_height(480)

        self.set_overlay_scrolling(False)
        self.set_policy( Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC )  # hbar, vbar

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        viewport        = Gtk.Viewport()
        self.button_box = Gtk.ListBox()

        self.button_box.set_hexpand( True )
        self.button_box.set_placeholder( Gtk.Label(label = "No completion data...") )
        self.button_box.set_selection_mode( Gtk.SelectionMode.BROWSE )

        self.button_box.connect("key-release-event", self._key_release_event)
        self.button_box.connect("button-release-event", self._button_release_event)

        viewport.add(self.button_box)
        self.add(viewport)

    def _key_release_event(self, widget, eve):
        keyname    = Gdk.keyval_name(eve.keyval)
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False

        if is_control:
            return True

        if keyname in [ "Enter", "Return" ]:
            self.activate_completion()
            return True

    def _button_release_event(self, widget, eve):
        if eve.button == 1: # lclick
            self.activate_completion()
            return True

    def clear_items(self):
        for child in self.button_box.get_children():
            self.button_box.remove(child)

    def add_completion_item(self, item: CompletionItem):
        self.button_box.add(item)

    def move_selection_up(self):
        srow  = self.button_box.get_selected_row()
        if not srow:
            self.select_last_row()
            return

        index = srow.get_index() - 1
        if index == -1:
            self.select_last_row()
            return

        row = self.button_box.get_row_at_index(index)
        self.select_and_scroll_to_view(row, self.vadjustment.get_value() - row.get_allocation().height)

    def move_selection_down(self):
        srow  = self.button_box.get_selected_row()
        if not srow:
            self.select_first_row()
            return

        index = srow.get_index() + 1
        if index > (len( self.button_box.get_children() ) - 1):
            index = 0
            self.select_first_row()
            return

        row = self.button_box.get_row_at_index(index)
        self.select_and_scroll_to_view(row, self.vadjustment.get_value() + row.get_allocation().height)

    def select_first_row(self):
        row = self.button_box.get_row_at_index(0)
        if not row: return
        self.select_and_scroll_to_view(row, self.vadjustment.get_lower())

    def select_last_row(self):
        row = self.button_box.get_row_at_index( len( self.button_box.get_children() ) - 1 )
        if not row: return
        self.select_and_scroll_to_view(row, self.vadjustment.get_upper())

    def select_and_scroll_to_view(self, row, adjustment: float):
        self.button_box.select_row(row)
        self.vadjustment.set_value( adjustment )

    def activate_completion(self):
        completion_item = self.button_box.get_selected_row().get_child()
        source_view     = self.get_parent()
        buffer          = source_view.get_buffer()
        siter           = buffer.get_iter_at_mark( buffer.get_insert() )
        pre_char        = self.get_pre_char(siter)

        if completion_item.textEdit:
            self.process_range_insert(buffer, completion_item.textEdit, completion_item.newText)

            for edit in completion_item.additionalTextEdits:
                self.process_range_insert(buffer, edit, edit["newText"])

            source_view.remove(self)
            GLib.idle_add( source_view.grab_focus )

            return

        if pre_char == '.':
            buffer.insert(siter, completion_item.insertText, -1)

            source_view.remove(self)
            GLib.idle_add( source_view.grab_focus )

            return

        if siter.inside_word() or siter.ends_word() or pre_char == '_':
            eiter = siter.copy()
            siter.backward_visible_word_start()
            self.get_word_start(siter)

            if not eiter.ends_word() and not pre_char == '_':
                eiter.forward_word_end()

            buffer.delete(siter, eiter)

        buffer.insert(siter, completion_item.insertText, -1)

        source_view.remove(self)
        GLib.idle_add( source_view.grab_focus )

    def process_range_insert(self, buffer, insert_data: {}, text: str):
        sline = insert_data["range"]["start"]["line"]
        schar = insert_data["range"]["start"]["character"]
        eline = insert_data["range"]["end"]["line"]
        echar = insert_data["range"]["end"]["character"]
        siter = buffer.get_iter_at_line_offset( sline, schar )
        eiter = buffer.get_iter_at_line_offset( eline, echar )

        buffer.delete(siter, eiter)
        buffer.insert(siter, text, -1)

    def get_word_start(self, iter):
        pre_char = self.get_pre_char(iter)
        while pre_char == '_':
            iter.backward_visible_word_start()
            pre_char = self.get_pre_char(iter)

    def get_pre_char(self, iter):
        pre_char = None
        if iter.backward_char():
            pre_char = iter.get_char()
            iter.forward_char()

        return pre_char