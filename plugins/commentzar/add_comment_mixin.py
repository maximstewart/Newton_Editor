# Python imports

# Lib imports

# Application imports



class AddCommentMixin:
    def add_comment_characters(self, buffer, start_tag, end_tag, start, end, deselect, oldPos):
        smark = buffer.create_mark("start", start, False)
        imark = buffer.create_mark("iter", start, False)
        emark = buffer.create_mark("end", end, False)
        number_lines = end.get_line() - start.get_line() + 1
        comment_pos_iter = None
        count = 0

        buffer.begin_user_action()

        for i in range(0, number_lines):
            iter = buffer.get_iter_at_mark(imark)
            if not comment_pos_iter:
                (comment_pos_iter, count) = self.discard_white_spaces(iter)

                if self.is_commented(comment_pos_iter, start_tag):
                    new_code = self.remove_comment_characters(buffer, start_tag, end_tag, start, end)
                    return
            else:
                comment_pos_iter = iter
                for i in range(count):
                    c = iter.get_char()
                    if not c in (" ", "\t"):
                        break

                    iter.forward_char()

            buffer.insert(comment_pos_iter, start_tag)
            buffer.insert(comment_pos_iter, " ")

            if end_tag:
                if i != number_lines -1:
                    iter = buffer.get_iter_at_mark(imark)
                    iter.forward_to_line_end()
                    buffer.insert(iter, end_tag)
                else:
                    iter = buffer.get_iter_at_mark(emark)
                    buffer.insert(iter, end_tag)

            iter = buffer.get_iter_at_mark(imark)
            iter.forward_line()
            buffer.delete_mark(imark)
            imark = buffer.create_mark("iter", iter, True)

        buffer.end_user_action()

        buffer.delete_mark(imark)
        new_start = buffer.get_iter_at_mark(smark)
        new_end = buffer.get_iter_at_mark(emark)

        buffer.select_range(new_start, new_end)
        buffer.delete_mark(smark)
        buffer.delete_mark(emark)

        if deselect:
            oldPosIter = buffer.get_iter_at_offset(oldPos + 2)
            buffer.place_cursor(oldPosIter)
