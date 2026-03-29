#!/usr/bin/env python3
"""markdown_parse: Minimal Markdown to HTML converter."""
import re, sys

def convert(text):
    lines = text.split("\n")
    html = []
    in_list = False
    in_code = False
    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                html.append("</code></pre>"); in_code = False
            else:
                html.append("<pre><code>"); in_code = True
            continue
        if in_code:
            html.append(line); continue
        # Close list if needed
        if in_list and not line.strip().startswith(("- ", "* ", "1.")):
            html.append("</ul>"); in_list = False
        # Headers
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            html.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue
        # Horizontal rule
        if re.match(r"^[-*_]{3,}$", line.strip()):
            html.append("<hr>"); continue
        # Unordered list
        m = re.match(r"^\s*[-*]\s+(.+)$", line)
        if m:
            if not in_list:
                html.append("<ul>"); in_list = True
            html.append(f"<li>{inline(m.group(1))}</li>")
            continue
        # Blockquote
        m = re.match(r"^>\s*(.*)$", line)
        if m:
            html.append(f"<blockquote>{inline(m.group(1))}</blockquote>")
            continue
        # Paragraph
        if line.strip():
            html.append(f"<p>{inline(line)}</p>")
    if in_list: html.append("</ul>")
    if in_code: html.append("</code></pre>")
    return "\n".join(html)

def inline(text):
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    # Code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Links
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    # Images
    text = re.sub(r"!\[(.+?)\]\((.+?)\)", r'<img src="\2" alt="\1">', text)
    return text

def test():
    assert "<h1>Hello</h1>" in convert("# Hello")
    assert "<h2>World</h2>" in convert("## World")
    assert "<strong>bold</strong>" in convert("**bold**")
    assert "<em>italic</em>" in convert("*italic*")
    assert "<code>code</code>" in convert("`code`")
    assert '<a href="http://x">link</a>' in convert("[link](http://x)")
    # Lists
    md = "- item1\n- item2"
    html = convert(md)
    assert "<ul>" in html
    assert "<li>item1</li>" in html
    # Code block
    md2 = "```\nprint('hi')\n```"
    html2 = convert(md2)
    assert "<pre><code>" in html2
    assert "print('hi')" in html2
    # HR
    assert "<hr>" in convert("---")
    # Blockquote
    assert "<blockquote>" in convert("> quote")
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: markdown_parse.py test")
