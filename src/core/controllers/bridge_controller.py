# Python imports
import base64

# Lib imports

# Application imports



class BridgeController:
    def __init__(self):

        self.originator   = -1

        self._setup_signals()
        self._subscribe_to_events()


    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("handle_bridge_event", self.handle_bridge_event)
        event_system.subscribe(f"keyboard_open_file", self.keyboard_open_file)
        event_system.subscribe(f"keyboard_scale_up_text", self.keyboard_scale_up_text)
        event_system.subscribe(f"keyboard_scale_down_text", self.keyboard_scale_down_text)
        event_system.subscribe(f"find_entry", self.find_entry)
        event_system.subscribe(f"find_next_entry", self.find_next_entry)
        event_system.subscribe(f"find_previous_entry", self.find_previous_entry)
        event_system.subscribe(f"replace_entry", self.replace_entry)
        event_system.subscribe(f"toggle_highlight_line", self.toggle_highlight_line)

    def keyboard_open_file(self, gfiles):
        event_system.emit(f"set_pre_drop_dnd_{self.originator}", (gfiles,))

    def keyboard_scale_up_text(self):
        event_system.emit(f"keyboard_scale_up_text_{self.originator}")

    def keyboard_scale_down_text(self):
        event_system.emit(f"keyboard_scale_down_text_{self.originator}")

    def toggle_highlight_line(self):
        event_system.emit(f"toggle_highlight_line_{self.originator}")

    def find_entry(self, query, isBackwwards, isWrap, isCaseSensitive,
                                                        useWholeWord,
                                                        useRegExp):
        event_system.emit(
            f"find_entry_{self.originator}",
            (
                query,
                isBackwwards,
                isWrap,
                isCaseSensitive,
                useWholeWord,
                useRegExp
            )
        )

    def find_next_entry(self):
        event_system.emit(f"find_next_entry_{self.originator}")

    def find_previous_entry(self):
        event_system.emit(f"find_previous_entry_{self.originator}")

    def replace_entry(self, fromStr, toStr):
        event_system.emit(f"replace_entry_{self.originator}", (fromStr, toStr,))

    def replace_all(self, fromStr, toStr):
        event_system.emit(f"replace_all_{self.originator}", (fromStr, toStr,))


    def handle_bridge_event(self, event):
        self.originator = event.originator

        match event.topic:
            case "load_starting_files":
                for file in settings_manager.get_starting_files():
                    event_system.emit("post_file_to_ipc", file)
            case "save":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "load_buffer":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "load_file":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "open_file":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "tggl_search_replace":
                event_system.emit(f"tggl_search_replace")
            case "tggl_top_main_menubar":
                event_system.emit("tggl_top_main_menubar")
            case "set_info_labels":
                content = base64.b64decode( event.content.encode() ).decode("utf-8")
                path          = event.fpath
                line_char     = content
                file_type     = event.ftype
                encoding_type = "utf-8"
                event_system.emit(f"set_info_labels", (path, line_char, file_type, encoding_type,))
            case "load_javascript":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "error":
                content = base64.b64decode( event.content.encode() ).decode("utf-8")
                logger.info(content)
            case _:
                ...