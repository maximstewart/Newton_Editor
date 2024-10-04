# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports



class CompletionItem(Gtk.Label):
    def __init__(self):
        super(CompletionItem, self).__init__()

        self.kind: int               = -1
        self.newText: str            = ""
        self.insertText: str         = ""
        self.textEdit: []            = []
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

        if "kind" in keys:
            self.kind = item["kind"]

        if "insertText" in keys:
            self.insertText = item["insertText"]

        if "textEdit" in keys:
            self.textEdit = item["textEdit"]
            self.newText  = item["textEdit"]["newText"]

        if "additionalTextEdits" in keys:
            self.additionalTextEdits = item["additionalTextEdits"]