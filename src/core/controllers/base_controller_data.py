# Python imports
import os
import subprocess

# Lib imports

# Application imports
from plugins.plugins_controller import PluginsController




class BaseControllerData:
    ''' BaseControllerData contains most of the state of the app at ay given time. It also has some support methods. '''

    def setup_controller_data(self) -> None:
        self.window      = settings_manager.get_main_window()
        self.builder     = None
        self.core_widget = None
        self.was_midified_key = False
        self.ctrl_down   = False
        self.shift_down  = False
        self.alt_down    = False
        self.active_src_view = None

        self.load_glade_file()
        self.plugins     = PluginsController()

    def set_active_src_view(self, source_view):
        if self.active_src_view:
            old_notebook = self.active_src_view.get_parent().get_parent()
            old_notebook.is_editor_focused = False

            ctx = old_notebook.get_style_context()
            ctx.remove_class("notebook-selected-focus")

        notebook = source_view.get_parent().get_parent()
        ctx = notebook.get_style_context()
        ctx.add_class("notebook-selected-focus")
        
        file = source_view.get_current_file()
        if file:
            source_view.set_bottom_labels(file)
        else:
            event_system.emit("set_bottom_labels")

        self.active_src_view = source_view

    def get_active_src_view(self):
        return self.active_src_view


    def clear_console(self) -> None:
        ''' Clears the terminal screen. '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def call_method(self, _method_name: str, data: type) -> type:
        '''
        Calls a method from scope of class.

                Parameters:
                        a (obj): self
                        b (str): method name to be called
                        c (*): Data (if any) to be passed to the method.
                                Note: It must be structured according to the given methods requirements.

                Returns:
                        Return data is that which the calling method gives.
        '''
        method_name = str(_method_name)
        method      = getattr(self, method_name, lambda data: f"No valid key passed...\nkey={method_name}\nargs={data}")
        return method(*data) if data else method()

    def has_method(self, obj: type, method: type) -> type:
        ''' Checks if a given method exists. '''
        return callable(getattr(obj, method, None))

    def clear_children(self, widget: type) -> None:
        ''' Clear children of a gtk widget. '''
        for child in widget.get_children():
            widget.remove(child)

    def get_clipboard_data(self, encoding="utf-8") -> str:
        proc    = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        retcode = proc.wait()
        data    = proc.stdout.read()
        return data.decode(encoding).strip()

    def set_clipboard_data(self, data: type, encoding="utf-8") -> None:
        proc = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        proc.stdin.write(data.encode(encoding))
        proc.stdin.close()
        retcode = proc.wait()