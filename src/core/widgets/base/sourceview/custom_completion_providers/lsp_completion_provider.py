# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject

# Application imports



class LSPCompletionProvider(GObject.Object, GtkSource.CompletionProvider):
    """
        This code is an LSP code completion plugin for Newton.
        # NOTE: Some code pulled/referenced from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'LSPProvider'

    def __init__(self, source_view):
        GObject.Object.__init__(self)

        self._theme       = Gtk.IconTheme.get_default()
        self._source_view = source_view


    def do_get_name(self):
        return "LSP Code Completion"

    def get_iter_correctly(self, context):
        return context.get_iter()[1] if isinstance(context.get_iter(), tuple) else context.get_iter()

    def do_match(self, context):
        return True

    def do_get_priority(self):
        return 1

    def do_get_activation(self):
        return GtkSource.CompletionActivation.USER_REQUESTED

    def do_populate(self, context, items = []):
        if hasattr(self._source_view, "completion_items"):
            items = self._source_view.completion_items

        proposals = []
        for item in items:
            proposals.append( self.create_completion_item(item) )

        context.add_proposals(self, proposals, True)

    def get_icon_for_type(self, _type):
        try:
            return self._theme.load_icon(icon_names[_type.lower()], 16, 0)
        except:
            ...

        try:
            return self._theme.load_icon(Gtk.STOCK_ADD, 16, 0)
        except:
            ...

        return None

    def create_completion_item(self, item):
        comp_item = GtkSource.CompletionItem.new()
        keys      = item.keys()
        comp_item.set_label(item["label"])

        if "insertText" in keys:
            comp_item.set_text(item["insertText"])

        return comp_item


    # def create_completion_item(self, item):
    #     comp_item = GtkSource.CompletionItem.new()
    #     comp_item.set_label(item.label)

    #     if item.textEdit:
    #         if isinstance(item.textEdit, dict):
    #             comp_item.set_text(item.textEdit["newText"])
    #         else:
    #             comp_item.set_text(item.textEdit)
    #     else:
    #         comp_item.set_text(item.insertText)

    #     comp_item.set_icon( self.get_icon_for_type(item.kind) )
    #     comp_item.set_info(item.documentation)

    #     return comp_item