# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class CompletionItem(Gtk.Label):
    def __init__(self):
        super(CompletionItem, self).__init__()

        self.insertText: str = ""
        self.additionalTextEdits: [] = []

        self._setup_styling()
        self._setup_signals()

        self.show()


    def _setup_styling(self):
        ctx = self.get_style_context()
        ctx.add_class("completion-item")

    def _setup_signals(self):
        ...


    def populate_completion_item(self, item):
        keys      = item.keys()
        self.set_label(item["label"])

        if "insertText" in keys:
            self.insertText = item["insertText"]

        if "additionalTextEdits" in keys:
            self.additionalTextEdits = item["additionalTextEdits"]
