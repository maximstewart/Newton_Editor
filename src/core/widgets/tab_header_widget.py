# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TabHeaderWidget(Gtk.Box):
    """ docstring for TabHeaderWidget """

    def __init__(self, content, close_tab):
        super(TabHeaderWidget, self).__init__()

        self.content   = content
        self.close_tab = close_tab

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        self.set_orientation(0)
        self.set_hexpand(False)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        self.label = Gtk.Label(label = "buffer")
        close  = Gtk.Button()
        icon   = Gtk.Image(stock = Gtk.STOCK_CLOSE)

        # TODO: Setup with settings and from file
        self.label.set_xalign(0.0)
        self.label.set_margin_left(25)
        self.label.set_margin_right(25)
        self.label.set_hexpand(True)

        close.set_always_show_image(True)
        close.set_hexpand(False)
        close.set_image( Gtk.Image.new_from_icon_name("gtk-close", 4) )
        close.connect("released", self.close_tab, *(self.content,))

        self.add(self.label)
        self.add(close)