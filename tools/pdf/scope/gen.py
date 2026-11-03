#!/usr/bin/env python3
"""Generate the 'Shamel Pro API - Capabilities & scope' fixed-page HTML from research JSON, then render + auto-fit."""
import html, json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_DATA = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'docs', 'upstream', 'scope-data'))
SC = os.environ.get('SCOPE_DATA') or (_REPO_DATA if os.path.isdir(_REPO_DATA) else os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scope'))
PDFDIR = os.path.dirname(HERE)                                             # scratchpad/pdf
OUT_HTML = os.path.join(HERE, 'scope.html')
FOOT = '<div class="page-foot"><span><b>Shamel Pro API</b> · Capabilities &amp; scope</span><span class="pn"></span></div>'
e = lambda s: html.escape(str(s if s is not None else ''), quote=False)

def load(name):
    p = os.path.join(SC, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None

D1, D2, D3 = load('dict-master-customers.json'), load('dict-items.json'), load('dict-vouchers.json')
EP, UC, LIM = load('endpoints.json'), load('usecases.json'), load('limits.json')
_raw = (D1 or {}).get('entities', []) + (D2 or {}).get('entities', []) + (D3 or {}).get('entities', [])
ENTITIES, _seen = [], {}
for _x in _raw:
    _k = (_x.get('name'), tuple(f.get('name') for f in _x.get('fields', [])))
    if _k in _seen:   # same class printed for several endpoints (e.g. PostResponse): merge endpoint lists
        _t = _seen[_k]
        for _f in ('returned_by', 'accepted_by'):
            _t[_f] = sorted(set((_t.get(_f) or []) + (_x.get(_f) or [])))
        continue
    _seen[_k] = _x; ENTITIES.append(_x)
ENUMS = (D3 or {}).get('enums', [])
N_FIELDS = sum(len(x.get('fields', [])) for x in ENTITIES)
ENDPOINTS = (EP or {}).get('endpoints', [])
MATRIX = (EP or {}).get('matrix', [])
FIT = json.load(open(os.path.join(HERE, 'fit.json'))) if os.path.exists(os.path.join(HERE, 'fit.json')) else {}

def section_head(no, kicker, title, lead=None):
    h = f'<div class="kicker"><span class="section-no">{no}</span>{e(kicker)}</div><h2 class="page-title">{title}</h2>'
    if lead: h += f'<p class="lead">{lead}</p>'
    return h

def cont_head(no, kicker, title):
    return f'<div class="kicker"><span class="section-no">{no}</span>{e(kicker)} · continued</div><h2 class="page-title" style="font-size:16pt">{title}</h2>'

def flow(sec_id, no, kicker, title, lead, blocks, first_cap=205, cap=245, wrap_open='', wrap_close=''):
    """Pack (html, est_mm) blocks into fixed pages. FIT[sec_id] scales estimates after overflow."""
    k = FIT.get(sec_id, 1.0)
    pages, cur, used, capacity = [], [], 0.0, first_cap
    for b, h in blocks:
        h = h * k
        if cur and used + h > capacity:
            pages.append(cur); cur, used, capacity = [], 0.0, cap
        cur.append(b); used += h
    if cur: pages.append(cur)
    out = []
    for i, p in enumerate(pages):
        head = section_head(no, kicker, title, lead) if i == 0 else cont_head(no, kicker, title)
        out.append(f'<section class="page" id="{sec_id}-{i+1}">{head}{wrap_open}{"".join(p)}{wrap_close}{FOOT}</section>')
    return out

def lines(text, chars_per_line):
    return max(1, math.ceil(len(str(text or '')) / max(1, chars_per_line)))

# ------------------------------------------------------------------ glance
def glance():
    t = (EP or {}).get('totals', {})
    reads = sum(1 for x in ENDPOINTS if x.get('kind') in ('read', 'report'))
    writes = sum(1 for x in ENDPOINTS if x.get('kind') == 'write')
    ready = sum(1 for u in (UC or {}).get('usecases', []) if u.get('feasibility') == 'ready')
    partial = sum(1 for u in (UC or {}).get('usecases', []) if u.get('feasibility') == 'partial')
    nuc = len((UC or {}).get('usecases', []))
    can = ['Read all customers (with getAll) with balances, cheque totals, contacts and price rows',
           'Read the full item catalog: up to 6 units and 6 sale-price fields, barcodes, groups, image paths',
           'Read stock per store, item serials and warranty dates',
           'Read vouchers by code or date range, the salesman’s prepared delivery and order status',
           'Run account statements, last-price and cost-center reports',
           'Create customers, items, cost centers and vouchers of all 13 types listed for Post2',
           'Fetch customers and items updated after a date (stock takes the same header; effect unstated)']
    cant = ['Update, cancel or delete anything: only inserts are documented',
            'Page through big lists: no paging is documented; lists come back in one response',
            'Detect changes to vouchers or balances, or deletions, directly',
            'Restrict what an API user sees: no permissions are documented, and getAll lifts salesman scoping',
            'Rely on documented HTTPS, rate limits, token lifetime or versioning']
    contents = [('01', 'At a glance'), ('02', 'How the API works'), ('03', 'The data map'), ('04', 'Capability matrix'),
                ('05', 'Master data'), ('06', 'Customers'), ('07', 'Items, stock & catalog'), ('08', 'Vouchers'),
                ('09', 'Reports & cost centers'), ('10', 'Writing data'), ('11', 'What we can build'),
                ('12', 'Limits & gaps'), ('13', 'How Bawaba fills the gaps'), ('A', 'Endpoint reference'),
                ('B', 'Data dictionary'), ('C', 'Open questions')]
    cl = ''.join(f'<div class="ci2"><span class="cn">{n}</span><span class="ct">{e(tl)}</span></div>' for n, tl in contents)
    return f'''<section class="page" id="glance">
{section_head("01", "At a glance", "A read-heavy API with insert-only writes",
 "The Shamel Pro Web API gives programs broad access to the company’s commercial data: customers, items, stock, prices, vouchers and reports. It can also create new records. The manual documents no way to change or delete them, and its only access control is a Shamel user login plus salesman scoping.")}
<div class="grid g4 mb4">
  <div class="stat"><div class="n">{t.get("endpoints", len(ENDPOINTS))}</div><div class="l">endpoints in the manual</div></div>
  <div class="stat"><div class="n">{reads}</div><div class="l">read endpoints, including 3 reports</div></div>
  <div class="stat"><div class="n">{writes}</div><div class="l">write endpoints (insert only), plus login</div></div>
  <div class="stat"><div class="n">{len(ENTITIES)}<small> / {N_FIELDS}</small></div><div class="l">record types / fields documented</div></div>
</div>
<div class="grid g2 mb4">
  <div class="card teal"><h4>What you can do</h4><ul class="clean ticks small">{"".join(f"<li>{e(x)}</li>" for x in can)}</ul></div>
  <div class="card sand"><h4>What you cannot do (today)</h4><ul class="clean crosses small">{"".join(f"<li>{e(x)}</li>" for x in cant)}</ul></div>
</div>
<div class="callout teal mb4"><div class="ci">★</div><div class="small"><b>{nuc} tool ideas checked against the manual:</b> {ready} are possible with documented endpoints alone, {partial} work with caveats or need an answer from ISCO, and the rest need something the API does not offer. See section 11.</div></div>
<h3>Contents</h3><div class="contents3">{cl}</div>
{FOOT}</section>'''

# ------------------------------------------------------------------ matrix
def trim(t, n):
    t = str(t or "")
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"

def sym(v):
    s = str(v or '').lower()
    if s.startswith('yes'): return '<span class="sym y">✓</span>'
    if s.startswith('partial') or s.startswith('limited'): return '<span class="sym p">◐</span>'
    if s.startswith('no') or s in ('', '-', 'n/a'): return '<span class="sym n">✕</span>'
    return '<span class="sym p">◐</span>'

def matrix():
    rows = ''
    for m in MATRIX:
        rows += (f'<tr><td>{e(m.get("entity"))} <span class="tiny muted" style="font-weight:400;font-family:IBM Plex Sans Arabic">{e(m.get("entity_ar",""))}</span></td>'
                 f'<td>{sym(m.get("list"))}</td><td>{sym(m.get("get_one"))}</td><td>{sym("yes" if m.get("filters") else "no")}</td>'
                 f'<td>{sym(m.get("incremental_sync"))}</td><td>{sym(m.get("create"))}</td><td>{sym(m.get("update"))}</td><td>{sym(m.get("delete"))}</td>'
                 f'<td class="note">{e(trim(", ".join(m.get("filters") or []), 58))}</td></tr>')
    return f'''<section class="page" id="matrix">
{section_head("04", "Capability matrix", "What you can do with each kind of data",
 "✓ supported by a documented endpoint · ◐ partly (with limits or assumptions) · ✕ not documented. “Changed since” means the endpoint accepts lastupdatedate.")}
<table class="mx"><thead><tr><th style="width:24%">Data</th><th>List</th><th>Get one</th><th>Filter</th><th>Changed since</th><th>Create</th><th>Update</th><th>Delete</th><th style="width:26%">Filters</th></tr></thead><tbody>{rows}</tbody></table>
<div class="callout mt2"><div class="ci">!</div><div class="tiny"><b>The pattern:</b> almost everything can be read; four kinds of records can be created; nothing can be updated or deleted through the API. Corrections would have to be made in Shamel itself or with an offsetting voucher, for example a return or credit note (our reading).</div></div>
{FOOT}</section>'''

# ------------------------------------------------------------------ domain pages
DOMAINS = [
 ('master', '05', 'Master data', 'The shared lists every other record refers to', ['master_data'], ['master_data', 'auth'],
  'Currencies and exchange rates, banks and branches, cities, stores, the six price classes and salesmen (response undocumented). Mostly short lookup lists (exchange rates change more often); tools use them to translate codes into names and to fill drop-downs.'),
 ('customers', '06', 'Customers', 'Who you sell to, what they owe, and what they pay', ['customers'], ['customers'],
  'Customer profiles with salesman, price class, credit limit, currency and location; a current balance with unpaid and returned cheque totals, plus a balance list whose rows each carry a currency; classifications, contacts and customer price rows (purpose not described).'),
 ('items', '07', 'Items, stock & catalog', 'What you sell, where it is, and at what price', ['items'], ['items', 'stock'],
  'The item catalog with up to six units and six sale prices per item, barcodes, groups and accounting links; stock quantities per store; serial numbers with warranty dates; and image paths for the catalog.'),
 ('vouchers', '08', 'Vouchers', 'Every commercial document, from order to journal entry', ['vouchers'], ['vouchers'],
  'Vouchers are Shamel’s documents: orders, invoices, returns, deliveries, receipts, payments, notes and journal entries. Each can carry a header, item lines, cheques and account lines. They can be read by code or by date range.'),
 ('reports', '09', 'Reports & cost centers', 'Ready-made summaries computed by Shamel', ['reports', 'cost_centers'], ['reports', 'cost_centers'],
  'Three reports come straight from Shamel: a customer account statement, the last prices of an item, and a cost-center statement. Cost centers can also be created.'),
]

def domain_pages(key, no, kicker, title, ent_domains, ep_domains, lead):
    blocks = []
    eps = [x for x in ENDPOINTS if x.get('domain') in ep_domains and x.get('kind') != 'write']
    if eps:
        rows = ''
        for x in eps:
            ins = ', '.join(i.get('name') for i in x.get('inputs', []) if i.get('name') not in ('username', 'token'))
            rows += (f'<tr><td><code>{e(x.get("path"))}</code></td><td>{e(x.get("purpose"))}</td>'
                     f'<td class="tiny">{e(ins) or "—"}</td><td>{"✓" if x.get("incremental_sync") else ""}</td></tr>')
        est = 14 + sum(max(lines(x.get('purpose'), 48), lines(', '.join(i.get('name') for i in x.get('inputs', [])), 30)) * 4.2 + 2.4 for x in eps)
        blocks.append((f'<h3>Endpoints</h3><table class="t compact" style="font-size:7.6pt"><thead><tr><th style="width:30%">Endpoint</th><th>What it returns</th><th style="width:22%">Inputs &amp; filters</th><th style="width:8%">Sync</th></tr></thead><tbody>{rows}</tbody></table>', est))
    ents = [x for x in ENTITIES if x.get('domain') in ent_domains]
    cards = ''
    est_cards = 10
    for i, x in enumerate(ents):
        fl = ' · '.join(f.get('name') for f in x.get('fields', [])[:18])
        more = len(x.get('fields', [])) - 18
        if more > 0: fl += f' · +{more} more'
        cards += (f'<div class="fg"><h4>{e(x.get("plain_name"))} <span class="tiny muted" style="font-weight:400">· {len(x.get("fields", []))} fields · p. {e(x.get("page",""))}</span></h4>'
                  f'<p style="margin:0 0 1mm;color:var(--ink-2)">{e(x.get("description"))}</p><div class="fl">{e(fl)}</div>'
                  f'<p><b style="color:var(--accent-2)">Use it for:</b> {e(x.get("business_value"))}</p></div>')
    if ents:
        # estimate 2-column card grid height
        hs = [10 + lines(x.get('description'), 52) * 3.6 + lines(' · '.join(f.get('name') for f in x.get('fields', [])[:18]), 46) * 3.6 + lines(x.get('business_value'), 52) * 3.6 for x in ents]
        col = sum(sorted(hs)[::2]) if len(hs) > 1 else sum(hs)
        blocks.append(('<h3 class="mt4">Records</h3><div class="grid g2" style="gap:3mm">', 0))
        for x, h in zip(ents, hs):
            blocks.append((cards_html(x), h / 2 + 1.5))
        blocks.append(('</div>', 0))
    return flow(key, no, kicker, title, lead, fix_grid(blocks))

def cards_html(x):
    fl = ' · '.join(f.get('name') for f in x.get('fields', [])[:18])
    more = len(x.get('fields', [])) - 18
    if more > 0: fl += f' · +{more} more'
    return (f'<div class="fg"><h4>{e(x.get("plain_name"))} <span class="tiny muted" style="font-weight:400">· {len(x.get("fields", []))} fields · p. {e(x.get("page",""))}</span></h4>'
            f'<p style="margin:0 0 1mm;color:var(--ink-2)">{e(x.get("description"))}</p><div class="fl">{e(fl)}</div>'
            f'<p><b style="color:var(--accent-2)">Use it for:</b> {e(x.get("business_value"))}</p></div>')

def fix_grid(blocks):
    """Merge grid open/close markers into each card so page breaks never split a grid wrapper."""
    out, in_grid = [], False
    for b, h in blocks:
        if b.startswith('<h3 class="mt4">Records</h3>'):
            out.append(('<h3 class="mt4">Records</h3>', 8)); in_grid = True; continue
        if b == '</div>' and in_grid: in_grid = False; continue
        if in_grid: out.append(('__CARD__' + b, h)); continue
        out.append((b, h))
    return out

def render_cards_in_pages(pages_html):
    res = []
    for p in pages_html:
        p = re.sub(r'((?:__CARD__<div class="fg">.*?</div></div>|__CARD__<div class="fg">(?:(?!__CARD__).)*?</p></div>)+)',
                   lambda m: '<div class="grid g2" style="gap:3mm">' + m.group(1).replace('__CARD__', '') + '</div>', p, flags=re.S)
        res.append(p.replace('__CARD__', ''))
    return res

# ------------------------------------------------------------------ writes
def writes():
    w = [x for x in ENDPOINTS if x.get('kind') == 'write']
    rows = ''.join(f'<tr><td><code>{e(x.get("path"))}</code></td><td>{e(x.get("purpose"))}</td><td class="tiny">{e(x.get("returns"))}</td></tr>' for x in w)
    vt = next((en for en in ENUMS if en.get('name', '').lower().startswith('vouchertype')), None)
    vrows = ''
    if vt:
        for v in sorted(vt.get('values', []), key=lambda v: v.get('value', 0)):
            vrows += (f'<tr><td>{e(v.get("value"))}</td><td><code>{e(v.get("name"))}</code></td><td>{e(v.get("meaning"))}</td>'
                      f'<td style="font-family:IBM Plex Sans Arabic;direction:rtl;text-align:right">{e(v.get("meaning_ar"))}</td><td style="text-align:center"><code>{e(v.get("code_prefix") or "—")}</code></td></tr>')
    return f'''<section class="page" id="writes">
{section_head("10", "Writing data", "Four ways to create records, none to change them",
 "Writes go through four endpoints. Each takes the new record as a JSON string in the form field obj and answers with Success, an error message and, where documented, the new record’s code. There is no update, cancel or delete, and the manual documents no protection against posting the same document twice.")}
<table class="t compact mb4" style="font-size:7.8pt"><thead><tr><th style="width:26%">Endpoint</th><th>What it creates</th><th style="width:30%">Returns</th></tr></thead><tbody>{rows}</tbody></table>
<h3>The 13 voucher types /Voucher/Post2 can create</h3>
<table class="t compact" style="font-size:7.4pt"><thead><tr><th style="width:8%">Type</th><th style="width:28%">Name in the manual</th><th>Meaning</th><th style="width:24%;text-align:right">Arabic</th><th style="width:10%">Code prefix</th></tr></thead><tbody>{vrows}</tbody></table>
<div class="grid g3 mt2 compact-cards">
  <div class="card soft"><h4>What a voucher carries</h4><p class="tiny muted">A header (type, date, customer, currency and rate, salesman, store, discount, VAT, notes), item lines (item, unit, store, quantity, price, bonus, discount, cost centers), cheques and, for journals, account lines.</p></div>
  <div class="card soft"><h4>Codes</h4><p class="tiny muted">Leave the code empty and Shamel numbers the voucher; send one and it must start with the type’s prefix letter (p. 13, 15–16). Purchase deliveries have no documented prefix.</p></div>
  <div class="card soft"><h4>Mistakes</h4><p class="tiny muted">Because only inserts are documented, a wrong document can only be corrected with an offsetting one (return, credit note, journal) or by hand in Shamel (our reading). Bawaba adds idempotency and an approval queue for this reason.</p></div>
</div>
{FOOT}</section>'''

# ------------------------------------------------------------------ use cases
def usecases():
    ucs = (UC or {}).get('usecases', [])
    order = ['Sales & customers', 'Field sales (salesmen)', 'Stock & items', 'Finance & accounting', 'E-commerce & integrations', 'Management & BI']
    ucs = sorted(ucs, key=lambda u: (order.index(u.get('group')) if u.get('group') in order else 99, u.get('id', '')))
    blocks, last = [], None
    cnt = {k: sum(1 for u in ucs if u.get('feasibility') == k) for k in ('ready', 'partial', 'blocked')}
    blocks.append((f'<div class="grid g3 mb4"><div class="stat"><div class="n" style="color:#23714F">{cnt["ready"]}</div><div class="l">ready: documented endpoints are enough</div></div><div class="stat"><div class="n" style="color:#8A5A1F">{cnt["partial"]}</div><div class="l">partial: works with caveats or an ISCO answer</div></div><div class="stat"><div class="n" style="color:#9B3B27">{cnt["blocked"]}</div><div class="l">blocked: needs something the API lacks</div></div></div>', 26))
    pair = []
    def flush():
        if pair:
            hs = [uc_h(u) for u in pair]
            blocks.append(('<div class="grid g2" style="gap:3mm;margin-bottom:3mm">' + ''.join(uc_html(u) for u in pair) + '</div>', max(hs) + 3))
            pair.clear()
    for u in ucs:
        if u.get('group') != last:
            flush(); blocks.append((f'<h3 class="mt2">{e(u.get("group"))}</h3>', 9)); last = u.get('group')
        pair.append(u)
        if len(pair) == 2: flush()
    flush()
    return flow('uc', '11', 'What we can build', 'Tool ideas, checked against the API',
                'Each idea lists the Shamel endpoints it needs and how feasible it is today, judged from the manual alone. “Milestone” is the Bawaba milestone that enables it (M1 reads, M2 writes and approvals, M3 webhooks).', blocks, first_cap=210)

def uc_h(u):
    return 14 + lines(u.get('description'), 50) * 3.6 + lines(u.get('why'), 56) * 3.3 + lines(' · '.join(u.get('reads', []) + u.get('writes', [])), 52) * 3.0

def uc_html(u):
    eps = ' · '.join(u.get('reads', []) + [f'✎ {w}' for w in u.get('writes', [])])
    isco = (' · ' + ', '.join(u.get('isco', []))) if u.get('isco') else ''
    return (f'<div class="uc"><div class="top"><div><h4>{e(u.get("title"))}<span class="ms">{e(u.get("milestone",""))}</span></h4><div class="arname">{e(u.get("title_ar",""))}</div></div>'
            f'<span class="feas {e(u.get("feasibility"))}">{e(u.get("feasibility"))}</span></div>'
            f'<p>{e(u.get("description"))}</p><div class="why">{e(u.get("why"))}{e(isco)}</div><div class="eps">{e(eps)}</div></div>')

# ------------------------------------------------------------------ limits
def limits():
    ls = (LIM or {}).get('limits', [])
    rank = {'high': 0, 'medium': 1, 'low': 2}
    ls = sorted(ls, key=lambda x: (rank.get(x.get('severity'), 3), x.get('id', '')))
    blocks = [('<div class="legend mb2"><span><i style="border-top:4px solid var(--rose);width:4mm"></i>high</span><span><i style="border-top:4px solid var(--accent);width:4mm"></i>medium</span><span><i style="border-top:4px solid var(--sky);width:4mm"></i>low</span></div>', 7)]
    for x in ls:
        isco = (' (' + ', '.join(x.get('isco', [])) + ')') if x.get('isco') else ''
        b = (f'<div class="lim"><div class="sv {e(x.get("severity"))}"></div><div><h4>{e(x.get("title"))} <span class="tiny muted" style="font-weight:400">· {e(x.get("category"))}{e(isco)}</span></h4>'
             f'<div class="d">{e(x.get("detail"))} <b>Impact:</b> {e(x.get("impact"))}</div><div class="b"><b>Bawaba:</b> {e(x.get("bawaba"))}</div></div></div>')
        h = 9 + lines(x.get('detail', '') + ' Impact: ' + x.get('impact', ''), 118) * 3.5 + lines(x.get('bawaba'), 122) * 3.4
        blocks.append((b, h))
    return flow('lim', '12', 'Limits & gaps', 'What the API does not do, and why it matters',
                'Ordered by severity. Each entry says what it means for the tools we build and whether the Bawaba gateway can work around it.', blocks, first_cap=215)

def short(t, n=170):
    t = str(t or '').strip()
    m = re.match(r'(.+?[.!?])(\s|$)', t)
    t = m.group(1) if m else t
    t = re.sub(r'\s*\((?:0\d|\d\d) ?§[^)]*\)', '', t)
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'

def bawaba_page():
    ls = (LIM or {}).get('limits', [])
    fix = [x for x in ls if x.get('bawaba') and not re.match(r'\s*cannot', x.get('bawaba', ''), re.I)]
    nofix = [x for x in ls if x not in fix]
    blocks = [('<div class="eprow" style="font-weight:700;color:var(--brand);border-bottom:2px solid var(--accent)"><div>Shamel limit</div><div>What Bawaba does about it</div></div>', 8)]
    for x in fix:
        blocks.append((f'<div class="eprow"><div><b>{e(x.get("title"))}</b></div><div>{e(short(x.get("bawaba")))}</div></div>',
                       3 + max(lines(x.get('title'), 34), lines(short(x.get('bawaba')), 84)) * 3.6))
    nf = ''.join(f'<li><b>{e(x.get("title"))}</b>: {e(short(x.get("bawaba"), 120))}</li>' for x in nofix)
    blocks.append((f'<div class="grid g2 mt4"><div class="card sand"><h4>Needs ISCO, not a gateway</h4><ul class="clean small">{nf}</ul></div>'
                   '<div class="card teal"><h4>Where to read more</h4><p class="small muted">Bawaba design: <code>docs/design/</code> and the visual overview PDF. '
                   'Open questions to ISCO: <code>08-isco-questions.md</code> (55 questions, Arabic + English).</p></div></div>', 14 + len(nofix) * 9))
    return flow('baw', '13', 'How Bawaba fills the gaps', 'A gateway can fix a lot, but not everything',
                'Bawaba sits in front of the Shamel API. It cannot add data Shamel does not expose, but it can make the existing API safe, fast and pleasant to build on.', blocks, first_cap=215)

# ------------------------------------------------------------------ appendices
def appendix_endpoints():
    blocks = []
    for x in ENDPOINTS:
        ins = ', '.join(f'{i.get("name")}' + ('' if i.get('where') == 'header' else f' ({i.get("where")})') for i in x.get('inputs', []) if i.get('name') not in ('username', 'token'))
        notes = '; '.join(x.get('notes', [])[:2])
        b = (f'<div class="eprow"><div><code>{e(x.get("path"))}</code><div class="tiny muted">{e(x.get("kind"))} · {e(x.get("method",""))} · p. {e(x.get("page",""))}</div>'
             f'<div class="tiny" style="color:var(--brand-2)">Bawaba: {e(x.get("bawaba_route",""))}</div></div>'
             f'<div><b>{e(x.get("purpose"))}</b><div class="tiny muted">Inputs: {e(ins) or "none besides username/token"} · Returns: {e(x.get("returns"))}{" · supports lastupdatedate" if x.get("incremental_sync") else ""}</div>'
             + (f'<div class="tiny muted" style="margin-top:.4mm">{e(notes)}</div>' if notes else '') + '</div></div>')
        h = 4 + max(3, lines(x.get('purpose'), 80) + lines('Inputs: ' + ins + ' Returns: ' + str(x.get('returns')), 95) + lines(notes, 95)) * 3.3
        blocks.append((b, h))
    return flow('apA', 'A', 'Appendix', 'Endpoint reference: all 30 endpoints', 'Every endpoint in ISCO’s manual with its inputs, return type, page in the manual and the matching Bawaba route.', blocks, first_cap=222)

def appendix_dict():
    blocks = []
    for x in ENTITIES:
        eps = ', '.join((x.get('returned_by') or []) + [f'→ {a}' for a in (x.get('accepted_by') or [])])
        head_html, head_h = (f'<div class="ent-head"><h3>{e(x.get("plain_name"))}</h3><span class="ar" style="font-family:IBM Plex Sans Arabic">{e(x.get("plain_name_ar",""))}</span><code class="tiny">{e(x.get("name"))}</code><span class="eps">{e(eps)} · p. {e(x.get("page",""))}</span></div><p class="ent-desc">{e(x.get("description"))}</p>',
                       9 + lines(x.get('description'), 120) * 3.4)
        fields = x.get('fields', [])
        def row_h(f):
            return 2.4 + max(lines(f.get('meaning'), 30), lines(f.get('note'), 44), 1) * 3.25
        chunks, cur, hcur = [], [], 7.0
        LIMIT = 185.0 / FIT.get('apB', 1.0)
        for f in fields:
            rh = row_h(f)
            if cur and hcur + rh > LIMIT:
                chunks.append((cur, hcur)); cur, hcur = [], 7.0
            cur.append(f); hcur += rh
        if cur: chunks.append((cur, hcur))
        for ci, (chunk, h) in enumerate(chunks):
            rows = ''
            for f in chunk:
                rows += (f'<tr><td class="f">{e(f.get("name"))}</td><td class="t">{e(f.get("type"))}</td><td>{e(f.get("meaning"))}</td>'
                         f'<td><span class="src {e(f.get("source"))}">{e(f.get("source"))}</span></td><td class="n">{e(f.get("note"))}</td></tr>')
            cont = head_html if ci == 0 else f'<div class="tiny muted mb2">{e(x.get("plain_name"))} (continued)</div>'
            blocks.append((cont + f'<table class="dict mb2"><thead><tr><th style="width:19%">Field</th><th style="width:8%">Type</th><th style="width:27%">Meaning</th><th style="width:11%">Source</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table>', h + (head_h if ci == 0 else 4)))
        if not chunks:
            blocks.append((head_html + '<p class="tiny muted mb2">No fields documented.</p>', head_h + 6))
    for en in ENUMS:
        rows = ''.join(f'<tr><td class="f">{e(v.get("value"))}</td><td class="t">{e(v.get("name"))}</td><td>{e(v.get("meaning"))}</td><td style="font-family:IBM Plex Sans Arabic;direction:rtl">{e(v.get("meaning_ar",""))}</td><td class="f">{e(v.get("code_prefix",""))}</td></tr>' for v in en.get('values', []))
        blocks.append((f'<div class="ent-head"><h3>Enumeration: {e(en.get("name"))}</h3><span class="eps">p. {e(en.get("page",""))}</span></div><table class="dict mb2"><thead><tr><th>Value</th><th>Name</th><th>Meaning</th><th>Arabic</th><th>Prefix</th></tr></thead><tbody>{rows}</tbody></table>',
                       12 + len(en.get('values', [])) * 5.0))
    legend = ('<div class="legend mb2"><span><span class="src manual">manual</span> stated in the manual</span><span><span class="src manual-ar">manual-ar</span> from an Arabic comment</span>'
              '<span><span class="src inferred">inferred</span> our reading</span><span><span class="src undocumented">undocumented</span> no meaning given</span></div>')
    blocks.insert(0, (legend, 7))
    return flow('apB', 'B', 'Appendix', 'Data dictionary: every record and field', 'All record types in ISCO’s manual with their fields exactly as printed (including original spellings), what each means, and where that meaning comes from.', blocks, first_cap=220)

def appendix_questions():
    pri = [('ISCO-01', 'Session token lifetime and concurrent sessions per user'), ('ISCO-05', 'HTTPS / TLS support'),
           ('ISCO-18', 'Error format, stable error codes, expired-token signal'), ('ISCO-20', 'Rate and concurrency limits'),
           ('ISCO-21', 'Pagination, truncation and large responses'), ('ISCO-22', 'Meaning of lastupdatedate'),
           ('ISCO-26', 'Response of /Files/GetSalesmen'), ('ISCO-43', 'Duplicate prevention and outcome of failed writes'),
           ('ISCO-50', 'Shamel version, API versioning, change notices'), ('ISCO-53', 'Licensing: internal layer now, commercial use later')]
    rows = ''.join(f'<tr><td><code>{a}</code></td><td>{e(b)}</td></tr>' for a, b in pri)
    return f'''<section class="page" id="apC">
{section_head("C", "Appendix", "Open questions that would widen the scope",
 "The manual leaves gaps that change what we can safely build. 55 questions (Arabic and English) are ready to send to ISCO; these ten matter most.")}
<table class="t compact" style="font-size:8pt"><thead><tr><th style="width:16%">Id</th><th>Topic</th></tr></thead><tbody>{rows}</tbody></table>
<div class="grid g2 mt4">
 <div class="card teal"><h4>Where they are</h4><p class="small muted"><code>docs/design/08-isco-questions.md</code> (full, bilingual, with cover letter) and <code>08-isco-questions-short.md</code> (56 short English questions, copy-paste ready). Every question was checked against this manual.</p></div>
 <div class="card sand"><h4>How answers change this document</h4><p class="small muted">Answers on update endpoints, paging, change feeds, enum values and undocumented fields would move several “partial” and “blocked” tool ideas in section 11 to “ready”.</p></div>
</div>
{FOOT}</section>'''

# ------------------------------------------------------------------ assemble
def build():
    parts = []
    parts.append(open(os.path.join(HERE, 's01-cover.html'), encoding='utf-8').read())
    parts.append(glance())
    parts.append(open(os.path.join(HERE, 's03-how.html'), encoding='utf-8').read())
    parts.append(open(os.path.join(HERE, 's04-map.html'), encoding='utf-8').read()
                 .replace('{{N_ENTITIES}}', str(len(ENTITIES))).replace('{{N_FIELDS}}', str(N_FIELDS)))
    parts.append(matrix())
    for d in DOMAINS:
        parts.extend(render_cards_in_pages(domain_pages(*d)))
    parts.append(writes())
    parts.extend(usecases())
    parts.extend(limits())
    parts.extend(bawaba_page())
    parts.extend(appendix_endpoints())
    parts.extend(appendix_dict())
    parts.append(appendix_questions())
    body = ''.join(parts)
    # scope inline svg <style> blocks per svg
    n = [0]
    def scope_svg(m):
        n[0] += 1; cls = f'sv{n[0]}'; svg = m.group(0)
        ot = re.match(r'<svg\b[^>]*>', svg).group(0)
        nt = ot.replace('class="', f'class="{cls} ', 1) if 'class="' in ot else ot[:-1] + f' class="{cls}">'
        svg = nt + svg[len(ot):]
        return re.sub(r'<style>(.*?)</style>', lambda sm: '<style>' + re.sub(r'(^|\})\s*([^{}]+?)\s*\{', lambda r: f"{r.group(1)}{', '.join('.'+cls+' '+s.strip() for s in r.group(2).split(','))}{{", sm.group(1)) + '</style>', svg, flags=re.S)
    body = re.sub(r'<svg\b.*?</svg>', scope_svg, body, flags=re.S)
    doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Shamel Pro API — Capabilities &amp; Scope</title>'
           '<link rel="stylesheet" href="base.css"></head><body>' + body + '</body></html>')
    open(OUT_HTML, 'w', encoding='utf-8').write(doc)
    return doc.count('<section class="page')

if __name__ == '__main__':
    print('pages:', build(), 'entities:', len(ENTITIES), 'fields:', N_FIELDS, 'endpoints:', len(ENDPOINTS))
