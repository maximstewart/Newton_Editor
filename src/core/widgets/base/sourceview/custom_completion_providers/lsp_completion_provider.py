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
        iter   = self.get_iter_correctly(context)
        buffer = iter.get_buffer()
        if buffer.get_context_classes_at_iter(iter) != ['no-spell-check']:
            return False

        ch = iter.get_char()
        # NOTE: Look to re-add or apply supprting logic to use spaces
        # As is it slows down the editor in certain contexts...
        if not (ch in ('_', '.', ' ') or ch.isalnum()):
        # if not (ch in ('_', '.') or ch.isalnum()):
            return False

        return True

    def do_get_priority(self):
        return 1

    def do_get_activation(self):
        return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context, result = None):
        result    = event_system.emit_and_await("textDocument/completion", (self._source_view,))
        proposals = []

        if result:
            if not result.items is None:
                for item in result.items:
                    proposals.append( self.create_completion_item(item) )
            else:
                proposals.append( self.create_completion_item(result) )

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
        comp_item.set_label(item.label)

        if item.textEdit:
            if isinstance(item.textEdit, dict):
                comp_item.set_text(item.textEdit["newText"])
            else:
                comp_item.set_text(item.textEdit)
        else:
            comp_item.set_text(item.insertText)

        comp_item.set_icon( self.get_icon_for_type(item.kind) )
        comp_item.set_info(item.documentation)

        return comp_item