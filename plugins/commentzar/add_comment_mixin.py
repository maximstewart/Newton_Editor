# Python imports

# Lib imports

# Application imports



class AddCommentMixin:
    def add_comment_characters(self, document, start_tag, end_tag, start, end, deselect, oldPos):
        smark = document.create_mark("start", start, False)
        imark = document.create_mark("iter", start, False)
        emark = document.create_mark("end", end, False)
        number_lines = end.get_line() - start.get_line() + 1
        comment_pos_iter = None
        count = 0

        document.begin_user_action()

        for i in range(0, number_lines):
            iter = document.get_iter_at_mark(imark)

            if not comment_pos_iter:
                (comment_pos_iter, count) = self.discard_white_spaces(iter)

                if self.is_commented(comment_pos_iter, start_tag):
                    new_code = self.remove_comment_characters(document, start_tag, end_tag, start, end)
                    return
            else:
                comment_pos_iter = iter
                for i in range(count):
                    c = iter.get_char()
                    if not c in (" ", "\t"):
                        break

                    iter.forward_char()

            document.insert(comment_pos_iter, start_tag)
            document.insert(comment_pos_iter, " ")

            if end_tag:
                if i != number_lines -1:
                    iter = document.get_iter_at_mark(imark)
                    iter.forward_to_line_end()
                    document.insert(iter, end_tag)
                else:
                    iter = document.get_iter_at_mark(emark)
                    document.insert(iter, end_tag)

            iter = document.get_iter_at_mark(imark)
            iter.forward_line()
            document.delete_mark(imark)
            imark = document.create_mark("iter", iter, True)

        document.end_user_action()

        document.delete_mark(imark)
        new_start = document.get_iter_at_mark(smark)
        new_end = document.get_iter_at_mark(emark)

        document.select_range(new_start, new_end)
        document.delete_mark(smark)
        document.delete_mark(emark)

        if deselect:
            oldPosIter = document.get_iter_at_offset(oldPos + 2)
            document.place_cursor(oldPosIter)
