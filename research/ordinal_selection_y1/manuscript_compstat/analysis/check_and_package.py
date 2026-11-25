"""Static checks of the LaTeX sources and a flat submission package.

No TeX installation is needed. Checks: every macro used is defined, every \\input,
figure and citation resolves, braces/environments/inline math balance, abstract
length (150-250 words, after macro expansion). Then copies the files into a flat
`submission/` folder (Editorial Manager does not accept subfolders) with paths
rewritten, and a separate `supplement/` folder.

Usage: python check_and_package.py <manuscript dir>
"""
import re
import shutil
import sys
from pathlib import Path

MS = Path(sys.argv[1])
problems = []

macros = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{(.*)\}\s*$', (MS / 'numbers.tex').read_text(encoding='utf-8'), flags=re.M))
bib = set(re.findall(r'@\w+\{([^,]+),', (MS / 'refs.bib').read_text(encoding='utf-8')))
KNOWN = set('''documentclass usepackage theoremstyle newtheorem raggedbottom input newcommand begin end title author
affil fnm sur email orgdiv orgname orgaddress city country abstract keywords maketitle section subsection paragraph
citep citet citealp label ref eqref emph textwidth centering footnotesize caption toprule midrule bottomrule cmidrule
multicolumn includegraphics item backmatter bmhead bibliography le ge ne to infty frac sum max min arg mathrm mathbb
mathbf boldsymbol bar hat top sqrt varepsilon lambda nu rho chi propto mid dots in qquad quad cdot times setlength
tabcolsep renewcommand thetable arabic LTcapwidth date endfirsthead endhead endfoot addlinespace large hidelinks
small normalsize ensuremath sum_ alpha ldots tfrac widehat left right lvert rvert QWKF textbackslash Pr
Delta beta sim bigl bigr log pi scriptsize url and equalcont lfloor rfloor
'''.split())

def strip_comments(t):
    return re.sub(r'(?<!\\)%.*', '', t)

for name in ('main.tex', 'supplement.tex'):
    src = strip_comments((MS / name).read_text(encoding='utf-8'))
    used = set(re.findall(r'\\([A-Za-z]+)', src))
    for u in sorted(used):
        if u not in macros and u not in KNOWN and not u.startswith(('text', 'math', 'eq', 'end', 'begin')):
            problems.append(f'{name}: unknown or undefined command \\{u}')
    for f in re.findall(r'\\input\{([^}]+)\}', src):
        p = MS / (f if f.endswith('.tex') else f + '.tex')
        if not p.exists():
            problems.append(f'{name}: missing input {f}')
    for f in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', src):
        if not (MS / f).exists():
            problems.append(f'{name}: missing figure {f}')
    for group in re.findall(r'\\cite(?:p|t|alp)?(?:\[[^\]]*\]){0,2}\{([^}]+)\}', src):
        for key in group.split(','):
            if key.strip() not in bib:
                problems.append(f'{name}: citation key not in refs.bib: {key.strip()}')
    depth = 0
    for i, ch in enumerate(src):
        if ch == '{' and (i == 0 or src[i - 1] != '\\'):
            depth += 1
        elif ch == '}' and (i == 0 or src[i - 1] != '\\'):
            depth -= 1
        if depth < 0:
            problems.append(f'{name}: unbalanced closing brace near char {i}')
            break
    if depth != 0:
        problems.append(f'{name}: brace depth {depth} at end')
    begins = re.findall(r'\\begin\{(\w+\*?)\}', src)
    ends = re.findall(r'\\end\{(\w+\*?)\}', src)
    for env in set(begins) | set(ends):
        if begins.count(env) != ends.count(env):
            problems.append(f'{name}: environment {env} begins {begins.count(env)} ends {ends.count(env)}')
    for k, para in enumerate(re.split(r'\n\s*\n', src)):
        if len(re.findall(r'(?<!\\)\$', para)) % 2:
            problems.append(f'{name}: odd number of $ in paragraph {k}: {para[:80]!r}')

for t in sorted((MS / 'tables').glob('*.tex')):
    for line in t.read_text(encoding='utf-8').splitlines():
        if line.count('$') % 2:
            problems.append(f'{t.name}: odd $ in line {line[:60]!r}')

# abstract length after macro expansion
main = (MS / 'main.tex').read_text(encoding='utf-8')
abstract = re.search(r'\\abstract\{(.*?)\}\n\n\\keywords', main, flags=re.S).group(1)
for k, v in macros.items():
    abstract = abstract.replace('\\' + k + '{}', v).replace('\\' + k, v)
plain = re.sub(r'\\ensuremath\{([^}]*)\}', r'\1', abstract)
plain = re.sub(r'\\[A-Za-z]+\{\}', '', plain)
plain = re.sub(r'[\\$]', ' ', plain)
words = len(plain.split())
if not 150 <= words <= 250:
    problems.append(f'abstract has {words} words (journal requires 150-250)')
kw = re.search(r'\\keywords\{(.*?)\}', main).group(1).split(',')
if not 4 <= len(kw) <= 6:
    problems.append(f'{len(kw)} keywords (journal requires 4-6)')

# flat packages
sub = MS / 'submission'
sup = MS / 'supplement_package'
for d in (sub, sup):
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
flat = main.replace('\\input{tables/', '\\input{').replace('{figures/', '{')
(sub / 'main.tex').write_text(flat, encoding='utf-8')
for f in ['refs.bib', 'numbers.tex']:
    shutil.copy2(MS / f, sub / f)
for t in (MS / 'tables').glob('tab_*.tex'):
    if not t.name.startswith('tab_s_'):
        shutil.copy2(t, sub / t.name)
for fig in (MS / 'figures').glob('*.pdf'):
    shutil.copy2(fig, sub / fig.name)
supp = (MS / 'supplement.tex').read_text(encoding='utf-8').replace('\\input{tables/', '\\input{')
(sup / 'supplement.tex').write_text(supp, encoding='utf-8')
shutil.copy2(MS / 'numbers.tex', sup / 'numbers.tex')
for t in (MS / 'tables').glob('tab_s_*.tex'):
    shutil.copy2(t, sup / t.name)

print(f'abstract words: {words}; keywords: {len(kw)}; macros defined: {len(macros)}; bib entries: {len(bib)}')
print('submission files:', sorted(p.name for p in sub.iterdir()))
print('supplement files:', sorted(p.name for p in sup.iterdir()))
print('PROBLEMS:' if problems else 'No problems found.')
for p in problems:
    print('  -', p)
sys.exit(1 if problems else 0)
