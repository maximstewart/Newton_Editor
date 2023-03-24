# Python imports
import re

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import GObject

# Application imports



class ExampleCompletionProvider(GObject.GObject, GtkSource.CompletionProvider):
    """
        This is a custom Completion Example Provider.
        # NOTE: used information from here --> https://warroom.rsmus.com/do-that-auto-complete/
    """
    __gtype_name__ = 'CustomProvider'

    def __init__(self):
        GObject.Object.__init__(self)

    def do_get_name(self):
        """ Returns: a new string containing the name of the provider. """
        return _('ExampleProvider')

    def do_match(self, context):
        """ Get whether the provider match the context of completion detailed in context. """
        # NOTE: True for debugging but context needs to normally get checked for actual usage needs.
        # TODO: Fix me
        return True

    def do_populate(self, context):
        """
            In this instance, it will do 2 things:
                1) always provide Hello World! (Not ideal but an option so its in the example)
                2) Utilizes the Gtk.TextIter from the TextBuffer to determine if there is a jinja
                    example of '{{ custom.' if so it will provide you with the options of foo and bar.
            If selected it will insert foo }} or bar }}, completing your syntax...

            PLEASE NOTE the GtkTextIter Logic and regex are really rough and should be adjusted and tuned
        """

        proposals = [
            # GtkSource.CompletionItem(label='Hello World!', text = 'Hello World!', icon = None, info = None) # NOTE: Always proposed...
        ]

        # Gtk Versions differ on get_iter responses...
        end_iter = context.get_iter()
        if not isinstance(end_iter, Gtk.TextIter):
            _, end_iter = context.get_iter()

        if end_iter:
            buf = end_iter.get_buffer()
            mov_iter = end_iter.copy()
            if mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY):
                mov_iter, _ = mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY)
                left_text = buf.get_text(mov_iter, end_iter, True)
            else:
                left_text = ''

            if re.match(r'.*\{\{\s*custom\.$', left_text):
                proposals.append(
                    GtkSource.CompletionItem(label='foo', text='foo }}')  # optionally proposed based on left search via regex
                )
                proposals.append(
                    GtkSource.CompletionItem(label='bar', text='bar }}')  # optionally proposed based on left search via regex
                )

        context.add_proposals(self, proposals, True)