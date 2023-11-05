# Python imports
import os

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import WebKit2

# Application imports
from . import markdown
from .markdown_template_mixin import MarkdownTemplateMixin
from plugins.plugin_base import PluginBase



class Plugin(MarkdownTemplateMixin, PluginBase):
    def __init__(self):
        super().__init__()

        self.name               = "Markdown Preview"  # NOTE: Need to remove after establishing private bidirectional 1-1 message bus
                                                      #       where self.name should not be needed for message comms
        self.path               = os.path.dirname(os.path.realpath(__file__))
        self._GLADE_FILE        = f"{self.path}/markdown_preview.glade"
        
        self.is_preview_paused  = False
        self.is_md_file         = False


    def run(self):
        WebKit2.WebView()       # Need one initialized for webview to work from glade file

        self._builder = Gtk.Builder()
        self._builder.add_from_file(self._GLADE_FILE)
        self._connect_builder_signals(self, self._builder)

        separator_right         = self._ui_objects[0]
        self._markdown_dialog   = self._builder.get_object("markdown_preview_dialog")
        self._markdown_view     = self._builder.get_object("markdown_view")
        self._web_view_settings = self._builder.get_object("web_view_settings")

        self._markdown_dialog.set_relative_to(separator_right)
        self._markdown_view.set_settings(self._web_view_settings)
        self._markdown_view.set_background_color(Gdk.RGBA(0, 0, 0, 0.0))


    def generate_reference_ui_element(self):
        ...

    def subscribe_to_events(self):
        self._event_system.subscribe("tggle_markdown_preview", self._tggle_markdown_preview)
        self._event_system.subscribe("set_active_src_view", self._set_active_src_view)
        self._event_system.subscribe("buffer_changed", self._do_markdown_translate)

    def _buffer_changed_first_load(self, buffer):
        self._buffer = buffer

        self._do_markdown_translate(buffer)

    def _set_active_src_view(self, source_view):
        self._active_src_view = source_view
        self._buffer          = self._active_src_view.get_buffer()

        self._do_markdown_translate(self._buffer)

    def _handle_settings(self, widget = None, eve = None):
        ...

    def _tggle_preview_updates(self, widget = None, eve = None):
        self.is_preview_paused = not self.is_preview_paused
        widget.set_active(self.is_preview_paused)

        if not self.is_preview_paused:
            self._do_markdown_translate(self._buffer)

    def _tggle_markdown_preview(self, widget = None, eve = None):
        if not self._active_src_view: return

        is_visible = self._markdown_dialog.is_visible()
        buffer     = self._active_src_view.get_buffer()
        data       = None

        if not is_visible:
            self._markdown_dialog.popup();
            self._do_markdown_translate(buffer)
        elif not data and is_visible:
            self._markdown_dialog.popdown()

    def _do_markdown_translate(self, buffer):
        if self.is_preview_paused: return

        self.is_markdown_check()
        is_visible = self._markdown_dialog.is_visible()
        if not is_visible or not self.is_md_file: return
        self.render_markdown(buffer)

    def render_markdown(self, buffer):
        start_iter = buffer.get_start_iter()
        end_iter   = buffer.get_end_iter()
        text       = buffer.get_text(start_iter, end_iter, include_hidden_chars = False)
        html       = markdown.markdown(text)

        path       = self._active_src_view.get_current_filepath().get_parent().get_path()
        data       = self.wrap_html_to_body(html)
        self._markdown_view.load_html(content = data, base_uri = f"file://{path}/")
    
    def is_markdown_check(self):
        self.is_md_file = self._active_src_view.get_filetype() == "markdown"
        if not self.is_md_file:
            data = self.wrap_html_to_body("<h1>Not a Markdown file...</h1>")
            self._markdown_view.load_html(content = data, base_uri = None)