# Python imports

# Lib imports

# Application imports



class ReplaceMixin:
    def replace(self, widget):
        replace_text = self._replace_entry.get_text()
        if self.find_text and replace_text:
            self._buffer.begin_user_action()

            iter       = self._buffer.get_start_iter()
            search_tag = self._tag_table.lookup(self.search_tag)

            iter.forward_to_tag_toggle(search_tag)
            self._do_replace(iter, replace_text)
            self._active_src_view.scroll_to_iter( iter, 0.0, True, 0.0, 0.0 )

            self._buffer.end_user_action()

    def replace_all(self, widget):
        replace_text = self._replace_entry.get_text()
        if self.find_text:
            self._buffer.begin_user_action()

            mark       = self._buffer.get_insert()
            iter       = self._buffer.get_start_iter()
            search_tag = self._tag_table.lookup(self.search_tag)

            while iter.forward_to_tag_toggle(search_tag):
                self._do_replace(iter, replace_text)
                iter = self._buffer.get_start_iter()

            self._buffer.end_user_action()


    def _do_replace(self, iter, text):
        start, end = self.get_start_end(iter)
        self.replace_in_buffer(start, end, text)

    def replace_in_buffer(self, start, end, text):
        pos_mark = self._buffer.create_mark("find-replace", end, True)
        self._buffer.delete(start, end)
        replace_iter = self._buffer.get_iter_at_mark(pos_mark)
        self._buffer.insert(replace_iter, text)

    def get_start_end(self, iter):
        start = iter.copy()
        end   = None

        while True:
            iter.forward_char()
            tags  = iter.get_tags()
            valid = False
            for tag in tags:
                if tag.props.name and self.search_tag in tag.props.name:
                    valid = True
                    break

            if valid:
                continue

            end = iter.copy()
            break

        return start, end

    # NOTE: Below, lovingly taken from Hamad Al Marri's Gamma text editor.
    # Link: https://gitlab.com/hamadmarri/gamma-text-editor
    def is_whole_word(self, match_start, match_end):
    	is_prev_a_char = True
    	is_next_a_char = True

    	prev_iter = match_start.copy()
    	next_iter = match_end.copy()
    	if not prev_iter.backward_char():
    		is_prev_a_char = False
    	else:
    		c = prev_iter.get_char()
    		is_prev_a_char = (c.isalpha() or c.isdigit())

    	if not next_iter:
    		is_next_a_char = False
    	else:
    		c = next_iter.get_char()
    		is_next_a_char = (c.isalpha() or c.isdigit())

    	is_word = (not is_prev_a_char and not is_next_a_char)

    	# Note: Both must be false to be a word...
    	return is_word
