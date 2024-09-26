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

        self.button_box = None

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

        self.button_box.connect("key-press-event", self._key_press_event)

        viewport.add(self.button_box)
        self.add(viewport)


    # This is depressing but only way I can get to scroll with items getting selected.
    # Cannot figure out how to just manually scroll widget into view with code.
    def _key_press_event(self, widget, eve):
        keyname    = Gdk.keyval_name(eve.keyval)
        modifiers  = Gdk.ModifierType(eve.get_state() & ~Gdk.ModifierType.LOCK_MASK)
        is_control = True if modifiers & Gdk.ModifierType.CONTROL_MASK else False
        is_shift   = True if modifiers & Gdk.ModifierType.SHIFT_MASK else False

        if is_control:
            return True

        if keyname in [ "Up" ]:
            self.move_selection_up()
            return True

        if keyname in [ "Down" ]:
            self.move_selection_down()
            return True

        if keyname in [ "Enter", "Return" ]:
            self.activate_completion()
            return True


    def add_completion_item(self, item: CompletionItem):
        self.button_box.add(item)

    def clear_items(self):
        for child in self.button_box.get_children():
            self.button_box.remove(child)

    def activate_completion(self):
        completion_item = self.button_box.get_selected_row().get_child()
        print()
        print()
        print(completion_item)
        print(completion_item.insertText)
        print(completion_item.additionalTextEdits)
        print()
        print()

    def move_selection_up(self):
        srow  = self.button_box.get_selected_row()
        if not srow:
            self.select_last_row()
            return

        index = srow.get_index() - 1
        if index == -1:
            index = len( self.button_box.get_children() ) - 1

        self.select_and_scroll_to_view(
            self.button_box.get_row_at_index(index)
        )

    def move_selection_down(self):
        srow  = self.button_box.get_selected_row()
        if not srow:
            self.select_first_row()
            return

        index = srow.get_index() + 1
        if index > (len( self.button_box.get_children() ) - 1):
            index = 0

        self.select_and_scroll_to_view(
            self.button_box.get_row_at_index(index)
        )


    def select_first_row(self):
        row = self.button_box.get_row_at_y(0)
        if not row: return
        self.select_and_scroll_to_view(row)

    def select_last_row(self):
        row = self.button_box.get_row_at_y( len( self.button_box.get_children() ) - 1)
        if not row: return
        self.select_and_scroll_to_view(row)

    def select_and_scroll_to_view(self, row):
        self.button_box.select_row(row)
        GLib.idle_add( row.grab_focus )