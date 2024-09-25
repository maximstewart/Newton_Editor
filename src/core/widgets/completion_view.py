# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
        self.set_size_request(320, 320)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        viewport        = Gtk.Viewport()
        self.button_box = Gtk.Box()

        self.button_box.set_orientation( Gtk.Orientation.VERTICAL )
        self.button_box.set_hexpand( True )

        viewport.add(self.button_box)
        self.add(viewport)
    
    def add_completion_item(self, item: CompletionItem):
        self.button_box.add(item)

    def clear_items(self):
        for child in self.button_box.get_children():
            self.button_box.remove(child)

    def activate_completion(self):
        ...

    def move_selection_up(self):
        ...

    def move_selection_down(self):
        ...

