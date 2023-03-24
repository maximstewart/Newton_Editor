# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject

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
    def get_script(file, buffer):
        doc_text    = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        iter_cursor = buffer.get_iter_at_mark(buffer.get_insert())
        linenum     = iter_cursor.get_line() + 1
        charnum     = iter_cursor.get_line_index()
        return Script(code = doc_text, path = file)


class GediCompletionProvider(GObject.Object, GtkSource.CompletionProvider):
    """
        This code is A python code completion plugin for Gedit that's been modified accordingly to work for Newton.
        # NOTE: Code pulled from here --> https://github.com/isamert/gedi
    """
    __gtype_name__ = 'GediProvider'

    def __init__(self, file):
        GObject.Object.__init__(self)
        self._theme = Gtk.IconTheme.get_default()
        self._file  = file

    def do_get_name(self):
        return _("Gedi Python Code Completion")

    def get_iter_correctly(self, context):
        if isinstance(context.get_iter(), tuple):
            return context.get_iter()[1];
        else:
            return context.get_iter()

    def do_match(self, context):
        iter = self.get_iter_correctly(context)
        iter.backward_char()
        buffer = iter.get_buffer()
        if buffer.get_context_classes_at_iter(iter) != ['no-spell-check']:
            return False
        ch = iter.get_char()
        if not (ch in ('_', '.') or ch.isalnum()):
            return False

        return True

    def do_get_priority(self):
        return 1

    def do_get_activation(self):
        return GtkSource.CompletionActivation.INTERACTIVE

    def do_populate(self, context):
        # TODO: Convert async maybe?
        it = self.get_iter_correctly(context)
        document  = it.get_buffer()
        proposals = []

        # for completion in Jedi.get_script(document).completions():
        for completion in Jedi.get_script(self._file, document).complete():
            complete = completion.name
            doc      = completion.doc if jedi.__version__ <= (0,7,0) else completion.docstring()

            proposals.append(GtkSource.CompletionItem.new(completion.name,
                                                            completion.name,
                                                            self.get_icon_for_type(completion.type),
                                                            doc))

        context.add_proposals(self, proposals, True)

    def get_icon_for_type(self, _type):
        try:
            return self._theme.load_icon(icon_names[_type.lower()], 16, 0)
        except:
            try:
                return self._theme.load_icon(Gtk.STOCK_ADD, 16, 0)
            except:
                return None
