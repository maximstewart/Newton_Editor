# Python imports

# Lib imports
import gi
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

# Application imports



class WebkitUISettings(WebKit2.Settings):
    def __init__(self):
        super(WebkitUISettings, self).__init__()
        
        self._set_default_settings()


    # Note: Highly insecure setup but most "app" like setup I could think of.
    #       Audit heavily any scripts/links ran/clicked under this setup! 
    def _set_default_settings(self):
        self.set_enable_xss_auditor(True)
        self.set_enable_hyperlink_auditing(True)
        # self.set_enable_xss_auditor(False)
        # self.set_enable_hyperlink_auditing(False)
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