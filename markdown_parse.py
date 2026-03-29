#!/usr/bin/env python3
"""markdown_parse - Markdown to HTML converter."""
import sys, re

def md_to_html(text):
    lines = text.split("\n"); html = []; in_code = False
    for line in lines:
        if line.startswith("```"):
            html.append("</code></pre>" if in_code else "<pre><code>"); in_code = not in_code; continue
        if in_code: html.append(line); continue
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m: n = len(m.group(1)); html.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); continue
        if re.match(r'^[-*_]{3,}\s*$', line): html.append("<hr>"); continue
        m = re.match(r'^[-*+]\s+(.*)', line)
        if m: html.append(f"<li>{inline(m.group(1))}</li>"); continue
        m = re.match(r'^>\s?(.*)', line)
        if m: html.append(f"<blockquote>{inline(m.group(1))}</blockquote>"); continue
        if line.strip(): html.append(f"<p>{inline(line)}</p>")
    return "\n".join(html)

def inline(t):
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t

def main():
    md = "# Hello\n\nThis is **bold** and *italic*.\n\n- Item one\n- Item [two](url)\n\n> Quote\n\n---\n\n```\ncode here\n```"
    print("Markdown parser demo\n")
    print(md_to_html(md))

if __name__ == "__main__":
    main()
