# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio

# Application imports



class DnDMixin:

    def _setup_dnd(self):
        flags   = Gtk.DestDefaults.ALL

        PLAIN_TEXT_TARGET_TYPE = 70
        URI_TARGET_TYPE        = 80

        text_target = Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags(0), PLAIN_TEXT_TARGET_TYPE)
        uri_target  = Gtk.TargetEntry.new('text/uri-list', Gtk.TargetFlags(0), URI_TARGET_TYPE)

        # targets   = [ text_target, uri_target ]
        targets     = [ uri_target ]

        action      = Gdk.DragAction.COPY

        # self.drag_dest_set_target_list(targets)
        self.drag_dest_set(flags, targets, action)

        self._setup_dnd_signals()

    def _setup_dnd_signals(self):
        # self.drag_motion_id        = self.connect("drag-motion",        self._on_drag_motion)
        # self.drag_drop_id          = self.connect('drag-drop',          self._on_drag_set)
        self.drag_data_received_id = self.connect("drag-data-received", self._on_drag_data_received)

    def _on_drag_motion(self, widget, drag_context, x, y, time):
        Gdk.drag_status(drag_context, drag_context.get_actions(), time)

        return False

    def _on_drag_set(self, widget, drag_context, data, info, time):
        self.drag_get_data(drag_context, drag_context.list_targets()[-1], time)

        return False

    def _on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        if info == 70: return

        if info == 80:
            uris   = data.get_uris()
            files  = []

            if len(uris) == 0:
                uris = data.get_text().split("\n")

            for uri in uris:
                gfile = None
                try:
                    gfile = Gio.File.new_for_uri(uri)
                except Exception as e:
                    gfile = Gio.File.new_for_path(uri)

                files.append(gfile)

            event_system.emit(f"set_pre_drop_dnd_{self.INDEX}", (files,))
