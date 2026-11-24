"""Convert the manuscript's own LaTeX sources into a JSON document model for the Word builder.

This is not a general LaTeX converter: it handles exactly the constructs used in
main.tex / supplement.tex (sections, paragraphs, natbib citations, cross-references,
inline math, a few display equations, proposition/proof/remark, generated tables,
figures and the back matter). Numbers come from numbers.tex, so the Word and LaTeX
versions cannot disagree.

Usage: python latex_to_json.py <manuscript dir> <main|supplement> <out.json>
"""
import json
import re
import sys
from pathlib import Path

MS, WHICH, OUTFILE = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])

MACROS = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{(.*)\}\s*$', (MS / 'numbers.tex').read_text(encoding='utf-8'), flags=re.M))
MACROS['QWKF'] = 'QWK-floor'


# ------------------------------------------------------------------ bibliography
def parse_bib(text):
    entries = {}
    for m in re.finditer(r'@(\w+)\{([^,]+),(.*?)\n\}', text, flags=re.S):
        typ, key, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        fields = {}
        for f in re.finditer(r'(\w+)\s*=\s*\{', body):
            depth, j = 1, f.end()
            while depth:
                depth += {'{': 1, '}': -1}.get(body[j], 0)
                j += 1
            fields[f.group(1).lower()] = body[f.end():j - 1]
        fields['_type'] = typ
        entries[key] = fields
    return entries


def tex_accents(s):
    rep = {r"{\'i}": 'í', r"{\'a}": 'á', r"{\'e}": 'é', r"{\'o}": 'ó', r"{\'E}": 'É', r'{\v{s}}': 'š', r'{\u{a}}': 'ă',
           r'{\"e}': 'ë', r"\'i": 'í', r"\'a": 'á', r"\'e": 'é', r"\'o": 'ó', r'\&': '&'}
    for a, b in rep.items():
        s = s.replace(a, b)
    return s.replace('{', '').replace('}', '')


def authors_of(e):
    out = []
    for a in e.get('author', '').split(' and '):
        a = tex_accents(a.strip())
        if ',' in a:
            last, first = [x.strip() for x in a.split(',', 1)]
        else:
            last, first = a, ''
        out.append((last, first))
    return out


BIB = parse_bib((MS / 'refs.bib').read_text(encoding='utf-8'))


def cite_name(key):
    au = authors_of(BIB[key])
    if len(au) == 1:
        return au[0][0]
    if len(au) == 2:
        return f'{au[0][0]} and {au[1][0]}'
    return f'{au[0][0]} et al.'


def cite_year(key):
    return BIB[key]['year']


CITED = []


def cite(kind, pre, post, keys):
    keys = [k.strip() for k in keys.split(',')]
    for k in keys:
        if k not in BIB:
            raise KeyError('Unknown citation ' + k)
        if k not in CITED:
            CITED.append(k)
    if kind == 'citet':
        return '; '.join(f'{cite_name(k)} ({cite_year(k)})' for k in keys)
    body = '; '.join(f'{cite_name(k)} {cite_year(k)}' for k in keys)
    if pre:
        body = pre + ' ' + body
    if post:
        body = body + ', ' + post
    return body if kind == 'citealp' else f'({body})'


# ------------------------------------------------------------------ inline math
GREEK = {'nu': 'ν', 'rho': 'ρ', 'lambda': 'λ', 'beta': 'β', 'varepsilon': 'ε', 'chi': 'χ', 'Delta': 'Δ', 'alpha': 'α'}
SYMS = {'le': '≤', 'ge': '≥', 'in': '∈', 'times': '×', 'to': '→', 'infty': '∞', 'sim': '∼', 'propto': '∝', 'mid': ' | ',
        'dots': '…', 'ldots': '…', 'sum': '∑', 'cdot': '·', 'qquad': '    ', 'quad': '  ', 'ne': '≠', 'top': '⊤', 'equiv': '≡',
        '|': '‖', 'lvert': '|', 'rvert': '|', ',': ' ', ' ': ' '}
ROMAN_FUN = {'Pr', 'max', 'min', 'arg'}


def math_tokens(s):
    i, toks = 0, []
    while i < len(s):
        ch = s[i]
        if ch == '\\':
            m = re.match(r'\\([A-Za-z]+|.)', s[i:])
            toks.append(('cmd', m.group(1)))
            i += len(m.group(0))
        elif ch == '{':
            depth, j = 1, i + 1
            while depth:
                depth += {'{': 1, '}': -1}.get(s[j], 0)
                j += 1
            toks.append(('grp', s[i + 1:j - 1]))
            i = j
        elif ch in '^_':
            toks.append((ch, ch))
            i += 1
        elif ch.isspace():
            i += 1
        else:
            toks.append(('chr', ch))
            i += 1
    return toks


def math_runs(s, sub=False, sup=False, bold=False):
    """Inline LaTeX math -> list of runs (italic letters, upright digits/operators)."""
    runs = []
    toks = math_tokens(s)
    k = 0

    def add(t, italic=None, b=None):
        it = italic if italic is not None else (len(t) == 1 and t.isalpha())
        runs.append({'t': t, 'i': it, 'b': bold if b is None else b, 'sub': sub, 'sup': sup})

    def take_arg(idx):
        typ, val = toks[idx]
        if typ == 'grp':
            return val, idx + 1
        if typ == 'cmd':
            return '\\' + val, idx + 1
        return val, idx + 1

    while k < len(toks):
        typ, val = toks[k]
        if typ in ('^', '_'):
            arg, k = take_arg(k + 1)
            runs.extend(math_runs(arg, sub=(typ == '_') or sub, sup=(typ == '^') or sup, bold=bold))
            continue
        if typ == 'grp':
            runs.extend(math_runs(val, sub, sup, bold))
        elif typ == 'chr':
            add({'-': '−', "'": '′'}.get(val, val))
        elif typ == 'cmd':
            if val in GREEK:
                add(GREEK[val], italic=True)
            elif val in SYMS:
                add(SYMS[val], italic=False)
            elif val in ROMAN_FUN:
                add(val, italic=False)
            elif val in ('mathrm', 'text', 'operatorname'):
                arg, k2 = take_arg(k + 1)
                add(arg.replace('\\', ''), italic=False)
                k = k2
                continue
            elif val in ('mathbf', 'boldsymbol'):
                arg, k2 = take_arg(k + 1)
                runs.extend(math_runs(arg, sub, sup, bold=True))
                k = k2
                continue
            elif val == 'mathbb':
                arg, k2 = take_arg(k + 1)
                add('𝟙' if arg == '1' else arg, italic=False)
                k = k2
                continue
            elif val in ('hat', 'bar', 'widehat'):
                arg, k2 = take_arg(k + 1)
                inner = math_runs(arg, sub, sup, bold)
                mark = '\u0302' if val in ('hat', 'widehat') else '\u0304'
                if inner:
                    inner[-1]['t'] += mark
                runs.extend(inner)
                k = k2
                continue
            elif val in ('frac', 'tfrac'):
                a, k2 = take_arg(k + 1)
                b, k3 = take_arg(k2)
                wrap = lambda x: len(x) > 1 and not re.fullmatch(r'\w', x)
                runs.extend(([{'t': '(', 'i': False, 'b': False, 'sub': sub, 'sup': sup}] if wrap(a) else []) +
                            math_runs(a, sub, sup, bold) +
                            ([{'t': ')', 'i': False, 'b': False, 'sub': sub, 'sup': sup}] if wrap(a) else []))
                add('/', italic=False)
                runs.extend(([{'t': '(', 'i': False, 'b': False, 'sub': sub, 'sup': sup}] if wrap(b) else []) +
                            math_runs(b, sub, sup, bold) +
                            ([{'t': ')', 'i': False, 'b': False, 'sub': sub, 'sup': sup}] if wrap(b) else []))
                k = k3
                continue
            elif val == 'sqrt':
                a, k2 = take_arg(k + 1)
                add('√(', italic=False)
                runs.extend(math_runs(a, sub, sup, bold))
                add(')', italic=False)
                k = k2
                continue
            elif val in ('left', 'right'):
                pass
            elif val == 'ensuremath':
                a, k2 = take_arg(k + 1)
                runs.extend(math_runs(a, sub, sup, bold))
                k = k2
                continue
            elif val in ('{', '}'):
                add(val, italic=False)
            else:
                raise ValueError('Unhandled math command \\' + val + ' in ' + s)
        k += 1
    # merge adjacent runs with identical formatting
    merged = []
    for r in runs:
        if merged and all(merged[-1].get(x) == r.get(x) for x in ('i', 'b', 'sub', 'sup')):
            merged[-1]['t'] += r['t']
        else:
            merged.append(dict(r))
    return merged


# ------------------------------------------------------------------ text -> runs
LABELS = {}


def expand_macros(s):
    for k in sorted(MACROS, key=len, reverse=True):
        s = s.replace('\\' + k + '{}', MACROS[k])
        s = re.sub(r'\\' + k + r'(?![A-Za-z])', lambda _m, v=MACROS[k]: v, s)
    return s


def plain_fix(t):
    t = t.replace('---', '—').replace('--', '–').replace('~', '\u00a0').replace("``", '“').replace("''", '”')
    t = t.replace('\\%', '%').replace('\\&', '&').replace('\\ ', ' ').replace('\\,', '\u2009')
    t = re.sub(r'(?<=\w)\\(?=\s)', '', t)
    return t


def text_runs(s, highlight_placeholders=False):
    """Paragraph LaTeX -> runs. Handles citations, refs, emph, inline math, ensuremath."""
    s = expand_macros(s)
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    s = re.sub(r'\\cite(p|t|alp)(?:\[([^\]]*)\])?(?:\[([^\]]*)\])?\{([^}]*)\}',
               lambda m: cite('cite' + m.group(1), (m.group(2) or '').strip(), (m.group(3) or '').strip(), m.group(4)), s)
    s = re.sub(r'\\eqref\{([^}]*)\}', lambda m: '(' + LABELS[m.group(1)] + ')', s)
    s = re.sub(r'\\ref\{([^}]*)\}', lambda m: LABELS[m.group(1)], s)
    s = s.replace('\\par', ' ')
    # tokenise into math / emph / text
    runs = []
    pos = 0
    pattern = re.compile(r'\$((?:[^$\\]|\\.)*?)\$|\\emph\{((?:[^{}]|\{[^{}]*\})*)\}|\\textbf\{((?:[^{}]|\{[^{}]*\})*)\}'
                         r'|\\ensuremath\{((?:[^{}]|\{[^{}]*\})*)\}')
    for m in pattern.finditer(s):
        if m.start() > pos:
            runs.append({'t': plain_fix(s[pos:m.start()])})
        if m.group(1) is not None or m.group(4) is not None:
            inner = m.group(1) if m.group(1) is not None else m.group(4)
            runs.extend(math_runs(inner))
        elif m.group(2) is not None:
            for r in text_runs(m.group(2)):
                r['i'] = True
                runs.append(r)
        else:
            for r in text_runs(m.group(3)):
                r['b'] = True
                runs.append(r)
        pos = m.end()
    if pos < len(s):
        runs.append({'t': plain_fix(s[pos:])})
    leftover = [r['t'] for r in runs if '\\' in r['t']]
    if leftover:
        raise ValueError('Unconverted LaTeX: ' + ' | '.join(leftover)[:300])
    if highlight_placeholders:
        out = []
        for r in runs:
            parts = re.split(r'(\[[^\]]*[A-Za-z][^\]]*\])', r['t'])
            for ptxt in parts:
                if not ptxt:
                    continue
                q = dict(r)
                q['t'] = ptxt
                if re.fullmatch(r'\[[^\]]*[A-Za-z][^\]]*\]', ptxt):
                    q['hl'] = True
                out.append(q)
        runs = out
    return [r for r in runs if r['t']]


def squash(s):
    return re.sub(r'\s+', ' ', s).strip()


# ------------------------------------------------------------------ tables
def table_rows(path):
    rows, seps = [], []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        if line.strip() == '\\midrule':
            seps.append(len(rows))
            continue
        if line.strip() == '\\addlinespace':
            seps.append(-len(rows))   # negative = light spacing
            continue
        line = re.sub(r'\\\\\s*$', '', line.rstrip())
        rows.append([text_runs(c.strip()) for c in re.split(r'(?<!\\)&', line)])
    return rows, seps


def H(*cells):
    """Header row helper: str or (str, span); strings may contain inline math."""
    out = []
    for c in cells:
        text, span = (c, 1) if isinstance(c, str) else c
        out.append({'runs': text_runs(text), 'span': span})
    return out


HEADERS = {
    'tab_data': [H('Task', '$n$', 'Groups (unit)', '$K$', '$p$', 'Class counts', 'Rarer endpoint (%)', 'Endpoint groups', 'Terms')],
    'tab_endpoint': [H('', '', ('QWK selection', 2), ('$\\Delta R_{\\mathrm{end}}$ relative to QWK', 3), '$\\Delta$QWK'),
                     H('Task', 'Family', '$R_0$', '$R_{K-1}$', 'AMAE', 'MMAE', 'QWK-floor', 'QWK-floor')],
    'tab_inference': [H('', ('$\\Delta R_{\\mathrm{end}}$', 6), ('$\\Delta$QWK', 2)),
                      H('Contrast', 'PO $+/-$', 'RF $+/-$', 'All $+/-$', 'Median', '$p$', 'Holm $p$', '$+/-$', 'Median')],
    'tab_controls': [H('Metric', 'Increase', 'Decrease', 'Median', 'Range')],
    'tab_constant': [H('Task', '$K$', '$\\nu_K$', 'Best cand.', 'QWK-sel.', 'AMAE-sel.', 'Worse than $\\nu_K$', 'QWK of QWK-sel.')],
    'tab_s_policies': [H('Task', 'Fam.', 'Criterion', 'QWK', 'MAE', 'AMAE', 'MMAE', 'Macro-F1', 'RPS', '$R_0$', '$R_{K-1}$', 'Bal.')],
    'tab_s_contrasts': [H('Task', 'Fam.', 'Criterion', '$\\Delta R_{\\mathrm{end}}$', '95% interval', 'Repeat 1 / 2',
                          '$\\Delta$QWK', '$\\Delta$MAE', '$\\Delta$AMAE', '$\\Delta$MMAE')],
    'tab_s_controls': [H('Task', 'Configuration', '$\\Delta R_0$', '$\\Delta R_{K-1}$', '$\\Delta$QWK', '$\\Delta$MAE',
                         '$\\Delta$AMAE', '$\\Delta$MMAE')],
    'tab_s_sim': [H('Prior', 'Signal', 'Fam.', 'Criterion', 'Same', '$\\Delta R_{\\mathrm{end}}$', 'MC 95% interval',
                    '$\\Delta$QWK', '$\\Delta$AMAE')],
    'tab_s_friedman': [H('Evaluation', '$\\chi^2_6$', '$p$', 'QWK', 'MAE', 'AMAE', 'MMAE', 'Macro-F1', 'RPS', 'QWK-floor')],
}


# ------------------------------------------------------------------ main parser
def strip_comments_keep_notes(src):
    notes = []
    out_lines = []
    for line in src.splitlines():
        m = re.match(r'\s*%%\s*AUTHORS:\s*(.*)', line)
        if m:
            out_lines.append('\\AUTHORNOTE{' + m.group(1).strip() + '}')
            continue
        out_lines.append(re.sub(r'(?<!\\)%.*', '', line))
    return '\n'.join(out_lines)


def number_labels(body):
    """First pass: assign numbers to sections, floats, equations, propositions, remarks."""
    sec = sub = 0
    counters = {'table': 0, 'figure': 0, 'eq': 0, 'prop': 0, 'rem': 0}
    env_stack = []
    for m in re.finditer(r'\\(section|subsection)\{([^}]*)\}(\\label\{([^}]*)\})?|\\begin\{(table|figure|equation|proposition|remark|longtable)\}|\\label\{([^}]*)\}|\\caption\{', body):
        if m.group(1) == 'section':
            sec += 1; sub = 0
            if m.group(4):
                LABELS[m.group(4)] = str(sec)
        elif m.group(1) == 'subsection':
            sub += 1
            if m.group(4):
                LABELS[m.group(4)] = f'{sec}.{sub}'
        elif m.group(5):
            env = m.group(5)
            key = {'table': 'table', 'longtable': 'table', 'figure': 'figure', 'equation': 'eq', 'proposition': 'prop',
                   'remark': 'rem'}[env]
            counters[key] += 1
            env_stack.append(key)
        elif m.group(6) and env_stack:
            key = env_stack[-1]
            prefix = 'S' if (WHICH == 'supplement' and key == 'table') else ''
            LABELS[m.group(6)] = prefix + str(counters[key])
    return counters


def parse_main(src):
    src = strip_comments_keep_notes(src)
    doc = {'blocks': []}
    B = doc['blocks']
    title = re.search(r'\\title\[([^\]]*)\]\{([^}]*)\}', src)
    doc['running_title'] = title.group(1)
    doc['title'] = title.group(2)
    doc['authors'] = [text_runs(a, True) for a in ['[First name] [Surname]\u00b9*', '[First name] [Surname]\u00b9']]
    doc['affil'] = text_runs('\u00b9[Department], [Institution], [City], [Country]', True)
    doc['email'] = text_runs('*Corresponding author: [corresponding e-mail]', True)
    abstract = re.search(r'\\abstract\{(.*?)\}\n\n\\keywords\{(.*?)\}', src, flags=re.S)
    doc['abstract'] = text_runs(squash(abstract.group(1)))
    doc['keywords'] = abstract.group(2)
    body = src[src.index('\\maketitle') + len('\\maketitle'):src.index('\\bibliography{refs}')]
    number_labels(body)

    # tokenise body into structural elements
    pat = re.compile(
        r'\\section\*?\{([^}]*)\}(?:\\label\{[^}]*\})?'
        r'|\\subsection\{([^}]*)\}(?:\\label\{[^}]*\})?'
        r'|\\begin\{(table|figure|enumerate|align\*|equation\*|equation|proposition|proof|remark)\}(\[[^\]]*\])?(.*?)\\end\{\3\}'
        r'|\\bmhead\{([^}]*)\}'
        r'|\\AUTHORNOTE\{([^}]*)\}'
        r'|\\backmatter'
        r'|\n\s*\n', flags=re.S)
    pending_runin = None
    pos = 0
    sec = sub = 0

    def flush(text):
        nonlocal pending_runin
        text = squash(text)
        if not text:
            return
        runin = None
        pm = re.match(r'\\paragraph\{([^}]*)\}\s*(.*)', text, flags=re.S)
        if pm:
            runin, text = pm.group(1), pm.group(2)
        blk = {'k': 'p', 'runs': text_runs(text, highlight_placeholders=True)}
        if runin or pending_runin:
            blk['runin'] = runin or pending_runin
            pending_runin = None
        B.append(blk)

    for m in pat.finditer(body):
        flush(body[pos:m.start()])
        pos = m.end()
        if m.group(1) is not None:
            if '*' in body[m.start():m.start() + 10]:
                B.append({'k': 'h1', 'text': m.group(1), 'num': ''})
            else:
                sec += 1; sub = 0
                B.append({'k': 'h1', 'text': m.group(1), 'num': str(sec)})
        elif m.group(2) is not None:
            sub += 1
            B.append({'k': 'h2', 'text': m.group(2), 'num': f'{sec}.{sub}'})
        elif m.group(3):
            env, opt, inner = m.group(3), (m.group(4) or '').strip('[]'), m.group(5)
            lab = re.search(r'\\label\{([^}]*)\}', inner)
            num = LABELS.get(lab.group(1)) if lab else None
            if env == 'table':
                cap = re.search(r'\\caption\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', inner, flags=re.S).group(1)
                tab = re.search(r'\\input\{tables/([^}]*)\}', inner).group(1)
                rows, seps = table_rows(MS / 'tables' / (tab + '.tex'))
                B.append({'k': 'table', 'num': num, 'id': tab, 'caption': text_runs(squash(cap)),
                          'header': HEADERS[tab], 'rows': rows, 'seps': seps})
            elif env == 'figure':
                cap = re.search(r'\\caption\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', inner, flags=re.S).group(1)
                g = re.search(r'\\includegraphics\[width=([\d.]*)\\textwidth\]\{figures/([^}]*)\.pdf\}', inner)
                B.append({'k': 'figure', 'num': num, 'file': g.group(2) + '.png', 'width': float(g.group(1) or 1),
                          'caption': text_runs(squash(cap))})
            elif env == 'enumerate':
                items = [squash(x) for x in re.split(r'\\item', inner)[1:]]
                B.append({'k': 'ol', 'items': [text_runs(x) for x in items]})
            elif env == 'align*':
                B.append({'k': 'eq', 'id': 'defs'})
            elif env == 'equation*':
                B.append({'k': 'eq', 'id': 'rps'})
            elif env == 'equation':
                B.append({'k': 'eq', 'id': 'qwk', 'num': num})
            elif env == 'proposition':
                intro, rest = inner.split('\\begin{enumerate}', 1)
                items = re.split(r'\\item\[([^\]]*)\]', rest.split('\\end{enumerate}')[0])[1:]
                blocks = []
                for lab_, txt in zip(items[0::2], items[1::2]):
                    parts = re.split(r'\\\[(.*?)\\\]', txt, flags=re.S)
                    blocks.append({'label': lab_, 'runs': text_runs(squash(parts[0])),
                                   'eq': 'nuk' if len(parts) > 1 else None,
                                   'after': text_runs(squash(parts[2])) if len(parts) > 2 else []})
                B.append({'k': 'theorem', 'label': 'Proposition ' + num, 'title': opt,
                          'intro': text_runs(squash(re.sub(r'\\label\{[^}]*\}', '', intro))), 'items': blocks})
            elif env == 'proof':
                B.append({'k': 'proof', 'runs': text_runs(squash(inner))})
            elif env == 'remark':
                B.append({'k': 'remark', 'label': 'Remark ' + num, 'title': opt,
                          'runs': text_runs(squash(re.sub(r'\\label\{[^}]*\}', '', inner)))})
        elif m.group(6) is not None:
            pending_runin = m.group(6)
        elif m.group(7) is not None:
            B.append({'k': 'note', 'runs': [{'t': '[AUTHORS: ' + m.group(7) + ']', 'hl': True}]})
    flush(body[pos:])

    # references (cited only), alphabetical by surname without lowercase prefix
    def sortkey(k):
        last = authors_of(BIB[k])[0][0]
        core = re.sub(r'^(?:[a-z]+\s)+', '', last)
        return (core.lower(), BIB[k]['year'])
    refs = []
    for k in sorted(CITED, key=sortkey):
        refs.append(format_ref(BIB[k]))
    doc['references'] = refs
    return doc


def format_ref(e):
    au = authors_of(e)
    names = ', '.join(f"{last} {''.join(p[0] for p in re.split(r'[\s-]+', first) if p)}".strip() for last, first in au)
    title = tex_accents(e['title'])
    runs = [{'t': f"{names} ({e['year']}) {title}. "}]
    typ = e['_type']
    if typ == 'article':
        runs.append({'t': tex_accents(e['journal']), 'i': True})
        vol = e.get('volume')
        tail = ''
        if vol:
            tail += f' {vol}'
            if e.get('number'):
                tail += f"({e['number']})"
        if e.get('pages'):
            tail += (':' if vol else ' ') + e['pages'].replace('--', '–')
        runs.append({'t': tail + '.'})
    elif typ == 'inproceedings':
        runs.append({'t': 'In: '})
        runs.append({'t': tex_accents(e['booktitle']), 'i': True})
        tail = f", pp {e['pages'].replace('--', '–')}" if e.get('pages') else ''
        if e.get('publisher'):
            tail += f", {e['publisher']}"
        runs.append({'t': tail + '.'})
    else:
        runs.append({'t': tex_accents(e.get('howpublished', '')) + ' [dataset].'})
    if e.get('doi'):
        url = 'https://doi.org/' + e['doi']
        runs.append({'t': ' '})
        runs.append({'t': url, 'link': url})
    return runs


def parse_supplement(src):
    src = re.sub(r'(?<!\\)%.*', '', src)
    doc = {'blocks': [], 'title': 'Supplementary Information',
           'subtitle': re.search(r'\\large ([^}]*)\}', src).group(1).strip()}
    body = src[src.index('\\maketitle') + len('\\maketitle'):src.index('\\end{document}')]
    number_labels(body)
    B = doc['blocks']
    pat = re.compile(r'\\section\*\{([^}]*)\}|\\begin\{longtable\}.*?\\caption\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}'
                     r'.*?\\input\{tables/([^}]*)\}\s*\\end\{longtable\}|\\paragraph\{([^}]*)\}|\n\s*\n', flags=re.S)
    pos = 0
    runin = None
    tabn = 0

    def flush(t):
        nonlocal runin
        t = squash(re.sub(r'\{\\footnotesize|\\setlength\{[^}]*\}\{[^}]*\}|^\}|\}$', '', t.strip()))
        if not t or t == '}':
            return
        blk = {'k': 'p', 'runs': text_runs(t)}
        if runin:
            blk['runin'] = runin
            runin = None
        B.append(blk)

    for m in pat.finditer(body):
        flush(body[pos:m.start()])
        pos = m.end()
        if m.group(1):
            B.append({'k': 'h1', 'text': m.group(1), 'num': ''})
        elif m.group(3):
            tabn += 1
            rows, seps = table_rows(MS / 'tables' / (m.group(3) + '.tex'))
            cap = re.sub(r'\\label\{[^}]*\}', '', m.group(2))
            B.append({'k': 'table', 'num': f'S{tabn}', 'id': m.group(3), 'caption': text_runs(squash(cap)),
                      'header': HEADERS[m.group(3)], 'rows': rows, 'seps': seps, 'small': True})
        elif m.group(4):
            runin = m.group(4)
    flush(body[pos:])
    return doc


src = (MS / ('main.tex' if WHICH == 'main' else 'supplement.tex')).read_text(encoding='utf-8')
doc = parse_main(src) if WHICH == 'main' else parse_supplement(src)
OUTFILE.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
print(WHICH, 'blocks:', len(doc['blocks']), 'refs:', len(doc.get('references', [])), 'labels:', len(LABELS))
