# Python imports
import urllib.parse as url_parse

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GtkSource

# Application imports
from libs.dto.lsp_message_structs import LSPResponseTypes, LSPResponseRequest, LSPResponseNotification, LSPIDResponseNotification
from .key_input_controller import KeyInputController
from .editor_events import EditorEventsMixin
from ...completion_item import CompletionItem



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

    def _handle_lsp_message(self, message: dict or LSPResponseType):
        if not self.is_editor_focused: return # TODO: Find way to converge this
        page_num, container, source_view = self.get_active_view()
        page_num  = None
        container = None

        logger.debug( f"\n\n{repr(message)}\n\n" )

        if isinstance(message, dict):
            ...

        if hasattr(message, "result"):
            if type(message.result) is dict:
                keys = message.result.keys()

                if "items" in keys: # completion
                    if source_view.completion_view.get_parent():
                        source_view.remove(source_view.completion_view)

                    source_view.completion_view.clear_items()
                    x, y = self._get_insert_line_xy(source_view)
                    source_view.add_child_in_window(source_view.completion_view,  Gtk.TextWindowType.WIDGET, x, y)

                    for item in message.result["items"]:
                        ci = CompletionItem()
                        ci.populate_completion_item(item)
                        source_view.completion_view.add_completion_item(ci)

                    if len( message.result["items"] ) > 0:
                        source_view.completion_view.show_all()
                        GLib.idle_add( source_view.completion_view.select_first_row )

                    # completion = source_view.get_completion()
                    # providers  = completion.get_providers()

                    # for provider in providers:
                    #     if provider.__class__.__name__ == 'LSPCompletionProvider':
                    #         source_view.completion_items = message.result["items"]
                    #         source_view.emit("show-completion")


                if "result" in keys:
                    ...

            if type(message.result) is list:
                if len(message.result) == 1:  # goto/aka definition
                    result = message.result[0]
                    line   = result["range"]["start"]["line"]
                    uri    = result["uri"].replace("file://", "")
                    if "jdt:" in uri:
                        uri = self.parse_java_jdt_to_uri(uri)

                    file = f"{uri}:{line}"
                    event_system.emit("handle_file_from_ipc", file)

        if hasattr(message, "method"):
            if message.method == "textDocument/publshDiagnostics":
                ...

        source_view = None

    def parse_java_jdt_to_uri(self, uri):
        parse_str     = url_parse.unquote(uri)
        post_stub, \
        pre_stub      = parse_str.split("?=")

        post_stub     = post_stub.replace("jdt://contents/", "")
        replace_stub  = post_stub[
            post_stub.index(".jar") + 4 : post_stub.index(".class")
        ]
        post_stub     = post_stub.replace(replace_stub, replace_stub.replace(".", "/") ) \
                            .replace(".jar", "-sources.jar:")
        post_stub     = post_stub.replace(".class", ".java")

        pre_stub      = pre_stub[
            pre_stub.index("/\\/") + 2 : pre_stub.index(".jar")
        ]
        pre_stub      = pre_stub[: pre_stub.rfind("/") + 1 ].replace("\\", "")

        return f"file://{pre_stub}{post_stub}"

    # Gotten logic from:
    # https://stackoverflow.com/questions/7139645/find-the-cursor-position-on-a-gtksourceview-window
    def _get_insert_line_xy(self, source_view):
        buffer   = source_view.get_buffer()
        iter     = buffer.get_iter_at_mark( buffer.get_insert() )
        iter_loc = source_view.get_iter_location(iter)

        win_loc  = source_view.buffer_to_window_coords(Gtk.TextWindowType.WIDGET, iter_loc.x, iter_loc.y)

        win      = source_view.get_window( Gtk.TextWindowType.WIDGET )
        view_pos = win.get_position()

        xx = win_loc[0] + view_pos[0]
        yy = win_loc[1] + view_pos[1] + iter_loc.height

        return xx, yy