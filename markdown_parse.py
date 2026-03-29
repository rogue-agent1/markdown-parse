#!/usr/bin/env python3
"""Markdown parser to HTML. Zero dependencies."""
import re, sys

def to_html(md):
    lines = md.split("\n")
    html = []; in_code = False; in_list = False; in_ol = False; buf = []
    for line in lines:
        if line.startswith("```"):
            if in_code:
                html.append("</code></pre>"); in_code = False
            else:
                lang = line[3:].strip()
                html.append(f'<pre><code class="{lang}">' if lang else "<pre><code>"); in_code = True
            continue
        if in_code:
            html.append(_escape(line)); continue
        stripped = line.strip()
        if not stripped:
            if in_list: html.append("</ul>"); in_list = False
            if in_ol: html.append("</ol>"); in_ol = False
            html.append(""); continue
        # Headers
        m = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if m:
            n = len(m.group(1))
            html.append(f"<h{n}>{_inline(m.group(2))}</h{n}>"); continue
        # HR
        if re.match(r"^[-*_]{3,}$", stripped):
            html.append("<hr>"); continue
        # Unordered list
        m = re.match(r"^[-*+]\s+(.*)", stripped)
        if m:
            if not in_list: html.append("<ul>"); in_list = True
            html.append(f"<li>{_inline(m.group(1))}</li>"); continue
        # Ordered list
        m = re.match(r"^\d+\.\s+(.*)", stripped)
        if m:
            if not in_ol: html.append("<ol>"); in_ol = True
            html.append(f"<li>{_inline(m.group(1))}</li>"); continue
        # Blockquote
        if stripped.startswith("> "):
            html.append(f"<blockquote>{_inline(stripped[2:])}</blockquote>"); continue
        # Paragraph
        html.append(f"<p>{_inline(stripped)}</p>")
    if in_list: html.append("</ul>")
    if in_ol: html.append("</ol>")
    if in_code: html.append("</code></pre>")
    return "\n".join(html)

def _escape(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def _inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[(.+?)\]\((.+?)\)", r'<img src="\2" alt="\1">', s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s

if __name__ == "__main__":
    text = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    print(to_html(text))
