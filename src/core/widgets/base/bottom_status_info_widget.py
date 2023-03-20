# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports


# NOTE: https://github.com/rwaldron/gtksourceview/blob/master/tests/test-widget.py


class BottomStatusInfoWidget:
    """docstring for BottomStatusInfoWidget."""

    def __init__(self):
        super(BottomStatusInfoWidget, self).__init__()

        _GLADE_FILE   = f"{settings.get_ui_widgets_path()}/bottom_status_info_ui.glade"
        self._builder = Gtk.Builder()
        self._builder.add_from_file(_GLADE_FILE)

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("set_bottom_labels", self.set_bottom_labels)

        event_system.subscribe("set_path_label", self._set_path_label)
        event_system.subscribe("set_encoding_label", self._set_encoding_label)
        event_system.subscribe("set_line_char_label", self._set_line_char_label)
        event_system.subscribe("set_file_type_label", self._set_file_type_label)


    def _load_widgets(self):
        builder = settings.get_builder()

        self.bottom_status_info      = self._builder.get_object("bottom_status_info")
        self.bottom_path_label       = self._builder.get_object("bottom_path_label")
        self.bottom_encoding_label   = self._builder.get_object("bottom_encoding_label")
        self.bottom_line_char_label  = self._builder.get_object("bottom_line_char_label")
        self.bottom_file_type_label  = self._builder.get_object("bottom_file_type_label")

        builder.expose_object(f"bottom_status_info", self.bottom_status_info)
        builder.expose_object(f"bottom_path_label", self.bottom_path_label)
        builder.expose_object(f"bottom_encoding_label", self.bottom_encoding_label)
        builder.expose_object(f"bottom_line_char_label", self.bottom_line_char_label)
        builder.expose_object(f"bottom_file_type_label", self.bottom_file_type_label)

        self.bottom_path_label.set_hexpand(True)
        self._set_line_char_label()

        builder.get_object("core_widget").add(self.bottom_status_info)


    def set_bottom_labels(self, gfile, info):
        self.bottom_path_label.set_text( gfile.get_path() )
        self.bottom_path_label.set_tooltip_text( gfile.get_path() )

        self.bottom_encoding_label.set_text("utf-8")
        self.bottom_line_char_label.set_text("0:0")
        self.bottom_file_type_label.set_text( info.get_content_type() )

    def _set_path_label(self):
        ...

    def _set_encoding_label(self):
        ...

    def _set_line_char_label(self, label = "0:0"):
        self.bottom_line_char_label.set_text(label)

    def _set_file_type_label(self):
        ...
