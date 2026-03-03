#!/usr/bin/env python3
"""Convert Markdown to PDF using fpdf2. Handles tables, code blocks, lists, headings.

CRITICAL: For numbered/bullet lists, always use a SINGLE multi_cell() call per item
with the number/bullet prepended to the text. NEVER use cell() + multi_cell() combos
for list items — fpdf2 breaks page handling across that pattern and content gets cut off.
"""

import re
import sys
from fpdf import FPDF

FONT_DIR = "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/matplotlib/mpl-data/fonts/ttf"

BODY_SIZE = 9
BODY_LH = 5.5


class MarkdownPDF(FPDF):
    def __init__(self, header_text=""):
        super().__init__(orientation="P", unit="mm", format="letter")
        self.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
        self.add_font("DejaVuMono", "", f"{FONT_DIR}/DejaVuSansMono.ttf")
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(15, 15, 15)
        self._header_text = header_text

    def header(self):
        if self.page_no() > 1 and self._header_text:
            self.set_font("DejaVu", "", 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 6, self._header_text, align="R",
                      new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(220, 220, 220)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    @property
    def cw(self):
        return self.w - self.l_margin - self.r_margin

    def check_page(self, needed=25):
        if self.get_y() + needed > self.h - 20:
            self.add_page()

    def wrapped_line_count(self, text, width, font_family="DejaVu", style="", size=8):
        self.set_font(font_family, style, size)
        if width <= 4:
            return 1
        words = text.split()
        if not words:
            return 1
        lines = 1
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if self.get_string_width(test) <= width:
                current = test
            else:
                if current:
                    lines += 1
                current = word
        return lines


def clean_md(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    return text


def parse_table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            rows.append(cells)
    if len(rows) < 2:
        return None, None
    headers = rows[0]
    data = [r for r in rows[1:] if not all(re.match(r"^[-:]+$", c) for c in r)]
    return headers, data


def compute_col_widths(pdf, headers, rows, aw, fs):
    nc = len(headers)
    pad = 4
    nw = []
    for i in range(nc):
        pdf.set_font("DejaVu", "B", fs)
        mx = pdf.get_string_width(clean_md(headers[i])) + pad
        pdf.set_font("DejaVu", "", fs)
        for row in rows:
            if i < len(row):
                mx = max(mx, pdf.get_string_width(clean_md(row[i])) + pad)
        nw.append(mx)

    total = sum(nw)
    if total <= aw:
        return [w / total * aw for w in nw]

    fair = aw / nc
    fixed, flex, ft = [], [], 0
    for i, w in enumerate(nw):
        if w <= fair * 1.2:
            fixed.append(i)
            ft += w
        else:
            flex.append(i)

    rem = aw - ft
    if flex and rem > 0:
        fn = sum(nw[i] for i in flex)
        cw = [0.0] * nc
        for i in fixed:
            cw[i] = nw[i]
        for i in flex:
            cw[i] = max(18, (nw[i] / fn) * rem)
    else:
        cw = [max(18, (w / total) * aw) for w in nw]

    t = sum(cw)
    return [(w / t) * aw for w in cw]


def render_table(pdf, headers, rows):
    if not headers:
        return
    nc = len(headers)
    aw = pdf.cw

    if nc >= 6:
        fs, lh = 6.5, 4
    elif nc >= 5:
        fs, lh = 7, 4.5
    else:
        fs, lh = 8, 5

    cw = compute_col_widths(pdf, headers, rows, aw, fs)
    cw = [max(w, 12) for w in cw]
    t = sum(cw)
    cw = [(w / t) * aw for w in cw]
    cp = 2

    def smc(width, height, text, **kw):
        pdf.multi_cell(max(width, 6), height, text, **kw)

    def draw_hdr():
        pdf.set_font("DejaVu", "B", fs)
        pdf.set_fill_color(40, 40, 40)
        pdf.set_text_color(255, 255, 255)
        y0, x0 = pdf.get_y(), pdf.l_margin
        hl = []
        for i, h in enumerate(headers):
            lc = pdf.wrapped_line_count(clean_md(h), max(cw[i] - cp, 6), "DejaVu", "B", fs)
            hl.append(lc)
        hh = max(hl) * lh + 2
        for i, h in enumerate(headers):
            x = x0 + sum(cw[:i])
            pdf.rect(x, y0, cw[i], hh, "DF")
            pdf.set_xy(x + 1, y0 + 1)
            smc(cw[i] - cp, lh, clean_md(h), border=0, align="L")
        pdf.set_xy(x0, y0 + hh)

    pdf.check_page(40)
    draw_hdr()

    for ri, row in enumerate(rows):
        pdf.set_font("DejaVu", "", fs)
        pdf.set_text_color(30, 30, 30)
        cr = [clean_md(row[i]) if i < len(row) else "" for i in range(nc)]
        rlc = [pdf.wrapped_line_count(cr[i], max(cw[i] - cp, 6), "DejaVu", "", fs) for i in range(nc)]
        rh = max(max(rlc) * lh + 1, lh + 1)

        if pdf.get_y() + rh > pdf.h - 20:
            pdf.add_page()
            pdf.set_font("DejaVu", "B", fs)
            draw_hdr()
            pdf.set_font("DejaVu", "", fs)
            pdf.set_text_color(30, 30, 30)

        y0, x0 = pdf.get_y(), pdf.l_margin
        fill = ri % 2 == 0
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255, 255, 255)

        for i in range(nc):
            x = x0 + sum(cw[:i])
            pdf.rect(x, y0, cw[i], rh, "DF" if fill else "D")
            pdf.set_xy(x + 1, y0 + 0.5)
            pdf.set_text_color(30, 30, 30)
            smc(cw[i] - cp, lh, cr[i], border=0, align="L")

        pdf.set_xy(x0, y0 + rh)
    pdf.ln(5)


def render_code(pdf, lines):
    if not lines:
        return
    lh = 4.5
    bh = len(lines) * lh + 6
    aw = pdf.cw
    if bh > pdf.h - 40:
        pdf.set_font("DejaVuMono", "", 7.5)
        pdf.set_text_color(40, 40, 40)
        for cl in lines:
            if pdf.get_y() + lh > pdf.h - 20:
                pdf.add_page()
            pdf.set_fill_color(243, 243, 243)
            pdf.cell(aw, lh, f"  {cl}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        return
    pdf.check_page(bh + 5)
    y0 = pdf.get_y()
    pdf.set_fill_color(243, 243, 243)
    pdf.set_draw_color(210, 210, 210)
    pdf.rect(pdf.l_margin, y0, aw, bh, "DF")
    pdf.set_font("DejaVuMono", "", 7.5)
    pdf.set_text_color(40, 40, 40)
    pdf.set_xy(pdf.l_margin + 4, y0 + 3)
    for cl in lines:
        pdf.cell(aw - 8, lh, cl, new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(pdf.l_margin + 4)
    pdf.set_xy(pdf.l_margin, y0 + bh + 2)


def render(pdf, md):
    lines = md.split("\n")
    i = 0
    in_code = False
    code_buf = []

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            if in_code:
                render_code(pdf, code_buf)
                code_buf = []
                in_code = False
            else:
                in_code = True
                code_buf = []
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # Table
        if line.strip().startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            tl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tl.append(lines[i])
                i += 1
            h, r = parse_table(tl)
            if h and r:
                render_table(pdf, h, r)
            continue

        # HR
        if line.strip() in ("---", "***", "___"):
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.l_margin, pdf.get_y() + 3, pdf.w - pdf.r_margin, pdf.get_y() + 3)
            pdf.ln(8)
            i += 1
            continue

        s = line.strip()

        # H1
        if line.startswith("# "):
            if pdf.page_no() > 1 and pdf.get_y() > 50:
                pdf.add_page()
            pdf.set_font("DejaVu", "B", 20)
            pdf.set_text_color(20, 20, 20)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.cw, 10, s[2:])
            pdf.ln(3)
            i += 1
            continue

        # H2
        if line.startswith("## "):
            pdf.check_page(45)
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 15)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.cw, 8, s[3:])
            pdf.set_draw_color(80, 80, 80)
            pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
            pdf.ln(4)
            i += 1
            continue

        # H3
        if line.startswith("### "):
            pdf.check_page(35)
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 12)
            pdf.set_text_color(40, 40, 40)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.cw, 7, s[4:])
            pdf.ln(2)
            i += 1
            continue

        # H4
        if line.startswith("#### "):
            pdf.check_page(20)
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.cw, 6, s[5:])
            pdf.ln(2)
            i += 1
            continue

        # Bold-only line
        if s.startswith("**") and s.endswith("**") and s.count("**") == 2:
            text = s[2:-2]
            pdf.check_page(12)
            pdf.set_font("DejaVu", "B", BODY_SIZE)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(pdf.cw, BODY_LH, text)
            pdf.ln(1)
            i += 1
            continue

        # Checklist
        if s.startswith("- [ ]") or s.startswith("- [x]"):
            text = clean_md(s[5:].strip())
            prefix = "[x] " if s.startswith("- [x]") else "[ ] "
            combined = prefix + text
            pdf.set_font("DejaVu", "", BODY_SIZE)
            pdf.set_text_color(30, 30, 30)
            w = pdf.cw
            lc = pdf.wrapped_line_count(combined, w, "DejaVu", "", BODY_SIZE)
            pdf.check_page(lc * BODY_LH + 1)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(w, BODY_LH, combined)
            i += 1
            continue

        # Numbered list — single multi_cell with number prepended
        m = re.match(r"^(\d+)\.\s+(.*)", s)
        if m:
            num, text = m.group(1), clean_md(m.group(2))
            combined = f"{num}.  {text}"
            pdf.set_font("DejaVu", "", BODY_SIZE)
            pdf.set_text_color(30, 30, 30)
            w = pdf.cw
            lc = pdf.wrapped_line_count(combined, w, "DejaVu", "", BODY_SIZE)
            pdf.check_page(lc * BODY_LH + 1)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(w, BODY_LH, combined)
            i += 1
            continue

        # Bullet — single multi_cell with bullet prepended
        indent_match = re.match(r"^(\s*)- (.*)", line)
        if indent_match:
            indent = len(indent_match.group(1))
            text = clean_md(indent_match.group(2))
            imm = min(indent, 8) * 2
            bullet = "  -  " if indent > 0 else "  •  "
            combined = bullet + text
            pdf.set_font("DejaVu", "", BODY_SIZE)
            pdf.set_text_color(30, 30, 30)
            w = pdf.cw - imm
            lc = pdf.wrapped_line_count(combined, w, "DejaVu", "", BODY_SIZE)
            pdf.check_page(lc * BODY_LH + 1)
            pdf.set_x(pdf.l_margin + imm)
            pdf.multi_cell(w, BODY_LH, combined)
            i += 1
            continue

        # Empty
        if s == "":
            pdf.ln(2)
            i += 1
            continue

        # Paragraph
        text = clean_md(s)
        if text:
            pdf.set_font("DejaVu", "", BODY_SIZE)
            pdf.set_text_color(30, 30, 30)
            w = pdf.cw
            lc = pdf.wrapped_line_count(text, w, "DejaVu", "", BODY_SIZE)
            pdf.check_page(lc * BODY_LH + 1)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(w, BODY_LH, text)
        i += 1


def convert(input_path, output_path, title="", subtitle="", header_text="", date_str=""):
    """Convert a markdown file to PDF."""
    with open(input_path, "r") as f:
        md = f.read()

    pdf = MarkdownPDF(header_text=header_text)
    pdf.add_page()

    if title:
        pdf.ln(50)
        pdf.set_font("DejaVu", "B", 30)
        pdf.set_text_color(20, 20, 20)
        pdf.cell(0, 14, title, align="C", new_x="LMARGIN", new_y="NEXT")
        if subtitle:
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 17)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 10, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(pdf.w * 0.3, pdf.get_y(), pdf.w * 0.7, pdf.get_y())
        pdf.ln(10)
        if date_str:
            pdf.set_font("DejaVu", "", 11)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 7, date_str, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.add_page()

    render(pdf, md)
    pdf.output(output_path)
    print(f"PDF saved to: {output_path} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    INPUT = "input.md"  # Replace with your markdown file path
    OUTPUT = "output.pdf"  # Replace with your desired output path

    # Skip the first few lines (title/date) since we render a custom title page
    with open(INPUT, "r") as f:
        md = f.read()

    start = md.find("## Pre-Build Checklist")
    content = md[start:] if start != -1 else md

    # Write trimmed content to temp file for conversion
    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
    tmp.write(content)
    tmp.close()

    convert(
        tmp.name,
        OUTPUT,
        title="MOGANO",
        subtitle="Meta Ads Campaign Build Guide",
        header_text="MOGANO  -  Meta Ads Campaign Build Guide",
        date_str="Step-by-step instructions for all 4 campaigns  |  $2,300/mo  |  February 21, 2026",
    )

    os.unlink(tmp.name)
