# Python imports

# Lib imports

# Application imports



class StylingMixin:
    def tggle_regex(self, widget):
        self.use_regex = not widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def tggle_case_sensitive(self, widget):
        self.use_case_sensitive = widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def tggle_selection_only_scan(self, widget):
        self.search_only_in_selection = widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def tggle_whole_word_search(self, widget):
        self.use_whole_word_search = widget.get_active()
        self._set_find_options_lbl()
        self.search_for_string(self._find_entry)

    def _set_find_options_lbl(self):
        find_options = "Finding with Options: "

        if self.use_regex:
            find_options += "Regex"

        find_options += ", " if self.use_regex else ""
        find_options += "Case Sensitive" if self.use_case_sensitive else "Case Inensitive"

        if self.search_only_in_selection:
            find_options += ", Within Current Selection"

        if self.use_whole_word_search:
            find_options += ", Whole Word"

        self._find_options_lbl.set_label(find_options)

    def update_style(self, state):
        self._find_entry.get_style_context().remove_class("searching")
        self._find_entry.get_style_context().remove_class("search_success")
        self._find_entry.get_style_context().remove_class("search_fail")

        if state == 0:
            self._find_entry.get_style_context().add_class("searching")
        elif state == 1:
            self._find_entry.get_style_context().add_class("search_success")
        elif state == 2:
            self._find_entry.get_style_context().add_class("search_fail")

    def _update_status_lbl(self, total_count: int = 0, query: str = None):
        if not query: return

        count  = total_count if total_count > 0 else "No"
        plural = "s" if total_count > 1 else ""

        if total_count == 0: self.update_style(2)
        self._find_status_lbl.set_label(f"{count} results{plural} found for '{query}'")
