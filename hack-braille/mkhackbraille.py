#!/usr/bin/env python3
# Copyright (c) 2026 Peter Marquardt <wwwutz@users.noreply.github.com>
# SPDX-License-Identifier: MIT
"""Make "Hack Braille" from Hack 3.003: add the Braille Patterns block.

Usage: mkhackbraille.py Hack-Style.ttf HackBraille-Style.ttf

Hack has no glyphs for U+2800..U+28FF, which many TUIs use for graphs and
spinners.  This draws them as 8 square dots on a 2x4 grid spanning the full
character cell (advance width x hhea ascent..descent), the same geometry as
the Nerd Fonts patcher's "rectangle" braille: dot centers at 1/4 and 3/4 of
the width, 1/8, 3/8, 5/8 and 7/8 of the height, each dot 60% of its grid
cell.  Nothing else in the font changes, except that it is renamed, as the
Bitstream Vera license asks of modified fonts (see LICENSE.md).
"""

import sys

from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

FAMILY = "Hack Braille"
PS_FAMILY = "HackBraille"
RATIO = 0.6

# Unicode dot numbers 1-8 map to bits 0-7; (column, row) of each dot
DOTS = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (0, 3), (1, 3)]


def braille_glyph(pattern, width, ymax, ymin):
    height = ymax - ymin
    half_x = round(width / 4 * RATIO)
    half_y = round(height / 8 * RATIO)
    pen = TTGlyphPen(None)
    for bit, (col, row) in enumerate(DOTS):
        if pattern & (1 << bit):
            cx = round(width / 4 + col * width / 2)
            cy = round(ymax - height / 8 - row * height / 4)
            # clockwise, as TrueType outlines are
            pen.moveTo((cx - half_x, cy + half_y))
            pen.lineTo((cx + half_x, cy + half_y))
            pen.lineTo((cx + half_x, cy - half_y))
            pen.lineTo((cx - half_x, cy - half_y))
            pen.closePath()
    return pen.glyph()


def main(src, dst):
    font = TTFont(src)
    cmap = font.getBestCmap()
    if any(code in cmap for code in range(0x2800, 0x2900)):
        sys.exit(f"{src} already has braille glyphs")

    width = font["hmtx"][cmap[ord("0")]][0]
    ymax, ymin = font["hhea"].ascent, font["hhea"].descent

    order = list(font.getGlyphOrder())
    for code in range(0x2800, 0x2900):
        name = f"uni{code:04X}"
        glyph = braille_glyph(code - 0x2800, width, ymax, ymin)
        glyph.recalcBounds(font["glyf"])
        font["glyf"][name] = glyph
        font["hmtx"][name] = (width, getattr(glyph, "xMin", 0))
        order.append(name)
        for table in font["cmap"].tables:
            if table.isUnicode():
                table.cmap[code] = name
    font.setGlyphOrder(order)
    font["glyf"].setGlyphOrder(order)

    # these hold per-glyph data that would no longer match
    for tag in ("hdmx", "LTSH", "VDMX"):
        if tag in font:
            del font[tag]

    os2 = font["OS/2"]
    os2.ulUnicodeRange3 |= 1 << (82 - 64)  # Braille Patterns

    for rec in font["name"].names:
        if rec.nameID in (1, 4, 16):
            rec.string = rec.toUnicode().replace("Hack", FAMILY, 1)
        elif rec.nameID == 6:
            rec.string = rec.toUnicode().replace("Hack", PS_FAMILY, 1)
        elif rec.nameID == 3:
            rec.string = rec.toUnicode() + "; Braille"
        elif rec.nameID == 5:
            rec.string = rec.toUnicode() + "; Braille added"

    font.save(dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
