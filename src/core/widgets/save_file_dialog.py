# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio

# Application imports



class SaveFileDialog:
    """docstring for SaveFileDialog."""

    def __init__(self):
        super(SaveFileDialog, self).__init__()

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        ...

    def _subscribe_to_events(self):
        event_system.subscribe("save_file_dialog", self.save_file_dialog)

    def _load_widgets(self):
        self._file_filter_text = Gtk.FileFilter()
        self._file_filter_text.set_name("Text Files")

        for p in settings.filters.code:
            self._file_filter_text.add_pattern(p)

        self._file_filter_all = Gtk.FileFilter()
        self._file_filter_all.set_name("All Files")
        self._file_filter_all.add_pattern("*.*")


    def save_file_dialog(self, current_filename: str = "", current_file: Gio.File = None) -> str:
        # TODO: Move Chooser logic to own widget
        dlg = Gtk.FileChooserDialog(title = "Please choose a file...", parent = None, action = 1)

        dlg.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        dlg.set_do_overwrite_confirmation(True)
        dlg.add_filter(self._file_filter_text)
        dlg.add_filter(self._file_filter_all)

        if current_filename == "":
            dlg.set_current_name("new.txt")
        else:
            dlg.set_current_folder(current_file.get_parent().get_path())
            dlg.set_current_name(current_filename)

        response = dlg.run()
        file     = dlg.get_filename() if response == Gtk.ResponseType.OK else ""
        dlg.destroy()

        return Gio.File.new_for_path(file) if not file == "" else None
