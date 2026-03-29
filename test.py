from markdown_parse import to_html
h = to_html("# Hello\n\nThis is **bold** and *italic*.\n\n- item1\n- item2")
assert "<h1>Hello</h1>" in h
assert "<strong>bold</strong>" in h
assert "<em>italic</em>" in h
assert "<li>item1</li>" in h
print("Markdown tests passed")