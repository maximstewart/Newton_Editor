# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .widgets.separator_widget import Separator
from .widgets.save_file_dialog import SaveFileDialog
from .widgets.base.general_info_widget import GeneralInfoWidget
from .widgets.base.banner_controls import BannerControls
from .editors_container import EditorsContainer



class CoreWidget(Gtk.Box):
    def __init__(self):
        super(CoreWidget, self).__init__()

        builder  = settings_manager.get_builder()
        self.ctx = self.get_style_context()
        builder.expose_object("core_widget", self)


        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.ctx.add_class("main-window")
        self.set_orientation(1) # VERTICAL = 1

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("update_transparency", self._update_transparency)
        event_system.subscribe("remove_transparency", self._remove_transparency)

    def _load_widgets(self):
        SaveFileDialog()
        GeneralInfoWidget()

        self.add(BannerControls())
        self.add(Separator("separator_top"))
        self.add(EditorsContainer())
        self.add(Separator("separator_botton"))

    def _update_transparency(self):
        self.ctx.add_class(f"mw_transparency_{settings.theming.transparency}")

    def _remove_transparency(self):
        self.ctx.remove_class(f"mw_transparency_{settings.theming.transparency}")
