#!/usr/bin/env python3
"""markdown_parse - Markdown to HTML converter."""
import sys, re

def markdown_to_html(text):
    lines = text.split("\n")
    html = []
    in_code = False
    in_list = False
    for line in lines:
        if line.startswith("```"):
            if in_code:
                html.append("</code></pre>")
            else:
                html.append("<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            html.append(_escape(line))
            continue
        if re.match(r"^#{1,6} ", line):
            level = len(line.split(" ")[0])
            content = line[level + 1:]
            html.append(f"<h{level}>{_inline(content)}</h{level}>")
            continue
        if line.startswith("- ") or line.startswith("* "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{_inline(line[2:])}</li>")
            continue
        if in_list:
            html.append("</ul>")
            in_list = False
        if line.startswith("> "):
            html.append(f"<blockquote>{_inline(line[2:])}</blockquote>")
        elif line.startswith("---") or line.startswith("***"):
            html.append("<hr/>")
        elif line.strip():
            html.append(f"<p>{_inline(line)}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)

def _escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img alt="\1" src="\2"/>', text)
    return text

def test():
    assert "<h1>Hello</h1>" in markdown_to_html("# Hello")
    assert "<h3>Sub</h3>" in markdown_to_html("### Sub")
    r = markdown_to_html("**bold** and *italic*")
    assert "<strong>bold</strong>" in r
    assert "<em>italic</em>" in r
    r2 = markdown_to_html("`code`")
    assert "<code>code</code>" in r2
    r3 = markdown_to_html("[link](http://example.com)")
    assert '<a href="http://example.com">link</a>' in r3
    r4 = markdown_to_html("- item1\n- item2")
    assert "<ul>" in r4
    assert "<li>item1</li>" in r4
    r5 = markdown_to_html("> quote")
    assert "<blockquote>quote</blockquote>" in r5
    r6 = markdown_to_html("---")
    assert "<hr/>" in r6
    r7 = markdown_to_html("```\ncode here\n```")
    assert "<pre><code>" in r7
    assert "code here" in r7
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("markdown_parse: Markdown converter. Use --test")
