# Python imports

# Lib imports

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
        if isinstance(message, dict):
            ...
        if isinstance(message, LSPResponseRequest):
            ...
        if isinstance(message, LSPResponseNotification):
            ...
