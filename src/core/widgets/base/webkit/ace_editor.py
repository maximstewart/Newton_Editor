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



class AceEditor(WebKit2.WebView):
    def __init__(self):
        super(AceEditor, self).__init__()

        # self.get_context().set_sandbox_enabled(False)

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
        event_system.subscribe("load_file", self.load_file)

        event_system.subscribe("updated_tab", self.updated_tab)
        event_system.subscribe("ui_message", self.ui_message)


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
            event_system.emit("handle_bridge_event", (event,))
        except Exception as e:
            logger.info(e)

    def load_file(self, ftype: str, fhash: str, file: str, content: str):
        command = f"loadFile('{ftype}', '{fhash}', '{file}', '{content}')"
        self.run_javascript(command, None, None)

    def updated_tab(self, ftype, fname):
        command = f"updatedTab('{ftype}', '{fname}')"
        self.run_javascript(command, None, None)

    def ui_message(self, message, mtype):
        command = f"displayMessage('{message}', '{mtype}', '3')"
        self.run_javascript(command, None, None)


class WebkitUISettings(WebKit2.Settings):
    def __init__(self):
        super(WebkitUISettings, self).__init__()

        self._set_default_settings()


    # Note: Highly insecure setup but most "app" like setup I could think of.
    #       Audit heavily any scripts/links ran/clicked under this setup!
    def _set_default_settings(self):
        self.set_enable_xss_auditor(False)
        self.set_enable_hyperlink_auditing(False)
        self.set_allow_file_access_from_file_urls(True)
        self.set_allow_universal_access_from_file_urls(True)

        self.set_enable_page_cache(False)
        self.set_enable_offline_web_application_cache(False)
        self.set_enable_html5_local_storage(False)
        self.set_enable_html5_database(False)

        self.set_enable_fullscreen(False)
        self.set_print_backgrounds(False)
        self.set_enable_tabs_to_links(False)
        self.set_enable_developer_extras(True)
        self.set_enable_webrtc(True)
        self.set_enable_webaudio(True)
        self.set_enable_accelerated_2d_canvas(True)

        self.set_user_agent(f"{app_name}")