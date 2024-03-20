# Python imports

# Lib imports

# Application imports



class MarkdownTemplateMixin:
    def wrap_html_to_body(self, html):
        return f"""\
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <title>Markdown View</title>
    <style media="screen">
        html, body {{
            display: block;
            background-color: #32383e00;
            color: #ffffff;
            text-wrap: wrap;
        }}
        
        img {{
            width: 100%;
            height: auto;
        }}
        
        code {{
            border: 1px solid #32383e;
            background-color: #32383e;
            padding: 4px;
        }}
    </style>
</head>
<body>
    {html}
</body>
</html>

"""