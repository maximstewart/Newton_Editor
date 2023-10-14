# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject

import jedi
from jedi.api import Script

# Application imports



# FIXME: Find real icon names...
icon_names = {
    'import':    '',
    'module':    '',
    'class':     '',
    'function':  '',
    'statement': '',
    'param':     ''
}


class Jedi:
    def get_script(file, doc_text):
        return Script(code = doc_text, path = file)


class PythonCompletionProvider(GObject.Object, GtkSource.CompletionProvider):
    """
        This code is A python code completion plugin for Newton.
        # NOTE: Some code pulled/referenced from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'PythonProvider'

    def __init__(self, file):
        GObject.Object.__init__(self)
        self._theme = Gtk.IconTheme.get_default()
        self._file  = file

    def do_get_name(self):
        return "Python Code Completion"

    def get_iter_correctly(self, context):
        return context.get_iter()[1] if isinstance(context.get_iter(), tuple) else context.get_iter()

    def do_match(self, context):
        iter = self.get_iter_correctly(context)
        iter.backward_char()

        buffer = iter.get_buffer()
        if buffer.get_context_classes_at_iter(iter) != ['no-spell-check']:
            return False

        ch = iter.get_char()
        # NOTE: Look to re-add or apply supprting logic to use spaces
         # As is it slows down the editor in certain contexts...
        # if not (ch in ('_', '.', ' ') or ch.isalnum()):
        if not (ch in ('_', '.') or ch.isalnum()):
            return False

        return True

    def do_get_priority(self):
        return 1

    def do_get_activation(self):
        return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context):
        # TODO: Maybe convert async?
        it        = self.get_iter_correctly(context)
        buffer    = it.get_buffer()
        proposals = []

        doc_text    = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        iter_cursor = buffer.get_iter_at_mark(buffer.get_insert())
        linenum     = iter_cursor.get_line() + 1
        charnum     = iter_cursor.get_line_index()

        def create_generator():
            for completion in Jedi.get_script(self._file, doc_text).complete(line = linenum, column = None, fuzzy = False):
                comp_item = GtkSource.CompletionItem.new()
                comp_item.set_label(completion.name)
                comp_item.set_text(completion.name)
                comp_item.set_icon(self.get_icon_for_type(completion.type))
                comp_item.set_info(completion.docstring())
                yield comp_item

        for item in create_generator():
            proposals.append(item)

        context.add_proposals(self, proposals, True)

    def get_icon_for_type(self, _type):
        try:
            return self._theme.load_icon(icon_names[_type.lower()], 16, 0)
        except:
            try:
                return self._theme.load_icon(Gtk.STOCK_ADD, 16, 0)
            except:
                return None
