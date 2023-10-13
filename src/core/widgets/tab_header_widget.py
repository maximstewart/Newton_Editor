# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TabHeaderWidget(Gtk.Box):
    """ docstring for TabHeaderWidget """

    ccount = 0
    def __new__(cls, *args, **kwargs):
        obj        = super(TabHeaderWidget, cls).__new__(cls)
        cls.ccount += 1
        return obj


    def __init__(self, scroll_view, source_view, close_tab):
        super(TabHeaderWidget, self).__init__()

        self.INDEX        = self.ccount
        self.NAME         = f"tab_{self.INDEX}"
        self._scroll_view = scroll_view
        self._source_view = source_view
        self._close_tab   = close_tab # NOTE: Close method in tab_mixin

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.set_tab_label()
        self.show_all()


    def _setup_styling(self):
        self.set_orientation(0)
        self.set_hexpand(False)

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        label  = Gtk.Label()
        close  = Gtk.Button()
        icon   = Gtk.Image(stock = Gtk.STOCK_CLOSE)

        # NOTE: Setup with settings and from file
        label.set_xalign(0.0)
        label.set_margin_left(25)
        label.set_margin_right(25)
        label.set_hexpand(True)

        close.set_always_show_image(True)
        close.set_hexpand(False)
        close.set_image( Gtk.Image.new_from_icon_name("gtk-close", 4) )
        close.connect("released", self._close_tab, *(self._scroll_view, self._source_view,))

        self.add(label)
        self.add(close)

    def set_tab_label(self, label = "untitled"):
        self.get_children()[0].set_label(label)

    def set_status(self, changed = False):
        label = self.get_children()[0]
        ctx   = label.get_style_context()

        ctx.add_class("buffer_changed") if changed else ctx.remove_class("buffer_changed")
