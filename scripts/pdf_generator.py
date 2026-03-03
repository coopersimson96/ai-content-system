#!/usr/bin/env python3
"""
Generic professional PDF generator.

Clean, modern design: white backgrounds, blue accents, professional typography.
No branding — designed for any creator to use as-is or customize.

Usage:
    python3 pdf_generator.py --content-file content.json --output output.pdf

JSON content format:
{
    "type": "setup-guide|cheatsheet|quick-reference|how-to-guide|checklist",
    "title": "Document Title",
    "subtitle": "Optional subtitle text",
    "subtitle_bullets": ["Bullet 1", "Bullet 2"],
    "footer_text": "Your Footer Text | 2026",
    "sections": [
        {"type": "section_title", "number": "01", "title": "Section Name"},
        {"type": "body", "text": "Paragraph text."},
        {"type": "heading", "text": "Heading text"},
        {"type": "bullets", "items": ["Item 1", "Item 2"]},
        {"type": "code_block", "code": "code here"},
        {"type": "tip_box", "title": "Pro Tip", "text": "Tip text."},
        {"type": "table", "headers": ["Col 1", "Col 2"], "rows": [["A", "B"]]},
        {"type": "checklist", "items": ["Check item 1", "Check item 2"]},
        {"type": "numbered_steps", "steps": [{"title": "Step 1", "description": "Do this"}]},
        {"type": "two_column", "items": [["Label", "Value"], ["Label2", "Value2"]]},
        {"type": "callout_box", "title": "Important", "items": ["Item 1"]},
        {"type": "resources", "items": ["Resource 1", "Resource 2"]},
        {"type": "page_break"}
    ]
}
"""

import argparse
import json
import sys
from pathlib import Path

from fpdf import FPDF


MAX_PAGES = 6

_FONT_DIR = Path.home() / "Library" / "Fonts"


class ProfessionalDoc(FPDF):
    """Clean, modern professional PDF — white bg, blue accents, sharp layout."""

    # ── Color System (neutral professional palette) ───────
    WHITE = (255, 255, 255)
    LIGHT_BG = (248, 249, 250)        # subtle gray background
    DARK_BG = (243, 244, 246)          # slightly darker for striping
    CHARCOAL = (31, 41, 55)            # primary text
    CHARCOAL_LIGHT = (55, 65, 81)      # secondary text
    BLUE = (37, 99, 235)               # primary accent
    BLUE_LIGHT = (59, 130, 246)        # lighter blue
    BLUE_BG = (239, 246, 255)          # very light blue tint
    AMBER = (217, 119, 6)              # secondary accent (tips/warnings)
    AMBER_BG = (255, 251, 235)         # very light amber tint
    GRAY = (107, 114, 128)             # muted body text
    LIGHT_GRAY = (156, 163, 175)       # subtle text
    BORDER = (229, 231, 235)           # subtle borders
    CODE_BG = (31, 41, 55)             # dark code blocks
    CODE_TEXT = (248, 249, 250)

    # ── Layout ────────────────────────────────────────────
    MARGIN = 20
    HEADER_BAR_H = 2
    FOOTER_H = 10

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=22)
        self.set_margin(self.MARGIN)
        self._footer_text = "Generated with AI Content System"
        self._is_cover_page = True
        self._doc_title = ""
        self._register_fonts()

    def _register_fonts(self):
        fd = _FONT_DIR
        self.add_font("Montserrat", "", str(fd / "Montserrat-Regular.ttf"))
        self.add_font("Montserrat", "B", str(fd / "Montserrat-Bold.ttf"))
        self.add_font("MontserratSB", "", str(fd / "Montserrat-SemiBold.ttf"))
        self.add_font("Poppins", "", str(fd / "Poppins-Regular.ttf"))
        self.add_font("Poppins", "B", str(fd / "Poppins-Bold.ttf"))
        self.add_font("PoppinsMed", "", str(fd / "Poppins-Medium.ttf"))
        self.add_font("PoppinsSB", "", str(fd / "Poppins-SemiBold.ttf"))
        self.add_font("RobotoMono", "", str(fd / "RobotoMono-Regular.ttf"))
        self.add_font("RobotoMono", "B", str(fd / "RobotoMono-Medium.ttf"))

    # ── helpers ───────────────────────────────────────────

    def _color(self, rgb):
        self.set_text_color(*rgb)

    def _bg(self, rgb):
        self.set_fill_color(*rgb)

    def _draw(self, rgb):
        self.set_draw_color(*rgb)

    def _check_page_limit(self):
        return self.page > MAX_PAGES

    def _ensure_space(self, needed_h):
        remaining = self.h - self.b_margin - self.get_y()
        if remaining < needed_h:
            self.add_page()

    @staticmethod
    def _clean(text):
        import re
        text = text.replace('\u2192', '->')
        text = re.sub(
            r'[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F'
            r'\U0000200D\U00002600-\U000026FF\U00002B50]+',
            '', text,
        )
        return text.strip()

    def _sharp_rect(self, x, y, w, h, fill_color, border_color=None, border_w=0):
        """Draw a sharp-cornered rectangle with optional border."""
        with self.local_context():
            self._bg(fill_color)
            if border_color and border_w > 0:
                self._draw(border_color)
                self.set_line_width(border_w)
                self.rect(x, y, w, h, style="FD")
            else:
                self.rect(x, y, w, h, style="F")

    def _offset_shadow(self, x, y, w, h, offset=2):
        """Draw a solid offset shadow."""
        with self.local_context():
            self._bg(self.BORDER)
            self.rect(x + offset, y + offset, w, h, style="F")

    def _bordered_card(self, x, y, w, h, fill=None, border_w=1, shadow_offset=2):
        """Draw a card with border and subtle offset shadow."""
        fill = fill or self.WHITE
        self._offset_shadow(x, y, w, h, offset=shadow_offset)
        self._sharp_rect(x, y, w, h, fill, self.BORDER, border_w)

    def _divider(self, y=None):
        """Draw a thin horizontal divider."""
        if y is None:
            y = self.get_y()
        with self.local_context():
            self._draw(self.BORDER)
            self.set_line_width(0.5)
            self.line(self.l_margin, y, self.w - self.r_margin, y)

    # ── page headers & footers ────────────────────────────

    def header(self):
        if self._is_cover_page:
            return
        # Blue top bar
        self._sharp_rect(0, 0, self.w, self.HEADER_BAR_H, self.BLUE)
        # Title in small caps
        self.set_y(self.HEADER_BAR_H + 2)
        self.set_font("Montserrat", "B", 6.5)
        self._color(self.LIGHT_GRAY)
        title_upper = self._doc_title.upper()[:60]
        self.cell(0, 4, title_upper, align="C")
        self.set_y(self.HEADER_BAR_H + 8)

    def footer(self):
        self.set_y(-self.FOOTER_H - 2)
        # Divider line
        with self.local_context():
            self._draw(self.BORDER)
            self.set_line_width(0.5)
            self.line(self.MARGIN, self.get_y(), self.w - self.MARGIN, self.get_y())
        self.ln(3)
        self.set_font("Montserrat", "", 6)
        self._color(self.LIGHT_GRAY)
        self.cell(0, 4, self._footer_text.upper(), align="L")
        self.set_x(-self.MARGIN)
        self._color(self.BLUE)
        self.set_font("Montserrat", "B", 7)
        self.cell(0, 4, f"{self.page_no():02d}", align="R")

    # ── Cover Page ────────────────────────────────────────

    def render_cover(self, title, subtitle=None, subtitle_bullets=None):
        self.add_page()
        self._is_cover_page = True
        self._doc_title = title

        # White background
        self._sharp_rect(0, 0, self.w, self.h, self.WHITE)

        # Top: blue bar
        bar_h = 4
        self._sharp_rect(0, 0, self.w, bar_h, self.BLUE)

        # Category label
        self.set_y(bar_h + 12)
        self.set_font("Montserrat", "B", 8)
        self._color(self.BLUE)
        # Blue dot + label
        dot_x = self.l_margin
        dot_y = self.get_y() + 1.5
        with self.local_context():
            self._bg(self.BLUE)
            self.ellipse(dot_x, dot_y, 2.5, 2.5, style="F")
        self.set_x(dot_x + 5)
        self.cell(0, 5, "GUIDE", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        # Title — large uppercase
        self.set_font("Montserrat", "B", 32)
        self._color(self.CHARCOAL)
        self.multi_cell(0, 13, title.upper(), align="L")
        self.ln(2)

        # Divider
        self._divider()
        self.ln(5)

        # Subtitle
        if subtitle:
            self.set_font("Poppins", "", 11)
            self._color(self.GRAY)
            self.multi_cell(self.epw * 0.75, 6, subtitle, align="L")
            self.ln(4)

        # "What You'll Learn" — bordered card with bullets
        if subtitle_bullets:
            card_x = self.l_margin
            card_w = self.epw
            text_w = card_w - 28

            # Pre-calculate card height
            self.set_font("Poppins", "", 9)
            total_bullet_h = 0
            for item in subtitle_bullets:
                n_lines = max(1, len(item) * self.get_string_width("x") / text_w + 0.5)
                total_bullet_h += max(7, int(n_lines) * 5.5 + 2)
            card_h = total_bullet_h + 24

            self._bordered_card(card_x, self.get_y(), card_w, card_h, fill=self.WHITE, border_w=1.5, shadow_offset=3)

            y_top = self.get_y()

            # Blue accent bar on left edge
            self._sharp_rect(card_x, y_top, 4, card_h, self.BLUE)

            # Section number
            self.set_xy(card_x + 10, y_top + 5)
            self.set_font("Montserrat", "B", 8)
            self._color(self.BLUE)
            self.cell(10, 5, "01", new_x="RIGHT", new_y="TOP")

            # Dash
            with self.local_context():
                self._draw(self.BORDER)
                self.set_line_width(0.5)
                self.line(self.get_x() + 2, y_top + 7.5, self.get_x() + 8, y_top + 7.5)

            # Label
            self.set_xy(self.get_x() + 10, y_top + 5)
            self._color(self.LIGHT_GRAY)
            self.set_font("Montserrat", "B", 7)
            self.cell(0, 5, "WHAT YOU'LL LEARN", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

            # Bullet items
            for item in subtitle_bullets:
                self.set_x(card_x + 10)
                # Blue checkmark square
                ck_x = self.get_x()
                ck_y = self.get_y() + 0.5
                self._sharp_rect(ck_x, ck_y, 4.5, 4.5, self.BLUE)
                # White checkmark
                with self.local_context():
                    self._draw(self.WHITE)
                    self.set_line_width(0.6)
                    self.line(ck_x + 1, ck_y + 2.5, ck_x + 2, ck_y + 3.5)
                    self.line(ck_x + 2, ck_y + 3.5, ck_x + 3.8, ck_y + 1)

                # Item text
                self.set_x(ck_x + 8)
                self._color(self.CHARCOAL)
                self.set_font("Poppins", "", 9)
                self.multi_cell(text_w, 5.5, item)
                self.ln(1)

            self.set_y(y_top + card_h + 4)

        self._is_cover_page = False

    # ── Section Title ─────────────────────────────────────

    def render_section_title(self, num, title):
        if self._check_page_limit():
            return
        self._ensure_space(26)
        self.ln(8)

        y = self.get_y()

        # Bottom border
        border_y = y + 14
        with self.local_context():
            self._draw(self.CHARCOAL)
            self.set_line_width(1.5)
            self.line(self.l_margin, border_y, self.w - self.r_margin, border_y)

        # Number — large blue
        self.set_xy(self.l_margin, y)
        self.set_font("Montserrat", "B", 16)
        self._color(self.BLUE)
        num_str = str(num).zfill(2) if num else ""
        if num_str:
            self.cell(12, 12, num_str, new_x="RIGHT", new_y="TOP")

            # Dash
            dash_x = self.get_x() + 2
            with self.local_context():
                self._draw(self.BORDER)
                self.set_line_width(0.5)
                self.line(dash_x, y + 6, dash_x + 6, y + 6)
            self.set_x(dash_x + 9)

        # Title — uppercase, bold
        self._color(self.CHARCOAL)
        self.set_font("Montserrat", "B", 13)
        self.set_y(y + 1)
        if num_str:
            self.set_x(self.l_margin + 30)
        self.cell(0, 12, title.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_y(border_y + 4)

    # ── Body Text ─────────────────────────────────────────

    def render_body(self, txt):
        if self._check_page_limit():
            return
        self._color(self.GRAY)
        self.set_font("Poppins", "", 9.5)
        self.multi_cell(0, 5.5, txt)
        self.ln(3)

    # ── Heading ───────────────────────────────────────────

    def render_heading(self, txt):
        if self._check_page_limit():
            return
        self.ln(5)
        self.set_font("Montserrat", "B", 10.5)
        self._color(self.CHARCOAL)
        self.cell(0, 7, txt.upper(), new_x="LMARGIN", new_y="NEXT")
        # Blue underline
        with self.local_context():
            self._draw(self.BLUE)
            self.set_line_width(0.8)
            self.line(self.l_margin, self.get_y(), self.l_margin + 20, self.get_y())
        self.ln(3)

    # ── Bullets ───────────────────────────────────────────

    def render_bullet(self, txt, indent=10):
        if self._check_page_limit():
            return
        x = self.l_margin + indent
        y = self.get_y()

        # Blue square bullet
        self._sharp_rect(x, y + 1.5, 2.5, 2.5, self.BLUE)

        self.set_x(x + 6)
        self._color(self.GRAY)
        self.set_font("Poppins", "", 9.5)
        self.multi_cell(self.epw - indent - 6, 5.5, txt)
        self.ln(0.5)

    def render_bullets(self, items, indent=10):
        for item in items:
            self.render_bullet(item, indent)

    # ── Code Block ────────────────────────────────────────

    def render_code_block(self, code):
        if self._check_page_limit():
            return
        code_lines = code.strip().split("\n")
        x = self.l_margin
        w = self.epw
        text_w = w - 16
        line_h = 5

        self.set_font("RobotoMono", "", 8.5)
        total_lines = 0
        for line in code_lines:
            if not line.strip():
                total_lines += 1
            else:
                line_w = self.get_string_width(line)
                total_lines += max(1, int(line_w / text_w) + (1 if line_w % text_w else 0))
        block_h = total_lines * line_h + 8

        self._ensure_space(block_h + 4)
        self.ln(1)
        y = self.get_y()

        # Shadow + dark rect
        self._bordered_card(x, y, w, block_h, fill=self.CODE_BG, border_w=1, shadow_offset=2)

        # Blue left accent bar
        self._sharp_rect(x, y, 3, block_h, self.BLUE)

        # Code text
        self.set_font("RobotoMono", "", 8.5)
        self._color(self.CODE_TEXT)
        self.set_xy(x + 10, y + 4)
        for line in code_lines:
            self.set_x(x + 10)
            if not line.strip():
                self.ln(line_h)
            else:
                self.multi_cell(text_w, line_h, line)

        self.set_y(y + block_h + 6)

    # ── Tip Box ───────────────────────────────────────────

    def render_tip_box(self, title, txt):
        if self._check_page_limit():
            return
        self.set_font("Poppins", "", 9)
        lines = max(len(txt) / 70, 1) + 1
        box_h = max(lines * 5.5 + 18, 22)
        self._ensure_space(box_h + 10)
        self.ln(4)
        x = self.l_margin
        y = self.get_y()
        w = self.epw

        # Amber-tinted background card
        self._bordered_card(x, y, w, box_h, fill=self.AMBER_BG, border_w=1, shadow_offset=2)

        # Amber left accent bar
        self._sharp_rect(x, y, 4, box_h, self.AMBER)

        # Badge label
        badge_x = x + 10
        badge_y = y + 5
        badge_w = self.get_string_width(title.upper()) + 8
        self.set_font("Montserrat", "B", 7)
        self._sharp_rect(badge_x, badge_y, badge_w, 5.5, self.AMBER)
        self._color(self.WHITE)
        self.set_xy(badge_x + 4, badge_y + 0.5)
        self.cell(badge_w - 8, 4.5, self._clean(title).upper())

        # Body text
        self.set_xy(x + 10, badge_y + 9)
        self._color(self.CHARCOAL)
        self.set_font("Poppins", "", 9)
        self.multi_cell(w - 20, 5, txt)
        self.set_y(y + box_h + 8)

    # ── Table ─────────────────────────────────────────────

    def render_table(self, headers, rows):
        if self._check_page_limit():
            return
        row_h = 7
        header_h = 9
        table_h = header_h + len(rows) * row_h + 4
        self._ensure_space(table_h)
        self.ln(2)
        n_cols = len(headers)
        col_w = self.epw / n_cols
        x_start = self.l_margin
        y_start = self.get_y()

        # Table border
        self._sharp_rect(x_start, y_start, self.epw, table_h, self.WHITE, self.BORDER, 1)

        # Header row — blue bg
        self._sharp_rect(x_start, y_start, self.epw, header_h, self.CHARCOAL)
        self._color(self.WHITE)
        self.set_font("Montserrat", "B", 8)
        self.set_xy(x_start, y_start)
        for h in headers:
            self.cell(col_w, header_h, f"  {h.upper()}", new_x="RIGHT", new_y="TOP")
        self.set_y(y_start + header_h)

        # Data rows with striping
        for i, row in enumerate(rows):
            bg = self.LIGHT_BG if i % 2 == 0 else self.WHITE
            self._bg(bg)
            self._color(self.CHARCOAL)
            self.set_font("Poppins", "", 8.5)
            for val in row:
                self.cell(col_w, row_h, f"  {val}", fill=True, new_x="RIGHT", new_y="TOP")
            self.ln(row_h)
        self.ln(2)

    # ── Checklist ─────────────────────────────────────────

    def render_checklist(self, items):
        if self._check_page_limit():
            return
        for item in items:
            x = self.l_margin + 8
            y = self.get_y()

            # Checkbox with blue border
            with self.local_context():
                self._draw(self.BLUE)
                self.set_line_width(0.8)
                self.rect(x, y + 0.5, 4, 4, style="D")

            self.set_x(x + 7)
            self._color(self.CHARCOAL)
            self.set_font("Poppins", "", 9.5)
            self.multi_cell(0, 5.5, item)
            self.ln(0.5)

    # ── Numbered Steps ────────────────────────────────────

    def render_numbered_steps(self, steps):
        if self._check_page_limit():
            return
        for i, step in enumerate(steps, 1):
            self._ensure_space(20)
            self.ln(1)
            x = self.l_margin
            y = self.get_y()

            # Square with number (blue bg)
            sq_size = 9
            self._sharp_rect(x + 2, y, sq_size, sq_size, self.BLUE)
            self.set_font("Montserrat", "B", 8)
            self._color(self.WHITE)
            num_str = str(i).zfill(2)
            nw = self.get_string_width(num_str)
            self.set_xy(x + 2 + (sq_size - nw) / 2, y + 1.5)
            self.cell(nw, 6, num_str, align="C")

            # Connecting line to next step
            if i < len(steps):
                with self.local_context():
                    self._draw(self.BORDER)
                    self.set_line_width(1)
                    line_x = x + 2 + sq_size / 2
                    self.line(line_x, y + sq_size + 1, line_x, y + sq_size + 6)

            # Step title
            text_x = x + sq_size + 8
            self.set_xy(text_x, y)
            self._color(self.CHARCOAL)
            self.set_font("Montserrat", "B", 10)
            self.cell(0, 6, step["title"].upper(), new_x="LMARGIN", new_y="NEXT")

            # Step description
            self.set_x(text_x)
            self._color(self.GRAY)
            self.set_font("Poppins", "", 9)
            self.multi_cell(self.epw - (text_x - self.l_margin), 5, step["description"])
            self.ln(4)

    # ── Two Column ────────────────────────────────────────

    def render_two_column(self, items):
        if self._check_page_limit():
            return
        col_w = self.epw / 2
        for i in range(0, len(items), 2):
            left = items[i]
            right = items[i + 1] if i + 1 < len(items) else None
            self.set_font("RobotoMono", "", 8.5)
            self._color(self.BLUE)
            self.set_x(self.l_margin + 5)
            self.cell(col_w - 5, 5.5, left[0].upper(), new_x="RIGHT", new_y="TOP")
            if right:
                self.cell(col_w - 5, 5.5, right[0].upper(), new_x="LMARGIN", new_y="NEXT")
            else:
                self.ln(5.5)
            self.set_font("Poppins", "", 8)
            self._color(self.GRAY)
            self.set_x(self.l_margin + 5)
            self.cell(col_w - 5, 4.5, left[1], new_x="RIGHT", new_y="TOP")
            if right:
                self.cell(col_w - 5, 4.5, right[1], new_x="LMARGIN", new_y="NEXT")
            else:
                self.ln(4.5)
            self.ln(1)

    # ── Callout Box ───────────────────────────────────────

    def render_callout_box(self, title, items):
        if self._check_page_limit():
            return
        box_h = len(items) * 6.5 + 20
        self._ensure_space(box_h + 6)
        self.ln(2)
        x = self.l_margin
        y = self.get_y()
        w = self.epw

        # Bordered card
        self._bordered_card(x, y, w, box_h, fill=self.WHITE, border_w=1, shadow_offset=2)

        # Blue top bar
        self._sharp_rect(x, y, w, 3, self.BLUE)

        # Title
        self.set_xy(x + 10, y + 7)
        self._color(self.CHARCOAL)
        self.set_font("Montserrat", "B", 10)
        self.cell(0, 6, self._clean(title).upper(), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

        # Items
        self.set_font("Poppins", "", 9)
        self._color(self.GRAY)
        for item in items:
            self.set_x(x + 10)
            self.cell(0, 5.5, item, new_x="LMARGIN", new_y="NEXT")

        self.set_y(y + box_h + 6)

    # ── Resources ─────────────────────────────────────────

    def render_resources(self, items):
        if self._check_page_limit():
            return
        box_h = len(items) * 7 + 22
        self._ensure_space(box_h + 6)
        self.ln(2)
        x = self.l_margin
        y = self.get_y()
        w = self.epw

        # Bordered card
        self._bordered_card(x, y, w, box_h, fill=self.LIGHT_BG, border_w=1, shadow_offset=2)

        # Charcoal top bar
        self._sharp_rect(x, y, w, 3, self.CHARCOAL)

        # Title
        self.set_xy(x + 10, y + 7)
        self._color(self.CHARCOAL)
        self.set_font("Montserrat", "B", 10)
        self.cell(0, 6, "RESOURCES & LINKS", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

        # Items with blue bullets
        for r in items:
            self.set_x(x + 10)
            bx = self.get_x()
            by = self.get_y() + 1
            self._sharp_rect(bx, by, 2.5, 2.5, self.BLUE)
            self.set_x(bx + 6)
            self._color(self.CHARCOAL)
            self.set_font("Poppins", "", 9)
            self.cell(0, 6, r, new_x="LMARGIN", new_y="NEXT")

        self.set_y(y + box_h + 6)

    # ── main render dispatch ──────────────────────────────

    @classmethod
    def _clean_section(cls, section):
        cleaned = {}
        for k, v in section.items():
            if k in ("code",):
                cleaned[k] = v
            elif isinstance(v, str):
                cleaned[k] = cls._clean(v)
            elif isinstance(v, list):
                cleaned[k] = [
                    cls._clean(i) if isinstance(i, str)
                    else {sk: cls._clean(sv) if isinstance(sv, str) else sv for sk, sv in i.items()} if isinstance(i, dict)
                    else [cls._clean(c) if isinstance(c, str) else c for c in i] if isinstance(i, list)
                    else i
                    for i in v
                ]
            else:
                cleaned[k] = v
        return cleaned

    def render_section(self, section):
        section = self._clean_section(section)
        t = section["type"]
        if t == "section_title":
            self.render_section_title(section["number"], section["title"])
        elif t == "body":
            self.render_body(section["text"])
        elif t == "heading":
            self.render_heading(section["text"])
        elif t == "bullet":
            self.render_bullet(section["text"])
        elif t == "bullets":
            self.render_bullets(section["items"])
        elif t == "code_block":
            self.render_code_block(section["code"])
        elif t == "code":
            self.render_code_block(section.get("code", section.get("text", "")))
        elif t == "tip_box":
            self.render_tip_box(section["title"], section["text"])
        elif t == "table":
            self.render_table(section["headers"], section["rows"])
        elif t == "checklist":
            self.render_checklist(section["items"])
        elif t == "numbered_steps":
            self.render_numbered_steps(section["steps"])
        elif t == "two_column":
            self.render_two_column(section["items"])
        elif t == "callout_box":
            self.render_callout_box(section["title"], section["items"])
        elif t == "resources":
            self.render_resources(section["items"])
        elif t == "page_break":
            if not self._check_page_limit():
                self.add_page()
        else:
            print(f"WARNING: Unknown section type '{t}', skipping.", file=sys.stderr)

    def render_content(self, content: dict):
        if content.get("footer_text"):
            self._footer_text = content["footer_text"]

        self.render_cover(
            content["title"],
            content.get("subtitle"),
            content.get("subtitle_bullets"),
        )

        for section in content.get("sections", []):
            if self._check_page_limit():
                break
            self.render_section(section)


def main():
    parser = argparse.ArgumentParser(description="Generate a professional PDF from JSON content.")
    parser.add_argument("--content-file", required=True, help="Path to JSON content file")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()

    content_path = Path(args.content_file)
    if not content_path.exists():
        print(f"ERROR: Content file not found: {content_path}", file=sys.stderr)
        sys.exit(1)

    with open(content_path) as f:
        content = json.load(f)

    pdf = ProfessionalDoc()
    pdf.render_content(content)

    if pdf.pages_count > MAX_PAGES:
        print(f"WARNING: PDF has {pdf.pages_count} pages, max is {MAX_PAGES}.", file=sys.stderr)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    print(f"PDF saved to: {output_path}")
    print(f"Pages: {pdf.pages_count}")


if __name__ == "__main__":
    main()
