# Renders PRD-Endpoint-Central-Reports.md into hosted-prd.html, the page published
# as an artifact. Requires `pip install markdown`. Run: python3 tools/build-prd-page.py
import re, pathlib, html
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = ROOT / 'PRD-Endpoint-Central-Reports.md'
out = ROOT / 'hosted-prd.html'

text = src.read_text(encoding='utf-8')

# --- split off the front matter: h1, h2 subtitle, meta table -------------------
lines = text.split('\n')
meta_rows = []
i = 0
subtitle = ''
while i < len(lines):
    l = lines[i]
    if l.startswith('## ') and not subtitle:
        subtitle = l[3:].strip()
    if l.startswith('| ') and '|' in l[2:]:
        # collect the first table only
        while i < len(lines) and lines[i].startswith('|'):
            meta_rows.append(lines[i])
            i += 1
        break
    i += 1
body_md = '\n'.join(lines[i:]).lstrip('\n')

meta = []
for r in meta_rows[2:]:
    cells = [c.strip() for c in r.strip().strip('|').split('|')]
    if len(cells) == 2:
        k = re.sub(r'^\*\*(.*)\*\*$', r'\1', cells[0])
        meta.append((k, cells[1]))

md = markdown.Markdown(extensions=['tables', 'fenced_code', 'sane_lists', 'toc'],
                       extension_configs={'toc': {'toc_depth': '2-3'}})
body = md.convert(body_md)

# --- post-process --------------------------------------------------------------
# tables get a scroll container
body = re.sub(r'<table>', '<div class="table-wrap"><table>', body)
body = re.sub(r'</table>', '</table></div>', body)

# blockquote flavours
def quote(m):
    inner = m.group(1)
    plain = re.sub(r'<[^>]+>', '', inner)
    if '⚠' in plain:
        inner = inner.replace('⚠️', '').replace('⚠', '')
        inner = re.sub(r'<strong>Assumption flag\.</strong>\s*', '', inner)
        return '<aside class="note note--flag"><span class="note-tag">Assumption</span>%s</aside>' % inner
    if 'Open decision' in plain:
        inner = re.sub(r'<strong>Open decision \(([^)]+)\):</strong>\s*', '', inner)
        return '<aside class="note note--decision"><span class="note-tag">Open decision · D1</span>%s</aside>' % inner
    return '<blockquote class="pull">%s</blockquote>' % inner
body = re.sub(r'<blockquote>\s*(.*?)\s*</blockquote>', quote, body, flags=re.S)

# requirement ids: a list item that opens with <strong>ID-n</strong>
body = re.sub(r'<li>\s*<strong>([A-Z][A-Z0-9-]{1,10}-\d+)</strong>\s*',
              r'<li class="req"><span class="req-id">\1</span> ', body)

# section numbers in headings become their own element
def head(m):
    tag, attrs, txt = m.group(1), m.group(2), m.group(3)
    nm = re.match(r'((?:\d+\.)*\d+)\.?\s+(.*)$', txt)
    if nm:
        txt = '<span class="sec-num">%s</span>%s' % (nm.group(1), nm.group(2))
    return '<%s%s>%s</%s>' % (tag, attrs, txt, tag)
body = re.sub(r'<(h[23])([^>]*)>(.*?)</\1>', head, body, flags=re.S)

# --- table of contents ----------------------------------------------------------
toc_items = []
for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', body, flags=re.S):
    label = re.sub(r'<[^>]+>', '', m.group(2))
    nm = re.match(r'((?:\d+\.)*\d+)\.?\s*(.*)$', label)
    num, rest = (nm.group(1), nm.group(2)) if nm else ('', label)
    toc_items.append('<li><a href="#%s"><span class="toc-num">%s</span><span>%s</span></a></li>'
                     % (m.group(1), num, rest))
toc = '\n'.join(toc_items)

meta_html = '\n'.join(
    '<div class="meta-row"><dt>%s</dt><dd>%s</dd></div>' % (k, md.reset().convert(v).replace('<p>', '').replace('</p>', ''))
    for k, v in meta)

tpl = (ROOT / 'tools' / 'prd-template.html').read_text(encoding='utf-8')
page = tpl.replace('<!--SUBTITLE-->', html.escape(subtitle)) \
          .replace('<!--META-->', meta_html) \
          .replace('<!--TOC-->', toc) \
          .replace('<!--BODY-->', body)
out.write_text(page, encoding='utf-8')
print('wrote', out, len(page), 'bytes;', len(toc_items), 'toc entries;', len(meta), 'meta rows')
