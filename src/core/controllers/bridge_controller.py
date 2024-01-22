# Python imports
import base64

# Lib imports

# Application imports



class BridgeController:
    def __init__(self):

        self.opened_files = {}

        self._setup_signals()
        self._subscribe_to_events()


    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("handle_bridge_event", self.handle_bridge_event)


    def handle_bridge_event(self, event):
        match event.topic:
            case "save":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "close":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "load_buffer":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "load_file":
                event_system.emit(f"handle_file_event_{event.originator}", (event,))
            case "error":
                content = base64.b64decode( event.content.encode() ).decode("utf-8")
                logger.info(content)
            case _:
                ...