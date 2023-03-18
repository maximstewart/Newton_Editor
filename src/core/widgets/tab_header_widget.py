# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class TabHeaderWidget(Gtk.ButtonBox):
    """docstring for TabHeaderWidget"""

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
        self._load_widgets()


    def _setup_styling(self):
        self.set_orientation(0)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        label = Gtk.Label()
        close = Gtk.Button()
        icon  = Gtk.Image(stock=Gtk.STOCK_CLOSE)

        label.set_label("untitled")
        label.set_width_chars(len(self.NAME))
        label.set_xalign(0.0)

        close.set_always_show_image(True)
        close.set_hexpand(False)
        close.set_size_request(32, 32)
        close.set_image( Gtk.Image.new_from_icon_name("gtk-close", 4) )
        close.connect("released", self._close_tab, *(self._scroll_view, self._source_view,))

        self.add(label)
        self.add(close)

        self.show_all()
