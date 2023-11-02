# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports



class SourceViewDnDMixin:

    def _set_up_dnd(self):
        PLAIN_TEXT_TARGET_TYPE = 70
        URI_TARGET_TYPE        = 80
        text_target        = Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags(0), PLAIN_TEXT_TARGET_TYPE)
        uri_target         = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)
        targets            = [ text_target, uri_target ]
        self.drag_dest_set_target_list(targets)

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 70: return

        if info == 80:
            buffer = self.get_buffer()
            uris   = data.get_uris()

            if len(uris) == 0:
                uris = data.get_text().split("\n")

            if not self._current_file and not buffer.get_modified():
                gfile = Gio.File.new_for_uri(uris[0])
                self.open_file(gfile)
                uris.pop(0)

            for uri in uris:
                gfile = None
                try:
                    gfile = Gio.File.new_for_uri(uri)
                except Exception as e:
                    gfile = Gio.File.new_for_path(uri)

                event_system.emit('create_view', (gfile,))
