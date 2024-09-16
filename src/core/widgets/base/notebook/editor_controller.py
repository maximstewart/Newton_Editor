# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports
from libs.dto.lsp_message_structs import LSPResponseTypes, LSPResponseRequest, LSPResponseNotification
from .key_input_controller import KeyInputController
from .editor_events import EditorEventsMixin



class EditorControllerMixin(KeyInputController, EditorEventsMixin):
    def get_active_view(self):
        page_num    = self.get_current_page()
        container   = self.get_nth_page( page_num )
        source_view = container.get_source_view()
        return page_num, container, source_view

    def action_controller(self, action = "", query = ""):
        # NOTE: Not efficent here as multiple same calls
        if not self.is_editor_focused: # TODO: Find way to converge this
            return

        page_num, container, source_view = self.get_active_view()

        # NOTE: These feel bad being here man...
        if action == "scale_up_text":
            self.scale_up_text(source_view)
        if action == "scale_down_text":
            self.scale_down_text(source_view)
        if action == "set_buffer_language":
            self.set_buffer_language(source_view, query)
        if action == "set_buffer_style":
            self.set_buffer_style(source_view, query)

    def _handle_lsp_message(self, message: dict or LSPResponseTypes):
        if not self.is_editor_focused: return # TODO: Find way to converge this
        page_num, container, source_view = self.get_active_view()
        page_num  = None
        container = None

        logger.debug( repr(message) )

        if isinstance(message, dict):
            ...

        if hasattr(message, "result"):
            keys = message.result.keys()

            if "items" in keys:
                buffer     = source_view.get_buffer()
                completion = source_view.get_completion()
                providers  = completion.get_providers()

                for provider in providers:
                    if provider.__class__.__name__ == 'LSPCompletionProvider':
                        # context = completion.create_context( buffer.get_iter_at_mark( buffer.get_insert() ) )
                        # context = completion.create_context( None )
                        # provider.do_populate(context, message.result["items"])

                        box  = Gtk.Box()
                        box.set_homogeneous(True)
                        # iter = buffer.get_iter_at_mark( buffer.get_insert() )
                        # rects, recte = source_view.get_cursor_locations(iter)
                        rect = source_view.get_allocation()

                        box.set_orientation( Gtk.Orientation.VERTICAL )
                        for item in message.result["items"]:
                            box.add( provider.create_completion_item_button(item) )

                        box.show_all()
                        source_view.add_child_in_window(box, Gtk.TextWindowType.WIDGET, rect.width - 200, rect.height / 2)

            if "result" in keys:
                ...

        if hasattr(message, "method"):
            if message.method == "textDocument/publshDiagnostics":
                ...

        source_view = None