# Python imports
import json

# Lib imports
import gi
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gdk
from gi.repository import WebKit2
from gi.repository import GLib

# Application imports
from libs.data_types import Event
from libs.settings_manager.other.webkit_ui_settings import WebkitUISettings



class AceEditor(WebKit2.WebView):
    def __init__(self, index):
        super(AceEditor, self).__init__()

        # self.get_context().set_sandbox_enabled(False)
        self.INDEX = index

        self._load_settings()
        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_view()
        self._setup_content_manager()

        self.show_all()

        if settings_manager.is_debug():
            inspector = self.get_inspector()
            inspector.show()

    def _setup_styling(self):
        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_background_color( Gdk.RGBA(0, 0, 0, 0.0) )

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe(f"load_file_{self.INDEX}", self.load_file)
        event_system.subscribe(f"new_session_{self.INDEX}", self.new_session)
        event_system.subscribe(f"switch_session_{self.INDEX}", self.switch_session)
        event_system.subscribe(f"updated_session_{self.INDEX}", self.updated_session)
        event_system.subscribe(f"close_session_{self.INDEX}", self.close_session)
        event_system.subscribe(f"remove_session_{self.INDEX}", self.remove_session)
        event_system.subscribe(f"keyboard_scale_up_text_{self.INDEX}", self.keyboard_scale_up_text)
        event_system.subscribe(f"keyboard_scale_down_text_{self.INDEX}", self.keyboard_scale_down_text)
        event_system.subscribe(f"toggle_highlight_line_{self.INDEX}", self.toggle_highlight_line)

        event_system.subscribe(f"ui_message_{self.INDEX}", self.ui_message)

    def _load_settings(self):
        self.set_settings( WebkitUISettings() )

    def _load_view(self):
        path = settings_manager.get_context_path()
        data = None

        with open(f"{path}/index.html", "r") as f:
            data = f.read()

        self.load_html(content = data, base_uri = f"file://{path}/")

    def _setup_content_manager(self):
        content_manager = self.get_user_content_manager()

        content_manager.connect("script-message-received", self._process_js_message)
        content_manager.register_script_message_handler("backend")

    def _process_js_message(self, user_content_manager, js_result):
        js_value = js_result.get_js_value()
        message  = js_value.to_string()

        try:
            event = Event( **json.loads(message) )
            event.originator = self.INDEX
            event_system.emit("handle_bridge_event", (event,))
        except Exception as e:
            logger.info(e)

    def load_file(self, ftype: str, fname: str, fpath: str, content: str, line: int = 0):
        command = f"loadFile('{ftype}', '{fname}', '{fpath}', '{content}', '{line}')"
        self.run_javascript(command, None, None)

    def new_session(self):
        command = f"newSession()"
        self.run_javascript(command, None, None)

    def switch_session(self, fhash):
        command = f"switchSession('{fhash}')"
        self.run_javascript(command, None, None)

    def updated_session(self, fhash, ftype, fname, fpath):
        command = f"updateSession('{fhash}', '{ftype}', '{fname}', '{fpath}')"
        self.run_javascript(command, None, None)

    def close_session(self, fhash):
        command = f"closeSession('{fhash}')"
        self.run_javascript(command, None, None)

    def remove_session(self, fhash):
        command = f"removeSession('{fhash}')"
        self.run_javascript(command, None, None)

    def keyboard_scale_up_text(self):
        command = "zoomIn()"
        self.run_javascript(command, None, None)

    def keyboard_scale_down_text(self):
        command = "zoomOut()"
        self.run_javascript(command, None, None)

    def toggle_highlight_line(self):
        command = "toggleLineHighlight()"
        self.run_javascript(command, None, None)

    def ui_message(self, message, mtype):
        command = f"displayMessage('{message}', '{mtype}', '3')"
        self.run_javascript(command, None, None)

    def run_javascript(self, script, cancellable, callback):
        logger.debug(script)
        super().run_javascript(script, cancellable, callback)
