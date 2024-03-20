# Python imports

# Lib imports

# Application imports



class RemoveCommentMixin:
	def remove_comment_characters(self, buffer, start_tag, end_tag, start, end):
		smark = buffer.create_mark("start", start, False)
		emark = buffer.create_mark("end", end, False)
		number_lines = end.get_line() - start.get_line() + 1
		iter = start.copy()
		head_iter = iter.copy()
		self.forward_tag(head_iter, start_tag)

		buffer.begin_user_action()

		for i in range(0, number_lines):
			if self.get_tag_position_in_line(start_tag, head_iter, iter):
				dmark = buffer.create_mark("delete", iter, False)
				buffer.delete(iter, head_iter)

				space_iter = head_iter.copy()
				space_iter.forward_char()
				s = head_iter.get_slice(space_iter)
				if s == " ":
					buffer.delete(head_iter, space_iter)

				if end_tag:
					iter = buffer.get_iter_at_mark(dmark)
					head_iter = iter.copy()
					self.forward_tag(head_iter, end_tag)
					if self.get_tag_position_in_line(end_tag, head_iter, iter):
						buffer.delete(iter, head_iter)
				buffer.delete_mark(dmark)

			iter = buffer.get_iter_at_mark(smark)
			iter.forward_line()
			buffer.delete_mark(smark)
			head_iter = iter.copy()
			self.forward_tag(head_iter, start_tag)
			smark = buffer.create_mark("iter", iter, True)

		buffer.end_user_action()

		buffer.delete_mark(smark)
		buffer.delete_mark(emark)
