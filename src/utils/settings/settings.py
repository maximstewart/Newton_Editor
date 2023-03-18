# Python imports
import os
import json
import inspect

# Lib imports

# Application imports
from .start_check_mixin import StartCheckMixin


class MissingConfigError(Exception):
    pass



class Settings(StartCheckMixin):
    def __init__(self):
        self._SCRIPT_PTH        = os.path.dirname(os.path.realpath(__file__))
        self._USER_HOME         = os.path.expanduser('~')
        self._USR_PATH          = f"/usr/share/{app_name.lower()}"

        self._USR_CONFIG_FILE   = f"{self._USR_PATH}/settings.json"
        self._HOME_CONFIG_PATH  = f"{self._USER_HOME}/.config/{app_name.lower()}"
        self._PLUGINS_PATH      = f"{self._HOME_CONFIG_PATH}/plugins"
        self._DEFAULT_ICONS     = f"{self._HOME_CONFIG_PATH}/icons"
        self._CONFIG_FILE       = f"{self._HOME_CONFIG_PATH}/settings.json"
        self._GLADE_FILE        = f"{self._HOME_CONFIG_PATH}/Main_Window.glade"
        self._CSS_FILE          = f"{self._HOME_CONFIG_PATH}/stylesheet.css"
        self._KEY_BINDINGS_FILE = f"{self._HOME_CONFIG_PATH}/key-bindings.json"
        self._PID_FILE          = f"{self._HOME_CONFIG_PATH}/{app_name.lower()}.pid"
        self._WINDOW_ICON       = f"{self._DEFAULT_ICONS}/icons/{app_name.lower()}.png"

        if not os.path.exists(self._HOME_CONFIG_PATH):
            os.mkdir(self._HOME_CONFIG_PATH)
        if not os.path.exists(self._PLUGINS_PATH):
            os.mkdir(self._PLUGINS_PATH)

        if not os.path.exists(self._CONFIG_FILE):
            import shutil
            try:
                shutil.copyfile(self._USR_CONFIG_FILE, self._CONFIG_FILE)
            except Exception as e:
                raise

        if not os.path.exists(self._DEFAULT_ICONS):
            self._DEFAULT_ICONS = f"{self._USR_PATH}/icons"
            if not os.path.exists(self._DEFAULT_ICONS):
                raise MissingConfigError("Unable to find the application icons directory.")
        if not os.path.exists(self._GLADE_FILE):
            self._GLADE_FILE   = f"{self._USR_PATH}/Main_Window.glade"
            if not os.path.exists(self._GLADE_FILE):
                raise MissingConfigError("Unable to find the application Glade file.")
        if not os.path.exists(self._KEY_BINDINGS_FILE):
            self._KEY_BINDINGS_FILE = f"{self._USR_PATH}/key-bindings.json"
            if not os.path.exists(self._KEY_BINDINGS_FILE):
                raise MissingConfigError("Unable to find the application Keybindings file.")
        if not os.path.exists(self._CSS_FILE):
            self._CSS_FILE     = f"{self._USR_PATH}/stylesheet.css"
            if not os.path.exists(self._CSS_FILE):
                raise MissingConfigError("Unable to find the application Stylesheet file.")
        if not os.path.exists(self._WINDOW_ICON):
            self._WINDOW_ICON  = f"{self._USR_PATH}/icons/{app_name.lower()}.png"
            if not os.path.exists(self._WINDOW_ICON):
                raise MissingConfigError("Unable to find the application icon.")


        with open(self._KEY_BINDINGS_FILE) as file:
            bindings = json.load(file)["keybindings"]
            keybindings.configure(bindings)

        self._main_window   = None
        self._main_window_w = 800
        self._main_window_h = 600
        self._builder       = None

        self._trace_debug   = False
        self._debug         = False
        self._dirty_start   = False

        self.load_settings()


    def register_signals_to_builder(self, classes=None):
        handlers = {}

        for c in classes:
            methods = None
            try:
                methods = inspect.getmembers(c, predicate=inspect.ismethod)
                handlers.update(methods)
            except Exception as e:
                ...

        self._builder.connect_signals(handlers)

    def set_main_window(self, window): self._main_window  = window
    def set_builder(self, builder) -> any:  self._builder = builder


    def get_monitor_data(self) -> list:
        screen = self._main_window.get_screen()
        monitors = []
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))
            print("{}x{}+{}+{}".format(monitor.width, monitor.height, monitor.x, monitor.y))

        return monitors

    def get_main_window(self)      -> any:   return self._main_window
    def get_main_window_width(self) -> Gtk.ApplicationWindow:  return self._main_window_w
    def get_main_window_height(self) -> Gtk.ApplicationWindow: return self._main_window_h
    def get_builder(self)          -> any:   return self._builder
    def get_glade_file(self)       -> str:   return self._GLADE_FILE

    def get_plugins_path(self)     -> str:   return self._PLUGINS_PATH
    def get_icon_theme(self)       -> str:   return self._ICON_THEME
    def get_css_file(self)         -> str:   return self._CSS_FILE
    def get_home_config_path(self) -> str:   return self._HOME_CONFIG_PATH
    def get_window_icon(self)      -> str:   return self._WINDOW_ICON
    def get_home_path(self)        -> str:   return self._USER_HOME

    # Filter returns
    def get_office_filter(self)    -> tuple: return tuple(self._settings["filters"]["office"])
    def get_vids_filter(self)      -> tuple: return tuple(self._settings["filters"]["videos"])
    def get_text_filter(self)      -> tuple: return tuple(self._settings["filters"]["text"])
    def get_music_filter(self)     -> tuple: return tuple(self._settings["filters"]["music"])
    def get_images_filter(self)    -> tuple: return tuple(self._settings["filters"]["images"])
    def get_pdf_filter(self)       -> tuple: return tuple(self._settings["filters"]["pdf"])

    def get_success_color(self)    -> str:   return self._theming["success_color"]
    def get_warning_color(self)    -> str:   return self._theming["warning_color"]
    def get_error_color(self)      -> str:   return self._theming["error_color"]

    def is_trace_debug(self)       -> str:   return self._trace_debug
    def is_debug(self)             -> str:   return self._debug

    def get_ch_log_lvl(self)       -> str:   return self._settings["debugging"]["ch_log_lvl"]
    def get_fh_log_lvl(self)       -> str:   return self._settings["debugging"]["fh_log_lvl"]

    def set_trace_debug(self, trace_debug):
        self._trace_debug = trace_debug

    def set_debug(self, debug):
        self._debug = debug


    def load_settings(self):
        with open(self._CONFIG_FILE) as f:
            self._settings = json.load(f)
            self._config   = self._settings["config"]
            self._theming  = self._settings["theming"]

    def save_settings(self):
        with open(self._CONFIG_FILE, 'w') as outfile:
            json.dump(self._settings, outfile, separators=(',', ':'), indent=4)
