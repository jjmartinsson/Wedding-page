#!/usr/bin/env python3
"""Generate a Swedish wedding invitation PDF for Joel & Madeleine."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import os

# Colors matching the website
BLUSH = HexColor('#d4899a')
BLUSH_LIGHT = HexColor('#fbeef0')
BLUSH_MID = HexColor('#f5cdd2')
SAGE = HexColor('#8ab58a')
SAGE_DARK = HexColor('#5a845a')
SAGE_LIGHT = HexColor('#eef6ee')
DARK_BROWN = HexColor('#3a2a2a')
OFF_WHITE = HexColor('#fdf8f5')
ROSE_DARK = HexColor('#b86878')

W, H = A4  # 595.28 x 841.89 points

def draw_border(c, x, y, w, h, color, thickness=1.5):
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.rect(x, y, w, h, stroke=1, fill=0)

def draw_thin_line(c, x1, y1, x2, y2, color, thickness=0.5):
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.line(x1, y1, x2, y2)

def draw_ornament_line(c, cx, y, width, color):
    """Draw a decorative line with diamond center."""
    half = width / 2
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(cx - half, y, cx - 0.4*cm, y)
    c.line(cx + 0.4*cm, y, cx + half, y)
    # Diamond
    c.setFillColor(color)
    path = c.beginPath()
    path.moveTo(cx, y + 3)
    path.lineTo(cx + 4, y)
    path.lineTo(cx, y - 3)
    path.lineTo(cx - 4, y)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

def create_invitation():
    output_path = '/home/user/Wedding-page/invitation_MadeleineJoel2026.pdf'
    c = canvas.Canvas(output_path, pagesize=A4)

    # ── Background ──────────────────────────────────────────────────────
    c.setFillColor(OFF_WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Soft blush gradient strip at top
    c.setFillColor(BLUSH_LIGHT)
    c.rect(0, H - 3.5*cm, W, 3.5*cm, fill=1, stroke=0)

    # Soft sage strip at bottom
    c.setFillColor(SAGE_LIGHT)
    c.rect(0, 0, W, 3*cm, fill=1, stroke=0)

    # Outer border (double)
    margin = 1.0*cm
    draw_border(c, margin, margin, W - 2*margin, H - 2*margin, BLUSH, 2)
    draw_border(c, margin + 0.25*cm, margin + 0.25*cm,
                W - 2*(margin + 0.25*cm), H - 2*(margin + 0.25*cm), SAGE, 0.8)

    cx = W / 2  # center x

    # ── Top decorative header ────────────────────────────────────────────
    top_y = H - 2.2*cm
    draw_ornament_line(c, cx, top_y, 10*cm, BLUSH)

    # ── Title: "Vi gifter oss" ───────────────────────────────────────────
    c.setFont("Times-BoldItalic", 32)
    c.setFillColor(ROSE_DARK)
    title = "Vi gifter oss"
    c.drawCentredString(cx, H - 4.2*cm, title)

    draw_ornament_line(c, cx, H - 4.8*cm, 8*cm, SAGE)

    # ── Names ────────────────────────────────────────────────────────────
    c.setFont("Times-BoldItalic", 48)
    c.setFillColor(DARK_BROWN)
    c.drawCentredString(cx, H - 6.5*cm, "Madeleine & Joel")

    # Small flourish under names
    draw_ornament_line(c, cx, H - 7.0*cm, 12*cm, BLUSH)

    # ── Castle image ─────────────────────────────────────────────────────
    castle_path = '/home/user/Wedding-page/slottet.jpg'
    img_w = 14*cm
    img_h = 7.5*cm
    img_x = (W - img_w) / 2
    img_y = H - 15.5*cm

    # Decorative frame behind image
    frame_pad = 0.2*cm
    c.setFillColor(BLUSH_MID)
    c.rect(img_x - frame_pad, img_y - frame_pad,
           img_w + 2*frame_pad, img_h + 2*frame_pad, fill=1, stroke=0)

    c.drawImage(castle_path, img_x, img_y, width=img_w, height=img_h,
                preserveAspectRatio=True, mask='auto')

    # Caption under castle image
    c.setFont("Times-Italic", 9)
    c.setFillColor(SAGE_DARK)
    c.drawCentredString(cx, img_y - 0.5*cm, "Kalmar Slott")

    draw_ornament_line(c, cx, img_y - 1.1*cm, 10*cm, SAGE)

    # ── Main invitation text ─────────────────────────────────────────────
    text_y = img_y - 2.0*cm

    c.setFont("Times-Roman", 13)
    c.setFillColor(DARK_BROWN)
    c.drawCentredString(cx, text_y, "Med glädje och kärlek inbjuder vi er att fira")

    text_y -= 0.65*cm
    c.drawCentredString(cx, text_y, "vårt bröllop tillsammans med oss.")

    # Date block
    text_y -= 1.4*cm
    c.setFont("Times-Bold", 16)
    c.setFillColor(ROSE_DARK)
    c.drawCentredString(cx, text_y, "Lördagen den 22 augusti 2026")

    text_y -= 0.75*cm
    c.setFont("Times-Roman", 13)
    c.setFillColor(DARK_BROWN)
    c.drawCentredString(cx, text_y, "Vigsel kl. 16:00")

    text_y -= 0.65*cm
    c.drawCentredString(cx, text_y, "Kalmar Slottskyrka, Kalmar")

    draw_ornament_line(c, cx, text_y - 0.6*cm, 9*cm, BLUSH)

    # Programme summary
    text_y -= 1.5*cm
    c.setFont("Times-BoldItalic", 12)
    c.setFillColor(SAGE_DARK)
    c.drawCentredString(cx, text_y, "Program")

    programme = [
        ("15:30", "Gästerna anländer till Kalmar Slott"),
        ("16:00", "Vigselceremoni i Slottskyrkan"),
        ("Efter vigseln", "Skålande i Örträdgården"),
        ("Kväll", "Middag i Slottsrestaurangen"),
        ("Natt", "Dans i Amiralitetskällaren"),
    ]

    text_y -= 0.5*cm
    for time_str, desc in programme:
        text_y -= 0.55*cm
        c.setFont("Times-Bold", 10)
        c.setFillColor(ROSE_DARK)
        c.drawRightString(cx - 0.3*cm, text_y, time_str)
        c.setFont("Times-Roman", 10)
        c.setFillColor(DARK_BROWN)
        c.drawString(cx + 0.3*cm, text_y, desc)
        # small dot separator
        c.setFillColor(BLUSH)
        c.circle(cx, text_y + 3, 2, fill=1, stroke=0)

    draw_ornament_line(c, cx, text_y - 0.6*cm, 10*cm, SAGE)

    # Dress code & practical
    text_y -= 1.4*cm
    c.setFont("Times-BoldItalic", 11)
    c.setFillColor(SAGE_DARK)
    c.drawCentredString(cx, text_y, "Klädsel: Mörk kostym")

    text_y -= 0.65*cm
    c.setFont("Times-Roman", 10)
    c.setFillColor(DARK_BROWN)
    c.drawCentredString(cx, text_y,
        "Boende: Slottshotellet, Slottsvägen 7, Kalmar  ·  10% rabatt med kod Joel&Madeleine2025")

    draw_ornament_line(c, cx, text_y - 0.55*cm, 12*cm, BLUSH)

    # ── Website & password box ───────────────────────────────────────────
    box_y = 2.5*cm
    box_h = 2.8*cm
    box_x = 3.5*cm
    box_w = W - 7*cm

    c.setFillColor(BLUSH_MID)
    c.roundRect(box_x, box_y, box_w, box_h, radius=0.3*cm, fill=1, stroke=0)
    c.setStrokeColor(ROSE_DARK)
    c.setLineWidth(1)
    c.roundRect(box_x, box_y, box_w, box_h, radius=0.3*cm, fill=0, stroke=1)

    c.setFont("Times-BoldItalic", 12)
    c.setFillColor(ROSE_DARK)
    c.drawCentredString(cx, box_y + box_h - 0.75*cm, "Vår bröllopssida")

    c.setFont("Times-Roman", 10)
    c.setFillColor(DARK_BROWN)
    c.drawCentredString(cx, box_y + box_h - 1.45*cm,
        "Webbplats:  MadeleineJoel2026.netlify.app")
    c.drawCentredString(cx, box_y + box_h - 2.0*cm,
        "Lösenord:  MadeleineJoel2026")

    # ── Bottom footer ─────────────────────────────────────────────────────
    c.setFont("Times-Italic", 9)
    c.setFillColor(SAGE_DARK)
    c.drawCentredString(cx, 1.5*cm,
        "Vi ser fram emot att fira denna dag med er  ♡")

    draw_ornament_line(c, cx, 1.1*cm, 8*cm, BLUSH)

    c.save()
    print(f"PDF saved to: {output_path}")
    return output_path

if __name__ == '__main__':
    create_invitation()
