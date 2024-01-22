# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Application imports
from ..tab_header_widget import TabHeaderWidget



class TabBar(Gtk.Notebook):
    def __init__(self, index):
        super(TabBar, self).__init__()

        self.INDEX     = index
        self.added_tab = None

        self.set_group_name("editor_widget")

        self._setup_styling()
        self._setup_signals()
        self._subscribe_to_events()
        self._load_widgets()

        self.show_all()


    def _setup_styling(self):
        ...

    def _setup_signals(self):
        self.connect("switch-page",  self._switch_page_update)

    def _subscribe_to_events(self):
        event_system.subscribe(f"add_tab_{self.INDEX}",    self.add_tab)
        event_system.subscribe(f"add_tab_with_name_{self.INDEX}", self.add_tab)
        event_system.subscribe(f"update_tab_{self.INDEX}", self.update_tab)
        event_system.subscribe(f"close_tab_{self.INDEX}",  self.close_tab)

    def _load_widgets(self):
        start_box = Gtk.Box()
        end_box   = Gtk.Box()

        add_tab   = Gtk.Button(label = "+")
        add_tab.connect("released", self._button_add_tab)

        end_box.add(add_tab)

        start_box.show_all()
        end_box.show_all()

        self.set_action_widget(start_box, 0)
        self.set_action_widget(end_box, 1)

    def _button_add_tab(self, widget):
        event_system.emit(f"new_session_{self.INDEX}")

    def _button_close_tab(self, widget, container):
        self._close_tab(widget, container)
        event_system.emit(f"remove_session_{self.INDEX}", (container.fhash))

    # Note: Need to get parent instead given we pass the close_tab method
    #       from a potentially former notebook.
    def _close_tab(self, widget, container):
        notebook = container.get_parent()

        if notebook.get_n_pages() < 2: return

        page_num = notebook.page_num(container)
        notebook.remove_page(page_num)
        # container._cancel_current_file_watchers()

    def _switch_page_update(self, notebook, container, page_num):
        if self.added_tab or self.added_tab == None:
            self.added_tab = False
            return

        event_system.emit(f"switch_session_{self.INDEX}", (container.fhash,))


    def add_tab(self, fhash, title = "[BAD TITLE]"):
        container       = Gtk.EventBox()
        header          = TabHeaderWidget(container, self._button_close_tab)
        page_num        = self.append_page(container, header)

        container.fhash = fhash
        self.added_tab  = True

        header.label.set_label(title)
        self.set_tab_detachable(container, True)
        self.set_tab_reorderable(container, True)

        self.show_all()
        self.set_current_page(page_num)

    def update_tab(self, fhash, title = "[BAD TITLE]"):
        # container = Gtk.EventBox()
        # header    = TabHeaderWidget(container, self._close_tab)
        # page_num  = self.append_page(container, header)

        # header.label.set_label(title)
        # self.set_tab_detachable(container, True)
        # self.set_tab_reorderable(container, True)

        # self.show_all()
        # self.set_current_page(page_num)
        ...

    def close_tab(self, fhash):
        target = None
        for child in self.get_children():
            if child.fhash == fhash:
                target = child
                break

        self._close_tab(None, target)