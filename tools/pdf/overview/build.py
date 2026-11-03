#!/usr/bin/env python3
"""Assemble overview.html from part*.html, scoping each inline <svg><style> to its own svg."""
import glob, os, re
here = os.path.dirname(os.path.abspath(__file__))
parts = sorted(glob.glob(os.path.join(here, 'part*.html')))
body = ''.join(open(p, encoding='utf-8').read() for p in parts)
n = 0
def scope_svg(m):
    global n
    n += 1
    cls = f'sv{n}'
    svg = m.group(0)
    # add class to the opening <svg ...> tag
    open_tag = re.match(r'<svg\b[^>]*>', svg).group(0)
    if 'class="' in open_tag:
        new_open = open_tag.replace('class="', f'class="{cls} ', 1)
    else:
        new_open = open_tag[:-1] + f' class="{cls}">'
    svg = new_open + svg[len(open_tag):]
    def scope_style(sm):
        css = sm.group(1)
        css = re.sub(r'(^|\})\s*([^{}]+?)\s*\{', lambda r: f"{r.group(1)}{', '.join('.'+cls+' '+s.strip() for s in r.group(2).split(','))}{{", css)
        return f'<style>{css}</style>'
    return re.sub(r'<style>(.*?)</style>', scope_style, svg, flags=re.S)
body = re.sub(r'<svg\b.*?</svg>', scope_svg, body, flags=re.S)
html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Bawaba — Visual Design Overview</title>'
        '<link rel="stylesheet" href="base.css"></head><body>' + body + '</body></html>')
open(os.path.join(here, 'overview.html'), 'w', encoding='utf-8').write(html)
print('svgs scoped:', n)
