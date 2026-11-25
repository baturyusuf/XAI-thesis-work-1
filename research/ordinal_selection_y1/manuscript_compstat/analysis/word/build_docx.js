// Build the Word versions (manuscript, supplement, cover letter) from the JSON models
// produced by latex_to_json.py. Usage:
//   node build_docx.js <main.json> <supplement.json> <figures dir> <cover_letter.txt> <out dir>
// Requires the `docx` npm package (NODE_PATH may point to its node_modules).
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink, ImageRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, VerticalAlign, LevelFormat, TabStopType,
  PageOrientation, Footer, PageNumber, LineNumberRestartFormat, ShadingType,
  Math: OMath, MathRun, MathFraction, MathSum, MathSubScript, MathSuperScript, MathSubSuperScript,
} = require('docx');
const JSZip = require('jszip');

const [mainJson, suppJson, figDir, coverTxt, outDir] = process.argv.slice(2);
const FONT = 'Times New Roman';
const A4 = { width: 11906, height: 16838 };
const MARGIN = 1440;

// ---------------------------------------------------------------- runs
function runs(rs, extra = {}) {
  const out = [];
  for (const r of rs || []) {
    const opts = {
      text: r.t, italics: !!r.i || !!extra.italics, bold: !!r.b || !!extra.bold,
      subScript: !!r.sub, superScript: !!r.sup && !r.sub, font: FONT,
      size: extra.size, highlight: r.hl ? 'yellow' : undefined,
    };
    if (r.link) {
      out.push(new ExternalHyperlink({ link: r.link, children: [new TextRun({ ...opts, style: 'Hyperlink' })] }));
    } else {
      out.push(new TextRun(opts));
    }
  }
  return out;
}
const T = (text, o = {}) => new TextRun({ text, font: FONT, ...o });

// ---------------------------------------------------------------- equations
// Upright names are post-processed into plain style (m:sty p) after packing.
const UPRIGHT = new Set(['MAE', 'AMAE', 'MMAE', 'QWK', 'RPS', 'max', 'odd', 'even']);
const mr = (t) => new MathRun(t);
const sub = (b, s) => new MathSubScript({ children: [mr(b)], subScript: [mr(s)] });
const sup = (b, s) => new MathSuperScript({ children: [mr(b)], superScript: [mr(s)] });
const frac = (n, d) => new MathFraction({ numerator: n, denominator: d });
const sum = (body, s, p) => new MathSum({ children: body, subScript: s, superScript: p });
const yhat = 'ŷ';

function eqParagraph(children, number) {
  const tabStops = [{ type: TabStopType.CENTER, position: 4513 }, { type: TabStopType.RIGHT, position: 9026 }];
  const kids = [T('\t'), new OMath({ children })];
  if (number) kids.push(T('\t(' + number + ')'));
  return new Paragraph({ tabStops, spacing: { before: 120, after: 120 }, children: kids });
}

function equation(id, num) {
  const absdiff = [mr('|'), sub('y', 'i'), mr('−'), sub(yhat, 'i'), mr('|')];
  if (id === 'defs') {
    return [
      eqParagraph([mr('MAE'), mr('='), frac([mr('1')], [mr('n')]), sum(absdiff, [mr('i')], []), mr(',    '),
        new MathSubScript({ children: [mr('MAE')], subScript: [mr('c')] }), mr('='),
        frac([mr('1')], [sub('n', 'c')]), sum(absdiff, [mr('i:'), sub('y', 'i'), mr('=c')], []), mr(',')]),
      eqParagraph([mr('AMAE'), mr('='), frac([mr('1')], [mr('K')]),
        sum([new MathSubScript({ children: [mr('MAE')], subScript: [mr('c')] })], [mr('c=0')], [mr('K−1')]),
        mr(',    '), mr('MMAE'), mr('='),
        new MathSubScript({ children: [mr('max')], subScript: [mr('c')] }),
        new MathSubScript({ children: [mr('MAE')], subScript: [mr('c')] }), mr('.')]),
    ];
  }
  if (id === 'qwk') {
    return [eqParagraph([mr('QWK'), mr('=1−'), frac([mr('O')], [mr('E')]), mr(',   '), mr('O'), mr('='),
      frac([mr('1')], [mr('n')]), sum([mr('('), sub('y', 'i'), mr('−'), sub(yhat, 'i'), new MathSuperScript({ children: [mr(')')], superScript: [mr('2')] })], [mr('i')], []),
      mr(',   '), mr('E'), mr('='), new MathSubSuperScript({ children: [mr('s')], subScript: [mr('y')], superScript: [mr('2')] }),
      mr('+'), new MathSubSuperScript({ children: [mr('s')], subScript: [mr(yhat)], superScript: [mr('2')] }),
      mr('+('), mr('ȳ'), mr('−'), mr(yhat + '̄'), new MathSuperScript({ children: [mr(')')], superScript: [mr('2')] }),
      mr(',')], num)];
  }
  if (id === 'rps') {
    const F = new MathSubScript({ children: [mr('F')], subScript: [mr('ij')] });
    return [eqParagraph([mr('RPS'), mr('='), frac([mr('1')], [mr('n')]),
      sum([frac([mr('1')], [mr('K−1')]),
        sum([mr('{'), F, mr('−𝟙('), sub('y', 'i'), mr('≤j)'), new MathSuperScript({ children: [mr('}')], superScript: [mr('2')] })],
          [mr('j=0')], [mr('K−2')])], [mr('i')], []),
      mr(',     '), new MathSubScript({ children: [mr('F')], subScript: [mr('ij')] }), mr('='),
      sum([new MathSubScript({ children: [mr('p')], subScript: [mr('ik')] })], [mr('k≤j')], []), mr(',')])];
  }
  if (id === 'nuk') {
    return [eqParagraph([sub('ν', 'K'), mr('='), frac([mr('K+1')], [mr('4K')]), mr('  ('), mr('K'), mr(' '), mr('odd'),
      mr('),      '), sub('ν', 'K'), mr('='), frac([mr('K')], [mr('4(K−1)')]), mr('  ('), mr('K'), mr(' '), mr('even'), mr(')')])];
  }
  throw new Error('Unknown equation ' + id);
}

// ---------------------------------------------------------------- tables
function table(b, textWidth, small) {
  const ncol = b.header[b.header.length - 1].reduce((a, c) => a + c.span, 0);
  // column width heuristic: proportional to the longest text in each column (bounded)
  const len = new Array(ncol).fill(4);
  const txt = (rs) => (rs || []).map((r) => r.t).join('');
  const isSpan = (r) => r.length === 1 && r[0] && r[0].span;
  for (const row of b.rows) if (!isSpan(row)) row.forEach((c, j) => { len[j] = Math.max(len[j], Math.min(txt(c).length, 24)); });
  b.header[b.header.length - 1].forEach((c, j) => { len[j] = Math.max(len[j], Math.min(txt(c.runs).length, 14)); });
  const total = len.reduce((a, x) => a + x, 0);
  const widths = len.map((x) => Math.floor(textWidth * x / total));
  widths[widths.length - 1] += textWidth - widths.reduce((a, x) => a + x, 0);
  const size = small ? 15 : 17;
  const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  const rule = (sz) => ({ style: BorderStyle.SINGLE, size: sz, color: '000000' });
  const textCols = (b.id === 'tab_stage4' || b.id === 'tab_stage5') ? 3 : (b.id === 'tab_s_stage5_tasks' || b.id === 'tab_s_source_rule') ? 1 : b.id.startsWith('tab_s_stage4') ? 1 : b.id.startsWith('tab_s_') ? 3 : (['tab_inference', 'tab_controls'].includes(b.id) ? 1 : 2);
  const align = (j) => (j < textCols ? AlignmentType.LEFT : AlignmentType.CENTER);
  const cell = (rs, j, w, borders, span = 1, bold = false) => new TableCell({
    width: { size: w, type: WidthType.DXA }, columnSpan: span > 1 ? span : undefined,
    borders: { left: none, right: none, top: borders.top || none, bottom: borders.bottom || none },
    margins: { top: 30, bottom: 30, left: 60, right: 60 }, verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ alignment: span > 1 ? AlignmentType.CENTER : align(j), spacing: { before: 0, after: 0, line: 240 },
      run: { size, font: FONT }, // paragraph-mark size keeps empty cells as short as filled ones
      children: (rs && rs.length) ? runs(rs, { size, bold }) : [T('', { size })] })],
  });
  const rows = [];
  b.header.forEach((hr, hi) => {
    let j = 0;
    const cells = hr.map((c) => {
      const w = widths.slice(j, j + c.span).reduce((a, x) => a + x, 0);
      const borders = { top: hi === 0 ? rule(12) : undefined,
        bottom: hi === b.header.length - 1 ? rule(6) : (c.span > 1 ? rule(4) : undefined) };
      const out = cell(c.runs, j, w, borders, c.span, true);
      j += c.span;
      return out;
    });
    rows.push(new TableRow({ tableHeader: true, cantSplit: true, children: cells }));
  });
  const midrules = new Set(b.seps.filter((s) => s > 0));
  b.rows.forEach((r, i) => {
    const borders = { top: midrules.has(i) ? rule(4) : undefined, bottom: i === b.rows.length - 1 ? rule(12) : undefined };
    if (isSpan(r)) {
      const sc = new TableCell({ width: { size: textWidth, type: WidthType.DXA }, columnSpan: r[0].span,
        borders: { left: none, right: none, top: borders.top || none, bottom: borders.bottom || none },
        margins: { top: 60, bottom: 30, left: 60, right: 60 },
        children: [new Paragraph({ alignment: AlignmentType.LEFT, spacing: { before: 0, after: 0, line: 240 },
          children: runs(r[0].runs, { size }) })] });
      rows.push(new TableRow({ cantSplit: true, children: [sc] }));
      return;
    }
    rows.push(new TableRow({ cantSplit: true, children: r.map((c, j) => cell(c, j, widths[j], borders)) }));
  });
  return new Table({ width: { size: textWidth, type: WidthType.DXA }, columnWidths: widths, rows,
    borders: { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none } });
}

function caption(prefix, num, rs, before = 240) {
  return new Paragraph({ spacing: { before, after: 120, line: 276 }, keepNext: prefix === 'Table',
    children: [T(prefix + ' ' + num + ' ', { bold: true, size: 20 }), ...runs(rs, { size: 20 })] });
}

// ---------------------------------------------------------------- figures
function pngSize(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }
function figure(b, textWidthDxa) {
  const buf = fs.readFileSync(path.join(figDir, b.file));
  const { w, h } = pngSize(buf);
  const widthPx = Math.round((textWidthDxa / 1440) * 96 * b.width);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 240, after: 0 },
      children: [new ImageRun({ type: 'png', data: buf, transformation: { width: widthPx, height: Math.round(widthPx * h / w) },
        altText: { title: 'Figure ' + b.num, description: b.caption.map((r) => r.t).join('').slice(0, 250), name: b.file } })] }),
    caption('Fig.', b.num, b.caption, 60),
  ];
}

// ---------------------------------------------------------------- common styles
const styles = {
  default: { document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 360, after: 120 } } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: FONT, size: 26, bold: true }, paragraph: { spacing: { before: 360, after: 120 }, keepNext: true, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: FONT, size: 24, bold: true, italics: true }, paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 1 } },
    { id: 'Title', name: 'Title', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { font: FONT, size: 32, bold: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 0, after: 240, line: 300 } } },
  ],
  characterStyles: [{ id: 'Hyperlink', name: 'Hyperlink', basedOn: 'DefaultParagraphFont', run: { color: '1F4E79', underline: {} } }],
};
const numbering = { config: [
  { reference: 'contrib', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 567, hanging: 360 } } } }] },
  { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 567, hanging: 360 } } } }] },
] };
const footer = () => ({ default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
  children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 })] })] }) });

async function save(doc, file, uprightMath) {
  let buf = await Packer.toBuffer(doc);
  const zip = await JSZip.loadAsync(buf);
  let xml = await zip.file('word/document.xml').async('string');
  if (uprightMath) {
    xml = xml.replace(/<m:r>((?:<w:rPr>.*?<\/w:rPr>)?)<m:t( [^>]*)?>([^<]*)<\/m:t><\/m:r>/g, (all, rpr, attr, text) => {
      return UPRIGHT.has(text.trim()) || /^[\s,.():+=−\-]+$/.test(text)
        ? `<m:r><m:rPr><m:sty m:val="p"/></m:rPr>${rpr}<m:t${attr || ''}>${text}</m:t></m:r>` : all;
    });
    zip.file('word/document.xml', xml);
  }
  buf = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
  fs.writeFileSync(file, buf);
  console.log('wrote', file, buf.length, 'bytes');
}

// ---------------------------------------------------------------- manuscript
function buildMain(d) {
  const TW = A4.width - 2 * MARGIN;
  const kids = [];
  kids.push(new Paragraph({ style: 'Title', children: [T(d.title, { bold: true, size: 32 })] }));
  d.authors.forEach((a) => kids.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0 }, children: runs(a) })));
  d.affil.forEach((a, i) => kids.push(new Paragraph({ alignment: AlignmentType.CENTER,
    spacing: { before: i === 0 ? 120 : 0, after: 0 }, children: runs(a, { size: 22 }) })));
  d.notes.forEach((a, i) => kids.push(new Paragraph({ alignment: AlignmentType.CENTER,
    spacing: { before: i === 0 ? 160 : 0, after: i === d.notes.length - 1 ? 240 : 0 }, children: runs(a, { size: 20 }) })));
  kids.push(new Paragraph({ spacing: { before: 240, after: 60 }, children: [T('Abstract', { bold: true })] }));
  kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, children: runs(d.abstract) }));
  kids.push(new Paragraph({ spacing: { before: 120, after: 240 }, children: [T('Keywords ', { bold: true }), T(d.keywords.split(',').map((s) => s.trim()).join(' · '))] }));
  for (const b of d.blocks) {
    switch (b.k) {
      case 'h1': kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [T((b.num ? b.num + ' ' : '') + b.text, { bold: true, size: 26 })] })); break;
      case 'h2': kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [T(b.num + ' ' + b.text, { bold: true, italics: true })] })); break;
      // Paragraphs with long unbreakable URLs or paths are left-aligned: justification would stretch the spaces.
      case 'p': kids.push(new Paragraph({ alignment: b.runs.some((r) => /https?:\/\//.test(r.t || '')) ? AlignmentType.LEFT : AlignmentType.JUSTIFIED,
        children: [...(b.runin ? [T(b.runin.replace(/\.$/, '') + '. ', { bold: true })] : []), ...runs(b.runs)] })); break;
      case 'ol': b.items.forEach((it) => kids.push(new Paragraph({ numbering: { reference: 'contrib', level: 0 }, alignment: AlignmentType.JUSTIFIED, children: runs(it) }))); break;
      case 'eq': kids.push(...equation(b.id, b.num)); break;
      case 'theorem':
        kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 180 },
          children: [T(b.label, { bold: true }), T(b.title ? ' (' + b.title + '). ' : '. '), ...runs(b.intro, { italics: true })] }));
        for (const it of b.items) {
          kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, indent: { left: 567, hanging: 454 },
            children: [T(it.label + '\t'), ...runs(it.runs, { italics: true })], tabStops: [{ type: TabStopType.LEFT, position: 567 }] }));
          if (it.eq) kids.push(...equation(it.eq));
          if (it.after && it.after.length) kids.push(new Paragraph({ indent: { left: 567 }, alignment: AlignmentType.JUSTIFIED, children: runs(it.after, { italics: true }) }));
        }
        break;
      case 'proof': kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, children: [T('Proof. ', { italics: true }), ...runs(b.runs), T('  ∎')] })); break;
      case 'remark': kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 180 },
        children: [T(b.label, { bold: true }), T(b.title ? ' (' + b.title + '). ' : '. ', { italics: true }), ...runs(b.runs)] })); break;
      case 'table': kids.push(caption('Table', b.num, b.caption)); kids.push(table(b, TW, false)); kids.push(new Paragraph({ spacing: { after: 120 }, children: [] })); break;
      case 'figure': kids.push(...figure(b, TW)); break;
      case 'note': kids.push(new Paragraph({ children: runs(b.runs) })); break;
      default: throw new Error('block ' + b.k);
    }
  }
  kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [T('References', { bold: true, size: 26 })] }));
  for (const r of d.references) {
    kids.push(new Paragraph({ indent: { left: 360, hanging: 360 }, spacing: { after: 80, line: 276 }, children: runs(r, { size: 22 }) }));
  }
  return new Document({
    creator: d.creator, title: d.title, styles, numbering,
    sections: [{ properties: { page: { size: A4, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } },
      lineNumbers: { countBy: 1, restart: LineNumberRestartFormat.CONTINUOUS } }, footers: footer(), children: kids }],
  });
}

// ---------------------------------------------------------------- supplement (landscape)
function buildSupplement(d) {
  const TW = A4.height - 2 * MARGIN;
  const kids = [
    new Paragraph({ style: 'Title', children: [T(d.title, { bold: true, size: 32 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [T(d.subtitle, { size: 24 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [T(d.authors_line, { size: 22 })] }),
    ...d.front.map((l, i) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: i === d.front.length - 1 ? 360 : 0 },
      children: [T(l, { size: 20 })] })),
  ];
  for (const b of d.blocks) {
    if (b.k === 'h1') kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [T(b.text, { bold: true, size: 26 })] }));
    else if (b.k === 'p') kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: 300 },
      children: [...(b.runin ? [T(b.runin.replace(/\.$/, '') + '. ', { bold: true })] : []), ...runs(b.runs, { size: 22 })] }));
    else if (b.k === 'table') { kids.push(caption('Table', b.num, b.caption)); kids.push(table(b, TW, true)); kids.push(new Paragraph({ children: [] })); }
  }
  return new Document({ creator: d.authors_line.replace(' · ', ', '), title: d.title, styles, numbering,
    sections: [{ properties: { page: { size: { width: A4.width, height: A4.height, orientation: PageOrientation.LANDSCAPE },
      margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } }, footers: footer(), children: kids }] });
}

// ---------------------------------------------------------------- cover letter
function buildCover(text) {
  const kids = [];
  const blocks = text.replace(/\r/g, '').split(/\n\s*\n/);
  for (const blk of blocks) {
    const lines = blk.split('\n').filter((l) => l.trim());
    if (lines.every((l) => l.startsWith('- '))) {
      lines.forEach((l) => kids.push(new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { after: 80 },
        children: hl(l.slice(2)) })));
    } else if (lines.length > 1 && lines.every((l) => l.length < 60)) {
      lines.forEach((l, i) => kids.push(new Paragraph({ spacing: { after: i === lines.length - 1 ? 200 : 0 }, children: hl(l) })));
    } else {
      kids.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 200 }, children: hl(lines.join(' ')) }));
    }
  }
  function hl(s) {
    return s.split(/(\[[^\]]+\])/).filter(Boolean).map((p) => T(p, { highlight: /^\[.*\]$/.test(p) ? 'yellow' : undefined, size: 24 }));
  }
  return new Document({ styles, numbering, sections: [{ properties: { page: { size: A4,
    margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } }, children: kids }] });
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const main = JSON.parse(fs.readFileSync(mainJson, 'utf8'));
  const supp = JSON.parse(fs.readFileSync(suppJson, 'utf8'));
  await save(buildMain(main), path.join(outDir, 'manuscript.docx'), true);
  // separate figure files named by their final number (journals ask for them alongside a Word manuscript)
  const figOut = path.join(outDir, 'figures');
  fs.mkdirSync(figOut, { recursive: true });
  for (const b of main.blocks.filter((x) => x.k === 'figure')) {
    for (const ext of ['png', 'pdf']) {
      fs.copyFileSync(path.join(figDir, b.file.replace(/\.png$/, '.' + ext)), path.join(figOut, `Fig${b.num}.${ext}`));
    }
  }
  await save(buildSupplement(supp), path.join(outDir, 'supplementary_information.docx'), false);
  await save(buildCover(fs.readFileSync(coverTxt, 'utf8')), path.join(outDir, 'cover_letter.docx'), false);
})().catch((e) => { console.error(e); process.exit(1); });
