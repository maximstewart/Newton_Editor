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
        if not self.is_editor_focused: return # TODO: Find way to converge this
        page_num, container, source_view = self.get_active_view()
        page_num  = None
        container = None

        # logger.debug( repr(message) )

        if isinstance(message, dict):
            ...

        if isinstance(message, LSPResponseRequest):
            keys = message.result.keys()
            if "items" in keys:
                self.handle_completion(message.result["items"])
            if "result" in keys:
                ...

        if isinstance(message, LSPResponseNotification):
            if message.method == "textDocument/publshDiagnostics":
                ...

        source_view = None


	# export const Text = 1;
	# export const Method = 2;
	# export const Function = 3;
	# export const Constructor = 4;
	# export const Field = 5;
	# export const Variable = 6;
	# export const Class = 7;
	# export const Interface = 8;
	# export const Module = 9;
	# export const Property = 10;
	# export const Unit = 11;
	# export const Value = 12;
	# export const Enum = 13;
	# export const Keyword = 14;
	# export const Snippet = 15;
	# export const Color = 16;
	# export const File = 17;
	# export const Reference = 18;
	# export const Folder = 19;
	# export const EnumMember = 20;
	# export const Constant = 21;
	# export const Struct = 22;
	# export const Event = 23;
	# export const Operator = 24;
	# export const TypeParameter = 25;

    def handle_completion(self, items):
        print()
        print()
        print()
        print(len(items))
        print()
        print()
        print()
        for item in items:
            if item["kind"] in [2, 3, 4, 5, 6, 7, 8, 10, 15]:
                # print(item)
                ...