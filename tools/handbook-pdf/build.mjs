#!/usr/bin/env node
// Builds a handbook PDF from its Markdown source.
//
//   node build.mjs <handbook.md> <output.pdf> [--keep-html]
//
// The Markdown dialect is plain GitHub-flavored Markdown, so the same file reads
// well on GitHub: pipe tables, fenced code, GitHub alerts (> [!NOTE]), mermaid
// diagrams, and relative image links. The build fails (exit 1) on a broken
// diagram, a missing image or a dead internal link, and warns about repeated
// paragraphs and over-long code lines.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';
import puppeteer from 'puppeteer-core';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const MAX_CODE_COLS = 88;
const LONG_LISTING_LINES = 16;
const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
].filter(Boolean);

const args = process.argv.slice(2);
const keepHtml = args.includes('--keep-html');
const [inputArg, outputArg] = args.filter((a) => !a.startsWith('--'));
if (!inputArg || !outputArg) {
  console.error('usage: node build.mjs <handbook.md> <output.pdf> [--keep-html]');
  process.exit(2);
}
const inputPath = path.resolve(inputArg);
const outputPath = path.resolve(outputArg);
const sourceDir = path.dirname(inputPath);
const source = fs.readFileSync(inputPath, 'utf8').replace(/\r\n/g, '\n');

const errors = [];
const warnings = [];

const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const cssString = (s) => String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"');

// ---------------------------------------------------------------- cover block

const lines = source.split('\n');
const ruleAt = lines.findIndex((l) => l.trim() === '---');
if (ruleAt === -1) {
  console.error('error: no cover block. Put the title, edition line and promise above a line containing only ---');
  process.exit(1);
}
const coverMd = lines.slice(0, ruleAt).join('\n');
const bodyMd = lines.slice(ruleAt + 1).join('\n');
const title = (coverMd.match(/^#\s+(.+)$/m) || [])[1]?.trim();
if (!title) {
  console.error('error: the cover block needs a "# Title" line');
  process.exit(1);
}
const edition = (coverMd.match(/\*\*(.+?)\*\*/) || [])[1]?.trim() || '';
const series = (coverMd.match(/\*\*.+?\*\*\s*·\s*(.+)$/m) || [])[1]?.trim() || '';
const promise = (coverMd.match(/^>\s*(.+)$/m) || [])[1]?.trim() || '';

// ------------------------------------------------------------------- markdown

const md = new MarkdownIt({ html: false, linkify: true, typographer: false });

// GitHub's heading-anchor algorithm, so [text](#anchor) links work in both places.
const usedSlugs = new Map();
function slugify(text) {
  const base = text
    .trim()
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s_-]/gu, '')
    .replace(/\s/g, '-');
  const n = usedSlugs.get(base) || 0;
  usedSlugs.set(base, n + 1);
  return n === 0 ? base : `${base}-${n}`;
}

const ALERTS = {
  NOTE: 'Note',
  TIP: 'Tip',
  IMPORTANT: 'Takeaway',
  WARNING: 'Watch out',
  CAUTION: 'Caution',
};

const SECTION_KINDS = [
  [/^why it matters/i, 'why'],
  [/^the idea/i, 'idea'],
  [/^worked example/i, 'example'],
  [/^common mistakes/i, 'mistakes'],
  [/^check yourself/i, 'check'],
  [/^questions to ask/i, 'ask'],
];

const outline = []; // { level, id, text, num }

// Block-level pass: alerts, captions, output labels (runs before inline parsing).
md.core.ruler.after('block', 'handbook_blocks', (state) => {
  const t = state.tokens;
  for (let i = 0; i < t.length; i++) {
    if (t[i].type === 'blockquote_open' && t[i + 2]?.type === 'inline') {
      const m = t[i + 2].content.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*\n?/);
      if (m) {
        const kind = m[1];
        t[i].attrJoin('class', `callout callout-${kind.toLowerCase()}`);
        t[i + 2].content = t[i + 2].content.slice(m[0].length);
        const label = new state.Token('html_block', '', 0);
        label.content = `<p class="callout-label">${ALERTS[kind]}</p>\n`;
        if (t[i + 2].content.trim() === '') t.splice(i + 1, 3, label);
        else t.splice(i + 1, 0, label);
      }
    }
    if (t[i].type === 'paragraph_open' && t[i + 1]?.type === 'inline') {
      const c = t[i + 1].content.trim();
      if (/^\*(Figure|Table) [^*]+\*$/s.test(c)) t[i].attrJoin('class', 'caption');
      else if (/^(Result|Output)[^\n]{0,70}:$/.test(c)) t[i].attrJoin('class', 'out-label');
    }
  }
});

// Inline-level pass: heading ids, figures, task-list boxes.
md.core.ruler.push('handbook_inline', (state) => {
  const t = state.tokens;
  for (let i = 0; i < t.length; i++) {
    if (t[i].type === 'heading_open') {
      const inline = t[i + 1];
      const text = inline.children
        .filter((c) => c.type === 'text' || c.type === 'code_inline')
        .map((c) => c.content)
        .join('');
      const level = Number(t[i].tag.slice(1));
      const id = slugify(text);
      t[i].attrSet('id', id);
      const entry = { level, id, text, num: null };
      if (level === 1) {
        t[i].attrJoin('class', 'part');
        const pm = text.match(/^(Part\s+[\w]+)\s*[—–:-]\s*(.+)$/);
        if (pm) {
          entry.kicker = pm[1];
          entry.name = pm[2];
          inline.children = [
            Object.assign(new state.Token('html_inline', '', 0), {
              content: `<span class="part-kicker">${esc(pm[1])}</span><span class="part-name">${esc(pm[2])}</span>`,
            }),
          ];
        }
      } else if (level === 2) {
        t[i].attrJoin('class', 'chapter');
        const cm = text.match(/^(\d+)\.\s+(.+)$/);
        if (cm) {
          entry.num = cm[1];
          entry.name = cm[2];
          const first = inline.children.find((c) => c.type === 'text');
          if (first) first.content = first.content.replace(/^\d+\.\s+/, '');
          inline.children.unshift(
            Object.assign(new state.Token('html_inline', '', 0), {
              content: `<span class="ch-num">${cm[1]}</span>`,
            }),
          );
        }
      } else if (level === 3) {
        const kind = SECTION_KINDS.find(([re]) => re.test(text));
        if (kind) t[i].attrJoin('class', `sec sec-${kind[1]}`);
      }
      outline.push(entry);
    }
    if (t[i].type === 'paragraph_open' && t[i + 1]?.type === 'inline') {
      const kids = t[i + 1].children.filter((c) => !(c.type === 'text' && c.content.trim() === ''));
      if (kids.length === 1 && kids[0].type === 'image') t[i].attrJoin('class', 'figure');
    }
    if (t[i].type === 'inline' && t[i - 2]?.type === 'list_item_open') {
      const first = t[i].children[0];
      const m = first?.type === 'text' && first.content.match(/^\[([ xX])\]\s+/);
      if (m) {
        first.content = first.content.slice(m[0].length);
        t[i].children.unshift(
          Object.assign(new state.Token('html_inline', '', 0), {
            content: `<span class="box${m[1] === ' ' ? '' : ' checked'}"></span>`,
          }),
        );
        t[i - 2].attrJoin('class', 'task');
      }
    }
  }
});

let diagramCount = 0;
md.renderer.rules.fence = (tokens, idx) => {
  const token = tokens[idx];
  const lang = (token.info || '').trim().split(/\s+/)[0].toLowerCase();
  const code = token.content.replace(/\n$/, '');
  if (lang === 'mermaid') {
    diagramCount += 1;
    return `<div class="diagram"><pre class="mermaid" data-n="${diagramCount}">${esc(code)}</pre></div>\n`;
  }
  code.split('\n').forEach((l, n) => {
    if (l.length > MAX_CODE_COLS) {
      warnings.push(`code line longer than ${MAX_CODE_COLS} chars (${l.length}) near source line ${(token.map?.[0] ?? 0) + n + 2 + ruleAt + 1}: ${l.slice(0, 60)}...`);
    }
  });
  // Short listings stay on one page; long ones may split so they do not leave half a page blank.
  const long = code.split('\n').length > LONG_LISTING_LINES ? ' long' : '';
  if (!lang || lang === 'text' || lang === 'txt' || lang === 'output') {
    return `<pre class="output${long}"><code>${esc(code)}</code></pre>\n`;
  }
  const html = hljs.getLanguage(lang)
    ? hljs.highlight(code, { language: lang, ignoreIllegals: true }).value
    : esc(code);
  return `<pre class="code${long}" data-lang="${esc(lang)}"><code>${html}</code></pre>\n`;
};

const MIME = { '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp' };
md.renderer.rules.image = (tokens, idx) => {
  const token = tokens[idx];
  const src = token.attrGet('src') || '';
  const alt = token.content || '';
  if (/^(https?:)?\/\//.test(src) || src.startsWith('data:')) {
    errors.push(`image must be a local file inside the source folder: ${src}`);
    return '';
  }
  const file = path.resolve(sourceDir, decodeURIComponent(src));
  const mime = MIME[path.extname(file).toLowerCase()];
  if (!fs.existsSync(file) || !mime) {
    errors.push(`image not found or unsupported type: ${src}`);
    return '';
  }
  if (!alt.trim()) warnings.push(`image has no alt text: ${src}`);
  const data = fs.readFileSync(file).toString('base64');
  return `<img src="data:${mime};base64,${data}" alt="${esc(alt)}">`;
};

md.renderer.rules.table_open = () => '<table>\n';

const coverHtml = `
<section class="cover">
  <div class="cover-top">${esc(series)}</div>
  <div class="cover-main">
    <h1 class="cover-title">${esc(title)}</h1>
    <p class="cover-edition">${esc(edition)}</p>
    ${promise ? `<p class="cover-promise">${md.renderInline(promise)}</p>` : ''}
  </div>
  <div class="cover-foot">Private study edition</div>
</section>`;

let bodyHtml = md.render(bodyMd);

// ------------------------------------------------------- contents and parts

const tocEntries = outline.filter((e) => e.level <= 2);
const tocRow = (e) => {
  const label =
    e.level === 1
      ? esc(e.kicker ? `${e.kicker} — ${e.name}` : e.text)
      : `${e.num ? `<span class="toc-num">${e.num}</span>` : '<span class="toc-num"></span>'}${esc(e.name || e.text)}`;
  return `<a class="toc-row toc-l${e.level}" href="#${e.id}"><span class="toc-text">${label}</span><span class="toc-dots"></span><span class="toc-page" data-dest="${e.id}"></span></a>`;
};
const tocHtml = `
<nav class="toc">
  <h2 class="toc-title" id="contents">Contents</h2>
  ${tocEntries.map(tocRow).join('\n  ')}
</nav>`;

// Each part opener lists its own chapters.
for (let i = 0; i < tocEntries.length; i++) {
  const part = tocEntries[i];
  if (part.level !== 1) continue;
  const chapters = [];
  for (let j = i + 1; j < tocEntries.length && tocEntries[j].level === 2; j++) chapters.push(tocEntries[j]);
  const mini = `<div class="part-contents">${chapters.map(tocRow).join('')}</div>`;
  const marker = new RegExp(`(<h1[^>]*id="${part.id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}"[^>]*>[\\s\\S]*?</h1>)`);
  bodyHtml = bodyHtml.replace(marker, `<section class="part-opener">$1${mini}</section>`);
}

// ------------------------------------------------------------- source checks

const knownIds = new Set(outline.map((e) => e.id).concat('contents'));
for (const m of bodyHtml.matchAll(/<a href="#([^"]*)"/g)) {
  const id = decodeURIComponent(m[1]);
  if (!knownIds.has(id)) errors.push(`internal link points to a heading that does not exist: #${id}`);
}

{
  const seen = new Map();
  let inFence = false;
  for (const block of bodyMd.split(/\n{2,}/)) {
    const fences = (block.match(/^```/gm) || []).length;
    if (inFence || fences) {
      if (fences % 2 === 1) inFence = !inFence;
      continue;
    }
    const text = block.trim().replace(/\s+/g, ' ');
    if (text.length < 140 || text.startsWith('|') || text.startsWith('![')) continue;
    seen.set(text, (seen.get(text) || 0) + 1);
  }
  for (const [text, n] of seen) {
    if (n > 1) warnings.push(`paragraph appears ${n} times: "${text.slice(0, 90)}..."`);
  }
}

// ----------------------------------------------------------------------- html

const css = fs.readFileSync(path.join(HERE, 'handbook.css'), 'utf8');
const pageCss = `
@page {
  size: Letter;
  margin: 0.95in 1in 0.95in 1in;
  @top-left { content: "${cssString(title)}"; font: 600 7.5pt "Avenir Next", "Helvetica Neue", Arial, sans-serif; letter-spacing: 0.09em; text-transform: uppercase; color: #6b7280; vertical-align: bottom; padding-bottom: 14pt; }
  @top-right { content: "${cssString(edition)}"; font: 500 7.5pt "Avenir Next", "Helvetica Neue", Arial, sans-serif; letter-spacing: 0.06em; color: #9ca3af; vertical-align: bottom; padding-bottom: 14pt; }
  @bottom-left { content: "${cssString(series)}"; font: 500 7.5pt "Avenir Next", "Helvetica Neue", Arial, sans-serif; letter-spacing: 0.06em; color: #9ca3af; vertical-align: top; padding-top: 14pt; }
  @bottom-right { content: counter(page); font: 600 8.5pt "Avenir Next", "Helvetica Neue", Arial, sans-serif; color: #4b5563; vertical-align: top; padding-top: 14pt; }
}
@page cover {
  margin: 0;
  @top-left { content: none; } @top-right { content: none; }
  @bottom-left { content: none; } @bottom-right { content: none; }
}
@page opener {
  @top-left { content: none; } @top-right { content: none; }
}`;

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${esc(title)} — ${esc(edition)}</title>
<meta name="author" content="EngineeringEverday">
<meta name="subject" content="${esc(series)}">
<style>${pageCss}\n${css}</style>
</head>
<body>
${coverHtml}
${tocHtml}
<main>
${bodyHtml}
</main>
</body>
</html>`;

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'handbook-'));
const htmlPath = keepHtml ? outputPath.replace(/\.pdf$/i, '') + '.html' : path.join(tmpDir, 'handbook.html');
fs.writeFileSync(htmlPath, html);

// ------------------------------------------------------------------------ pdf

const executablePath = CHROME_CANDIDATES.find((p) => fs.existsSync(p));
if (!executablePath) {
  console.error('error: Chrome not found. Set CHROME_PATH to a Chrome or Chromium binary.');
  process.exit(1);
}

function readDestinations(pdfPath) {
  try {
    const out = execFileSync('pdfinfo', ['-dests', pdfPath], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
    const map = {};
    for (const line of out.split('\n')) {
      const m = line.match(/^\s*(\d+)\s+\[.*\]\s+"(.*)"\s*$/);
      if (m) map[m[2]] = Number(m[1]);
    }
    return map;
  } catch {
    return null;
  }
}

const browser = await puppeteer.launch({ executablePath, headless: true, args: ['--no-sandbox', '--font-render-hinting=none'] });
try {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  if (diagramCount > 0) {
    await page.addScriptTag({ path: path.join(HERE, 'node_modules/mermaid/dist/mermaid.min.js') });
    const diagramErrors = await page.evaluate(async () => {
      /* global mermaid */
      const font = '"Helvetica Neue", Helvetica, Arial, sans-serif';
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: 'base',
        fontFamily: font,
        themeVariables: {
          fontFamily: font,
          fontSize: '13px',
          primaryColor: '#eef2ff',
          primaryBorderColor: '#4f46e5',
          primaryTextColor: '#1f2937',
          secondaryColor: '#f8fafc',
          secondaryBorderColor: '#cbd5e1',
          tertiaryColor: '#ffffff',
          tertiaryBorderColor: '#cbd5e1',
          lineColor: '#6b7280',
          textColor: '#1f2937',
          noteBkgColor: '#fef3c7',
          noteBorderColor: '#b45309',
          noteTextColor: '#1f2937',
          actorBkg: '#eef2ff',
          actorBorder: '#4f46e5',
          signalColor: '#374151',
          signalTextColor: '#1f2937',
          labelBoxBkgColor: '#f8fafc',
          labelBoxBorderColor: '#cbd5e1',
          activationBkgColor: '#e0e7ff',
          activationBorderColor: '#4f46e5',
          edgeLabelBackground: '#ffffff',
          clusterBkg: '#f8fafc',
          clusterBorder: '#cbd5e1',
        },
        flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis', padding: 10, nodeSpacing: 34, rankSpacing: 36 },
        sequence: {
          useMaxWidth: true, mirrorActors: false, messageMargin: 32, width: 112, height: 42,
          actorMargin: 34, boxMargin: 8, noteMargin: 10,
          // Measure text with the same font it is drawn in, or notes overflow their boxes.
          actorFontFamily: font, messageFontFamily: font, noteFontFamily: font,
          actorFontSize: 13, messageFontSize: 13, noteFontSize: 13,
        },
        state: { useMaxWidth: true },
        er: { useMaxWidth: true },
      });
      const problems = [];
      const small = [];
      for (const pre of document.querySelectorAll('pre.mermaid')) {
        const code = pre.textContent;
        const n = pre.dataset.n;
        try {
          const { svg } = await mermaid.render(`diagram-${n}`, code);
          const holder = document.createElement('div');
          holder.className = 'diagram-svg';
          holder.innerHTML = svg;
          pre.replaceWith(holder);
          // Mermaid draws at screen size; print it a little smaller so diagram
          // text sits close to table text instead of shouting over the body.
          const el = holder.querySelector('svg');
          const natural = parseFloat(el.style.maxWidth) || el.viewBox.baseVal.width;
          if (natural) el.style.maxWidth = `${Math.round(natural * 0.86)}px`;
          // A note over two participants is only as wide as the gap between them.
          for (const rect of holder.querySelectorAll('rect.note')) {
            const text = rect.parentNode.querySelector('text.noteText');
            if (text && text.getBBox().width > rect.getBBox().width - 6) {
              small.push(`diagram ${n}: the note "${text.textContent.trim()}" is wider than its box; shorten it`);
            }
          }
          // The text column is 6.5in (624 CSS px). Anything wider is shrunk to fit.
          const shrink = natural ? 624 / (natural * 0.86) : 1;
          if (shrink < 0.8) {
            small.push(`diagram ${n} (starts "${code.split('\n')[0]}") is ${Math.round(natural)}px wide and prints at ${Math.round(shrink * 100)}% size, so its text will be small: make it narrower (flowchart LR, fewer boxes per row, shorter labels)`);
          }
        } catch (e) {
          problems.push(`diagram ${n} (starts "${code.split('\n')[0]}"): ${String(e.message || e).split('\n').slice(0, 4).join(' | ')}`);
          document.querySelectorAll(`#ddiagram-${n}, #diagram-${n}`).forEach((el) => el.remove());
        }
      }
      return { problems, small };
    });
    diagramErrors.problems.forEach((e) => errors.push(`mermaid ${e}`));
    diagramErrors.small.forEach((w) => warnings.push(w));
    if (process.env.HANDBOOK_DEBUG) {
      const sizes = await page.evaluate(() =>
        [...document.querySelectorAll('.diagram-svg svg')].map((s) => {
          const r = s.getBoundingClientRect();
          return `${s.id} ${Math.round(r.width)}x${Math.round(r.height)} style="${s.getAttribute('style')}" width=${s.getAttribute('width')} height=${s.getAttribute('height')} viewBox=${s.getAttribute('viewBox')}`;
        }),
      );
      sizes.forEach((l) => console.log('debug:', l));
    }
  }

  if (errors.length) throw new Error('build stopped');

  const pdfOptions = { path: outputPath, preferCSSPageSize: true, printBackground: true, outline: true, tagged: true, timeout: 180000 };
  await page.pdf(pdfOptions);

  // Second pass: read where each heading landed and print those page numbers in
  // the contents. Repeats if writing the numbers moved anything.
  let dests = readDestinations(outputPath);
  if (!dests) {
    warnings.push('pdfinfo (poppler) not found: contents pages have no page numbers');
  } else {
    for (let pass = 0; pass < 4; pass++) {
      await page.evaluate((map) => {
        document.querySelectorAll('.toc-page').forEach((el) => {
          el.textContent = map[el.dataset.dest] ?? '';
        });
      }, dests);
      await page.pdf(pdfOptions);
      const next = readDestinations(outputPath);
      const stable = next && Object.keys(next).every((k) => next[k] === dests[k]);
      dests = next || dests;
      if (stable) break;
    }
  }
} catch (e) {
  if (e.message !== 'build stopped') errors.push(String(e.stack || e));
} finally {
  await browser.close();
  if (!keepHtml) fs.rmSync(tmpDir, { recursive: true, force: true });
}

warnings.forEach((w) => console.warn(`warning: ${w}`));
if (errors.length) {
  errors.forEach((e) => console.error(`error: ${e}`));
  console.error(`\n${errors.length} error(s). No PDF was accepted.`);
  if (fs.existsSync(outputPath)) fs.rmSync(outputPath);
  process.exit(1);
}

let pages = '?';
try {
  pages = execFileSync('pdfinfo', [outputPath], { encoding: 'utf8' }).match(/Pages:\s+(\d+)/)[1];
} catch {}
const words = bodyMd.split(/\s+/).filter(Boolean).length;
console.log(`built ${path.basename(outputPath)}: ${pages} pages, ${words} words, ${outline.filter((e) => e.level === 2).length} chapters, ${diagramCount} diagrams, ${warnings.length} warning(s)`);
