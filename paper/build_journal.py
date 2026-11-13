"""Professional journal-format builder (v2).

Fixes the two problems of the first builds:
  * all text is black Times New Roman (no blue Word heading colours),
  * hard-wrapped Markdown lines are merged into real paragraphs, so the
    pages are dense like a real journal instead of sparse.

Usage (from project root):
  python paper/build_journal.py paper/paper_ieee.md --two-col
  python paper/build_journal.py paper/paper_full.md
Outputs <name>.docx and <name>.pdf next to the source file.
"""
import re
import subprocess
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLACK = RGBColor(0, 0, 0)
TWO_COL = "--two-col" in sys.argv
SRC = [a for a in sys.argv[1:] if not a.startswith("--")][0]
OUT = SRC.rsplit(".", 1)[0] + ".docx"


def add_rich(par, text, size=10, italic_all=False):
    tokens = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            run = par.add_run(tok[2:-2]); run.bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            run = par.add_run(tok[1:-1]); run.italic = True
        else:
            run = par.add_run(tok)
        run.font.size = Pt(size)
        run.font.color.rgb = BLACK
        run.font.name = "Times New Roman"
        if italic_all:
            run.italic = True


def heading(doc, text, level, size):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    run.bold = True
    run.font.size = Pt(size)
    run.font.color.rgb = BLACK
    run.font.name = "Times New Roman"
    return h


def set_columns(section, num, space_twips=360):
    cols = OxmlElement("w:cols")
    cols.set(qn("w:num"), str(num))
    cols.set(qn("w:space"), str(space_twips))
    section._sectPr.append(cols)


def blocks(lines):
    """Yield ('para'|'bullet'|'heading1'|'heading2'|'heading3'|'title'|
    'image'|'table', payload) with wrapped lines merged."""
    buf, kind = [], None

    def flush():
        nonlocal buf, kind
        if buf:
            yield (kind or "para", " ".join(buf))
        buf, kind = [], None

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1
        if line.startswith("# "):
            yield from flush(); yield ("title", line[2:]); continue
        if line.startswith("## "):
            yield from flush(); yield ("heading1", line[3:]); continue
        if line.startswith("### "):
            yield from flush(); yield ("heading2", line[4:]); continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if m:
            yield from flush(); yield ("image", m.group(2)); continue
        if line.startswith("|"):
            yield from flush()
            rows = []
            while True:
                rows.append([c.strip() for c in line.strip().strip("|").split("|")])
                if i < len(lines) and lines[i].startswith("|"):
                    line = lines[i].rstrip(); i += 1
                else:
                    break
            rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
            yield ("table", rows); continue
        if not line.strip() or line.strip() == "---":
            yield from flush(); continue
        if line.startswith("- "):
            yield from flush()
            buf, kind = [line[2:]], "bullet"; continue
        buf.append(line)
    yield from flush()


def main():
    lines = open(SRC, encoding="utf-8").read().splitlines()
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(10)
    normal.font.color.rgb = BLACK
    for section in doc.sections:
        section.top_margin = Inches(0.7); section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.7); section.right_margin = Inches(0.7)

    in_header = True   # title block before the Abstract heading
    body_started = False
    img_w = Inches(3.3) if TWO_COL else Inches(5.8)

    for kind, payload in blocks(lines):
        if kind == "heading1" and payload.strip().lower().startswith("1. introduction") \
                and TWO_COL and not body_started:
            section = doc.add_section(WD_SECTION.CONTINUOUS)
            section.top_margin = Inches(0.7); section.bottom_margin = Inches(0.7)
            section.left_margin = Inches(0.7); section.right_margin = Inches(0.7)
            set_columns(section, 2)
            body_started = True
        if kind == "title":
            h = heading(doc, payload, 0, 16)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            in_header = True
            continue
        if kind == "heading1":
            if payload.strip().lower() == "abstract":
                in_header = False
            heading(doc, payload, 1, 11.5)
            continue
        if kind == "heading2":
            heading(doc, payload, 2, 10.5)
            continue
        if kind == "image":
            path = payload.replace("../", "", 1)
            doc.add_picture(path, width=img_w)
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue
        if kind == "table":
            table = doc.add_table(rows=len(payload), cols=len(payload[0]))
            table.style = "Light Grid Accent 1"
            for r, row in enumerate(payload):
                for c, val in enumerate(row):
                    cell = table.cell(r, c)
                    cell.text = ""
                    add_rich(cell.paragraphs[0], val, size=8.5)
                    if r == 0:
                        for run in cell.paragraphs[0].runs:
                            run.bold = True
            continue
        # paragraphs / bullets / captions
        text = payload
        is_caption = (text.startswith("*Figure") or text.startswith("*Table")
                      or text.startswith("*R²")) and text.endswith("*")
        if is_caption:
            text = text.strip("*")
        par = doc.add_paragraph(style="List Bullet" if kind == "bullet" else "Normal")
        add_rich(par, text, size=9 if is_caption else 10, italic_all=is_caption)
        if is_caption:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif in_header:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.save(OUT)
    print("wrote", OUT)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", OUT,
                    "--outdir", "paper"], check=True, capture_output=True,
                   timeout=240)
    print("wrote", OUT.rsplit(".", 1)[0] + ".pdf")


if __name__ == "__main__":
    main()
