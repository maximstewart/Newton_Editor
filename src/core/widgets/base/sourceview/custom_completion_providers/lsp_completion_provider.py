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
        This code is A python code completion plugin for Newton.
        # NOTE: Some code pulled/referenced from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'PythonProvider'

    def __init__(self, source_view):
        GObject.Object.__init__(self)

        self._theme       = Gtk.IconTheme.get_default()
        self._source_view = source_view

    def do_get_name(self):
        return "LSP Code Completion"

    def get_iter_correctly(self, context):
        return context.get_iter()[1] if isinstance(context.get_iter(), tuple) else context.get_iter()

    def do_match(self, context):
        event_system.emit("textDocument/completion", (self._source_view, context, self.do_populate))
        return True

    def do_get_priority(self):
        return 1

    def do_get_activation(self):
        return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context, result = None):
        proposals = []
        if result:
            if result.items:
                for item in result.items:
                    comp_item = GtkSource.CompletionItem.new()
                    comp_item.set_label(item.label)
                    comp_item.set_text(item.textEdit)
                    comp_item.set_icon( self.get_icon_for_type(item.kind) )
                    comp_item.set_info(item.documentation)
                    proposals.append(comp_item)
            else:
                comp_item = GtkSource.CompletionItem.new()
                comp_item.set_label(item.label)
                comp_item.set_text(item.textEdit)
                comp_item.set_icon( self.get_icon_for_type(item.kind) )
                comp_item.set_info(item.documentation)
                proposals.append(comp_item)

        context.add_proposals(self, proposals, True)

    def get_icon_for_type(self, _type):
        try:
            return self._theme.load_icon(icon_names[_type.lower()], 16, 0)
        except:
            try:
                return self._theme.load_icon(Gtk.STOCK_ADD, 16, 0)
            except:
                return None