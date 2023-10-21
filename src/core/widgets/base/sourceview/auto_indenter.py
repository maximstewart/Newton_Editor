# Python imports

# Lib imports
import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource

# Application imports



# NOTE: GtkSource 5 allows for smart indent action by allowing us to override the default auto indent logic...
#  In the long run this will be better because we can check not only for :, ;, { or other things but apply per language such as bash where
#  there isn't a special char but words...
# class AutoIndenter(GtkSource.Indenter):
#     def __init__(self):
#         ...
#
#     def indent(self, view, iter):
#         ...
#
#     def is_trigger(self, view, iter, modifier, keyval):
#         print(iter.get_char())
