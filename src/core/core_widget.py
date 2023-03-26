# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from .widgets.base.banner_controls import BannerControls
from .editors_container import EditorsContainer
from .widgets.base.general_info_widget import GeneralInfoWidget



class CoreWidget(Gtk.Box):
    def __init__(self):
        super(CoreWidget, self).__init__()

        builder = settings.get_builder()
        builder.expose_object("core_widget", self)

        self._setup_styling()
        self._setup_signals()
        self._load_widgets()

        self.show()


    def _setup_styling(self):
        self.set_orientation(1)

    def _setup_signals(self):
        ...

    def _load_widgets(self):
        self.add(BannerControls())
        GeneralInfoWidget()
        self.add(EditorsContainer())
