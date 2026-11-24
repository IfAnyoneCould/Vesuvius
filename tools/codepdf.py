# NOTE this file was written by an AI (Claude), not me. it's just a helper for turning the
# code into a pdf for the class and is not part of the game or the code submission
# usage: uv run --with reportlab --with pygments python tools/codepdf.py code.pdf --project --configs --size 8 --color --flow --gutter-rule

import argparse
import fnmatch
import os
import subprocess

from pygments import lex
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.styles import get_style_by_name
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("mono", "C:/Windows/Fonts/consola.ttf"))
pdfmetrics.registerFont(TTFont("mono-b", "C:/Windows/Fonts/consolab.ttf"))
pdfmetrics.registerFont(TTFont("mono-i", "C:/Windows/Fonts/consolai.ttf"))

W, H = letter
MARGIN = 0.6 * 72
HEADER_H = 28
FOOTER_H = 22
GRAY = (0.45, 0.45, 0.45)
RULE = (0.8, 0.8, 0.8)

# used with --project
INCLUDE = ["*.py", "configs/*.json"]
EXCLUDE = [
    "drivers/*",
    "fonts/*",
    "typings/*",
    "tools/deploy.py",
    "tools/codepdf.py",
]


def project_files(root, configs):
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root, capture_output=True, text=True, check=True,
    ).stdout
    files = []
    for f in sorted(set(out.splitlines())):
        inc = INCLUDE if configs else INCLUDE[:1]
        if not any(fnmatch.fnmatch(f, i) for i in inc):
            continue
        if any(fnmatch.fnmatch(f, e) for e in EXCLUDE):
            continue
        with open(os.path.join(root, f), encoding="utf-8") as fh:
            if not fh.read().strip():
                continue  # empty __init__.py etc
        files.append(f)
    return files


def hex_rgb(h):
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))


def token_lines(path, text, color, style):
    # list of lines, each a list of (text, rgb, font)
    plain = [[(l, (0, 0, 0), "mono")] for l in text.split("\n")]
    if not color:
        return plain
    try:
        lexer = get_lexer_for_filename(path, stripnl=False, ensurenl=False)
    except Exception:
        lexer = TextLexer()
    sty = get_style_by_name(style)
    lines = [[]]
    for ttype, val in lex(text, lexer):
        s = sty.style_for_token(ttype)
        rgb = hex_rgb(s["color"]) if s["color"] else (0, 0, 0)
        font = "mono-b" if s["bold"] else "mono-i" if s["italic"] else "mono"
        parts = val.split("\n")
        for i, p in enumerate(parts):
            if i:
                lines.append([])
            if p:
                lines[-1].append((p, rgb, font))
    return lines


def wrap(segs, width):
    # split one source line into rows of at most width chars, breaking at spaces
    chars = [(ch, rgb, font) for t, rgb, font in segs for ch in t.replace("	", "    ")]
    if len(chars) <= width:
        return [segs]
    line = "".join(ch for ch, _, _ in chars)
    indent = min(len(line) - len(line.lstrip(" ")) + 4, width // 2)
    rows, pos, room = [], 0, width
    while pos < len(chars):
        cut = pos + room
        if cut < len(chars):
            sp = line.rfind(" ", pos + room // 2, cut)
            if sp != -1:
                cut = sp + 1
        rows.append(([(" " * indent, (0, 0, 0), "mono")] if rows else []) + [(ch, rgb, font) for ch, rgb, font in chars[pos:cut]])
        pos, room = cut, width - indent
    return rows


def layout(files, args, rows_per_page, chars):
    # pages: {"file": name, "cont": bool, "rows": [(kind, num, segs)]}
    pages = []

    def new_page(name, cont):
        pages.append({"file": name, "cont": cont, "rows": []})

    for path, name in files:
        with open(path, encoding="utf-8") as f:
            text = f.read().rstrip("\n")
        lines = token_lines(path, text, args.color, args.style)
        if args.flow and pages and len(pages[-1]["rows"]) + 4 < rows_per_page:
            if pages[-1]["rows"]:
                pages[-1]["rows"].append(("gap", None, None))
            pages[-1]["rows"].append(("title", None, name))
            pages[-1].setdefault("starts", []).append(name)
        else:
            new_page(name, False)
        for num, segs in enumerate(lines, 1):
            for i, row in enumerate(wrap(segs, chars)):
                if len(pages[-1]["rows"]) >= rows_per_page:
                    new_page(name, True)
                pages[-1]["rows"].append(("code", num if i == 0 else None, row))
    return pages


def render(pages, args, out):
    c = canvas.Canvas(out, pagesize=letter)
    c.setTitle(args.title)
    lh = args.size * 1.25
    gutter = pdfmetrics.stringWidth("0000", "mono", args.size) + 10
    total = len(pages)
    for pn, page in enumerate(pages, 1):
        top = H - MARGIN
        # header
        name = page["file"]
        c.setFont("mono-b", 11)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(MARGIN, top - 12, name)
        if page["cont"]:
            c.setFont("mono-i", 9)
            c.setFillColorRGB(*GRAY)
            c.drawString(MARGIN + pdfmetrics.stringWidth(name, "mono-b", 11) + 8, top - 12, "(continued)")
        c.setFont("mono", 9)
        c.setFillColorRGB(*GRAY)
        c.drawRightString(W - MARGIN, top - 12, args.title)
        c.setStrokeColorRGB(*RULE)
        c.setLineWidth(0.6)
        c.line(MARGIN, top - HEADER_H + 8, W - MARGIN, top - HEADER_H + 8)

        y = top - HEADER_H - lh + 4
        x_code = MARGIN + gutter
        for kind, num, segs in page["rows"]:
            if kind == "title":
                c.setFont("mono-b", args.size + 1)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(MARGIN, y, segs)
                c.line(MARGIN, y - 3, W - MARGIN, y - 3)
            elif kind == "code":
                if args.gutter_rule:
                    c.setStrokeColorRGB(*RULE)
                    c.line(x_code - 5, y - lh * 0.3, x_code - 5, y + lh * 0.7)
                c.setFont("mono", args.size)
                c.setFillColorRGB(*GRAY)
                c.drawRightString(x_code - 10, y, str(num) if num is not None else "+")
                x = x_code
                for t, rgb, font in segs:
                    c.setFont(font, args.size)
                    c.setFillColorRGB(*rgb)
                    c.drawString(x, y, t)
                    x += pdfmetrics.stringWidth(t, font, args.size)
            y -= lh

        # footer
        c.setFont("mono", 8)
        c.setFillColorRGB(*GRAY)
        c.drawCentredString(W / 2, MARGIN, f"page {pn} of {total}")
        c.showPage()
    c.save()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("out")
    p.add_argument("files", nargs="*")
    p.add_argument("--project", action="store_true", help="pick files from git using INCLUDE/EXCLUDE")
    p.add_argument("--configs", action="store_true", help="with --project, also include configs/*.json")
    p.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p.add_argument("--title", default="Vesuvius")
    p.add_argument("--size", type=float, default=9)
    p.add_argument("--color", action="store_true")
    p.add_argument("--style", default="default")
    p.add_argument("--flow", action="store_true")
    p.add_argument("--gutter-rule", action="store_true")
    args = p.parse_args()

    names = project_files(args.root, args.configs) if args.project else args.files
    files = [(os.path.join(args.root, f), f.replace("\\", "/")) for f in names]
    lh = args.size * 1.25
    usable_h = H - 2 * MARGIN - HEADER_H - FOOTER_H
    rows_per_page = int(usable_h // lh)
    gutter = pdfmetrics.stringWidth("0000", "mono", args.size) + 10
    chars = int((W - 2 * MARGIN - gutter) // pdfmetrics.stringWidth("m", "mono", args.size))
    pages = layout(files, args, rows_per_page, chars)
    render(pages, args, args.out)
    print(args.out, len(pages), "pages,", rows_per_page, "lines/page,", chars, "chars/line")


main()
