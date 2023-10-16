# Python imports

# Lib imports

# Application imports



class CodeCommentTags:
	def get_comment_tags(self, lang):
		(s, e) = self.get_line_comment_tags(lang)
		if (s, e) == (None, None):
			(s, e) = self.get_block_comment_tags(lang)

		return (s, e)

	def get_block_comment_tags(self, lang):
        start_tag = lang.get_metadata('block-comment-start')
        end_tag = lang.get_metadata('block-comment-end')
        if start_tag and end_tag:
            return (start_tag, end_tag)

        return (None, None)

    def get_line_comment_tags(self, lang):
        start_tag = lang.get_metadata('line-comment-start')
        if start_tag:
            return (start_tag, None)

        return (None, None)
