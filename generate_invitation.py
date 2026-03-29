#!/usr/bin/env python3
"""Generate a Swedish wedding invitation PDF for Joel & Madeleine."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# Colors matching the website
BLUSH       = HexColor('#d4899a')
BLUSH_LIGHT = HexColor('#fbeef0')
BLUSH_MID   = HexColor('#f5cdd2')
SAGE        = HexColor('#8ab58a')
SAGE_DARK   = HexColor('#5a845a')
SAGE_LIGHT  = HexColor('#eef6ee')
DARK_BROWN  = HexColor('#3a2a2a')
OFF_WHITE   = HexColor('#fdf8f5')
ROSE_DARK   = HexColor('#b86878')

W, H = A4   # 595.28 x 841.89 pt  ≈  21 x 29.7 cm
cx = W / 2


def y(cm_from_top):
    """Convert cm-from-top to reportlab y (bottom-origin)."""
    return H - cm_from_top * cm


def ornament(c, cy_from_top, width_cm, color):
    """Decorative rule with a diamond centre."""
    yp = y(cy_from_top)
    half = width_cm * cm / 2
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(cx - half, yp, cx - 0.35*cm, yp)
    c.line(cx + 0.35*cm, yp, cx + half, yp)
    c.setFillColor(color)
    path = c.beginPath()
    path.moveTo(cx,        yp + 3)
    path.lineTo(cx + 4,    yp)
    path.lineTo(cx,        yp - 3)
    path.lineTo(cx - 4,    yp)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def text(c, cm_from_top, string, font, size, color, align='centre'):
    c.setFont(font, size)
    c.setFillColor(color)
    yp = y(cm_from_top)
    if align == 'centre':
        c.drawCentredString(cx, yp, string)
    elif align == 'right':
        c.drawRightString(cx - 0.25*cm, yp, string)
    elif align == 'left':
        c.drawString(cx + 0.25*cm, yp, string)


def create_invitation():
    out = '/home/user/Wedding-page/invitation_MadeleineJoel2026.pdf'
    c = canvas.Canvas(out, pagesize=A4)

    # ── Background ────────────────────────────────────────────────────────
    c.setFillColor(OFF_WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Blush top strip
    c.setFillColor(BLUSH_LIGHT)
    c.rect(0, y(3.2), W, 3.2*cm, fill=1, stroke=0)

    # Sage bottom strip
    c.setFillColor(SAGE_LIGHT)
    c.rect(0, 0, W, 3.0*cm, fill=1, stroke=0)

    # Outer double border
    m = 1.0*cm
    c.setStrokeColor(BLUSH);  c.setLineWidth(2.0)
    c.rect(m, m, W - 2*m, H - 2*m, stroke=1, fill=0)
    c.setStrokeColor(SAGE);   c.setLineWidth(0.8)
    c.rect(m + 0.22*cm, m + 0.22*cm,
           W - 2*(m + 0.22*cm), H - 2*(m + 0.22*cm), stroke=1, fill=0)

    # ── Header ────────────────────────────────────────────────────────────
    ornament(c, 2.1, 10, BLUSH)
    text(c, 3.6, "Vi gifter oss", "Times-BoldItalic", 30, ROSE_DARK)
    ornament(c, 4.2, 8, SAGE)
    text(c, 5.8, "Madeleine & Joel", "Times-BoldItalic", 46, DARK_BROWN)
    ornament(c, 6.4, 12, BLUSH)

    # ── Castle image ──────────────────────────────────────────────────────
    iw, ih = 13.5*cm, 6.5*cm
    ix = (W - iw) / 2
    iy = y(13.5)                     # bottom of image = 13.5 cm from top
    pad = 0.18*cm
    c.setFillColor(BLUSH_MID)
    c.rect(ix - pad, iy - pad, iw + 2*pad, ih + 2*pad, fill=1, stroke=0)
    c.drawImage('/home/user/Wedding-page/slottet.jpg',
                ix, iy, width=iw, height=ih,
                preserveAspectRatio=True, mask='auto')

    text(c, 14.1, "Kalmar Slott", "Times-Italic", 9, SAGE_DARK)
    ornament(c, 14.7, 10, SAGE)

    # ── Invitation body ───────────────────────────────────────────────────
    text(c, 15.7, "Med glädje och kärlek inbjuder vi er att fira",
         "Times-Roman", 12, DARK_BROWN)
    text(c, 16.3, "vårt bröllop tillsammans med oss.",
         "Times-Roman", 12, DARK_BROWN)

    text(c, 17.4, "Lördagen den 22 augusti 2026",
         "Times-Bold", 15, ROSE_DARK)
    text(c, 18.1, "Vigsel kl. 16:00",   "Times-Roman", 12, DARK_BROWN)
    text(c, 18.7, "Kalmar Slottskyrka, Kalmar", "Times-Roman", 12, DARK_BROWN)

    ornament(c, 19.35, 9, BLUSH)

    # ── Programme ────────────────────────────────────────────────────────
    text(c, 20.2, "Program", "Times-BoldItalic", 12, SAGE_DARK)

    rows = [
        ("15:30",         "Gasternas ankomst till Kalmar Slott"),
        ("16:00",         "Vigselceremoni i Slottskyrkan"),
        ("Efter vigseln", "Skalande i Ortradgarden"),
        ("Kvall",         "Middag i Slottsrestaurangen"),
        ("Natt",          "Dans i Amiralitetskallaren"),
    ]
    # Swedish text with proper chars
    rows_sw = [
        ("15:30",           "G\u00e4sternas ankomst till Kalmar Slott"),
        ("16:00",           "Vigselceremoni i Slottskyrkan"),
        ("Efter vigseln",   "Sk\u00e5lande i \u00d6rttr\u00e4dg\u00e5rden"),
        ("Kv\u00e4ll",      "Middag i Slottsrestaurangen"),
        ("Natt",            "Dans i Amiralitetsk\u00e4llaren"),
    ]

    row_y = 20.85
    for time_s, desc_s in rows_sw:
        text(c, row_y, time_s,  "Times-Bold",   10, ROSE_DARK, 'right')
        text(c, row_y, desc_s,  "Times-Roman",  10, DARK_BROWN, 'left')
        # dot
        c.setFillColor(BLUSH)
        c.circle(cx, y(row_y) + 3, 2, fill=1, stroke=0)
        row_y += 0.55

    ornament(c, row_y + 0.3, 10, SAGE)

    # ── Dress code & accommodation ────────────────────────────────────────
    text(c, row_y + 1.1, "Kl\u00e4dsel: M\u00f6rk kostym",
         "Times-BoldItalic", 11, SAGE_DARK)
    text(c, row_y + 1.75,
         "Boende: Slottshotellet, Slottsv\u00e4gen 7, Kalmar  \u00b7  "
         "10% rabatt med kod Joel&Madeleine2025",
         "Times-Roman", 9, DARK_BROWN)

    ornament(c, row_y + 2.35, 12, BLUSH)

    # ── Website / password box ────────────────────────────────────────────
    bx, bw, bh = 3.8*cm, W - 7.6*cm, 2.5*cm
    by = 1.7*cm                     # bottom edge, from page bottom
    c.setFillColor(BLUSH_MID)
    c.roundRect(bx, by, bw, bh, radius=0.28*cm, fill=1, stroke=0)
    c.setStrokeColor(ROSE_DARK);  c.setLineWidth(1)
    c.roundRect(bx, by, bw, bh, radius=0.28*cm, fill=0, stroke=1)

    # text inside box (in bottom-origin coords)
    c.setFont("Times-BoldItalic", 12)
    c.setFillColor(ROSE_DARK)
    c.drawCentredString(cx, by + bh - 0.72*cm, "V\u00e5r br\u00f6llopsida")

    c.setFont("Times-Roman", 10)
    c.setFillColor(DARK_BROWN)
    c.drawCentredString(cx, by + bh - 1.4*cm,
                        "Webbplats:  MadeleineJoel2026.netlify.app")
    c.drawCentredString(cx, by + bh - 1.95*cm,
                        "L\u00f6senord:  MadeleineJoel2026")

    # ── Footer ────────────────────────────────────────────────────────────
    c.setFont("Times-Italic", 9)
    c.setFillColor(SAGE_DARK)
    c.drawCentredString(cx, 0.9*cm,
                        "Vi ser fram emot att fira denna dag med er  \u2665")
    ornament(c, 29.0, 8, BLUSH)

    c.save()
    print(f"Saved: {out}")
    return out


if __name__ == '__main__':
    create_invitation()
