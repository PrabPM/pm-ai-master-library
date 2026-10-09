# Handbook PDF builder

Turns a handbook's Markdown source into the reader PDF: cover, contents with page
numbers, part openers, syntax-highlighted code, rendered diagrams and bookmarks.

```bash
cd tools/handbook-pdf
npm install
node build.mjs ../../05-source-documents/curriculum/volume-5-sql-handbook-for-business-analysts-v2.md \
  ../../01-curriculum/04-sql-and-data/volume-5-sql-handbook-for-business-analysts-v2.pdf
```

Requirements: Node 20 or later, Google Chrome (or set `CHROME_PATH`), and `pdfinfo`
from poppler for the page numbers in the contents (`brew install poppler`).

## What the source may contain

Plain GitHub-flavored Markdown, so the same file also reads well on GitHub.

| Element | How to write it |
|---|---|
| Cover | `# Title`, then `**Edition** · Series`, then a `> promise` line, closed by a line containing only `---` |
| Part | `# Part I — Name` (gets its own opener page listing its chapters) |
| Chapter | `## 7. Name` (starts a new page) |
| Callout | GitHub alerts: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]` |
| Diagram | a fenced `mermaid` block |
| Figure | `![alt](volume-4-assets/name.svg)` with a local file |
| Caption | a paragraph in italics that starts with `Figure` or `Table` |
| Output | a line ending in `Result:` or `Output:` followed by a fenced `text` block |

## Checks the build runs

The build stops without writing a PDF if a diagram does not parse, an image is
missing, or an internal `#link` points at a heading that does not exist. It warns
about any paragraph that appears more than once and about code lines longer than
88 characters.
