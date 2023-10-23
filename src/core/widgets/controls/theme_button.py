# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports



class ThemePopover(Gtk.Popover):
    """docstring for ThemePopover."""

    def __init__(self):
        super(ThemePopover, self).__init__()

        self._style_choser = None

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()


    def _setup_styling(self):
        self.set_modal(True)
        self.set_position(Gtk.PositionType.BOTTOM)
        self.set_size_request(320, 280)

    def _setup_signals(self):
        event_system.subscribe("show_theme_popup", self._show_theme_popup)

    def _load_widgets(self):
        manager      = GtkSource.StyleSchemeManager()
        style_scheme = manager.get_scheme(settings.theming.syntax_theme)

        self._style_choser = GtkSource.StyleSchemeChooserWidget()
        self._style_choser.set_style_scheme(style_scheme)
        self._style_choser.show_all()
        self._style_choser.connect("button-release-event", self._set_theme)

        self.add(self._style_choser)


    def _show_theme_popup(self, widget = None, eve = None):
        self.popup()

    def _set_theme(self, widget = None, eve = None):
        style_scheme                  = widget.get_style_scheme()
        id                            = style_scheme.get_id()
        settings.theming.syntax_theme = id.lower()

        event_system.emit('set_buffer_style', ("set_buffer_style", id.lower(),))



class ThemeButton(Gtk.Button):
    def __init__(self):
        super(ThemeButton, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        self.set_label("Themes")
        self.set_image( Gtk.Image.new_from_icon_name("gtk-page-setup", 4) )
        self.set_always_show_image(True)
        self.set_image_position(1) # Left - 0, Right = 1
        self.set_margin_left(5)
        # self.set_margin_right(5)

    def _setup_signals(self):
        self.connect("clicked", self._show_popover)

    def _subscribe_to_events(self):
        ...

    def _load_widgets(self):
        popover = ThemePopover()
        popover.set_relative_to(self)


    def _show_popover(self, widget, eve = None):
        event_system.emit("show_theme_popup")
