"""Build the GitHub Overview from PROFILE.md. Run with Python 3.10+, Pillow and
the Liberation Sans, Serif and Mono fonts installed (fc-match on PATH).
Use a repository checkout of Dishank25/Dishank25. The small SVGs are the
GitHub-native presentation; each linked panel has a complete text equivalent.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from html import escape
from pathlib import Path

from PIL import ImageFont
from profile_art import motif

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://dishank25.github.io/Dishank25/"
GITHUB = "https://github.com/Dishank25"
RAW = "https://raw.githubusercontent.com/Dishank25/Dishank25/main/"
LINKEDIN = "https://www.linkedin.com/in/dishankjain25/"
ASSETS = Path("assets/overview")
INK, LIGHT, BODY = "#0b1922", "#e7f5f3", "#c1d8d9"
MINT, LINE, MONO_COLOR = "#80ead2", "#29454c", "#a1cbbe"
SANS = "Arial,Helvetica,sans-serif"
SERIF = "Georgia,'Liberation Serif',serif"
MONO = "'Liberation Mono',Consolas,monospace"
HERO = """<a href="https://dishank25.github.io/Dishank25/"><picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/Dishank25/Dishank25/2a100f4d9834131c5c129b0d8cfeea1d2d21182d/assets/observatory-breathing-mobile.svg">
  <img align="top" src="assets/observatory-breathing.svg" width="1080" alt="Dishank Jain, AI engineer. An illustrated engineer watches a luminous manta through the window of a deep-sea observatory. Open the portfolio.">
</picture></a>"""

PROJECT_LABELS = {
    "pawsupport": "FAQ routing",
    "supportpilot": "Semantic retrieval",
    "veterinary-records": "Document extraction",
    "recommendations": "Recommender systems",
    "breed-identification": "Computer vision",
    "abyssal-portfolio": "Python / Django",
    "job-portal": "Flutter / Hiring",
    "job-discovery": "Flutter / Candidate search",
    "terminal-tic-tac-toe": "Python / Standard library",
}


@lru_cache()
def font(family, size, weight=400, italic=False):
    style = "Italic" if italic else ("Bold" if weight >= 600 else "Regular")
    name = {SANS: "Liberation Sans", SERIF: "Liberation Serif", MONO: "Liberation Mono"}[family]
    path = subprocess.check_output(["fc-match", f"{name}:style={style}", "-f", "%{file}"], text=True)
    return ImageFont.truetype(path, size)


def wrap(value, size, available, weight=400):
    measure = font(SANS, size, weight)
    lines = []
    for word in value.split():
        candidate = (lines[-1] + " " + word) if lines else word
        if lines and measure.getlength(candidate) <= available * .97:
            lines[-1] = candidate
        else:
            lines.append(word)
    return lines


@dataclass
class Panel:
    key: str
    kind: str
    title: str
    href: str
    label: str = ""
    paragraphs: tuple = ()
    rows: tuple = ()
    detail: str = ""

    def alt(self):
        parts = [self.label, self.title, *self.paragraphs, self.detail]
        parts.extend(". ".join(row) for row in self.rows)
        if self.kind == "project":
            parts.append("Open the case study.")
        return " ".join(p.rstrip(".") + "." for p in parts if p)


def get_panels():
    sections = re.split(r"^## (.+)$", (ROOT / "PROFILE.md").read_text(), flags=re.M)
    body = dict(zip(sections[1::2], sections[2::2]))
    about = tuple(body["About me"].strip().split("\n\n"))
    yield Panel("featured", "feature", "Abyssal Observatory", GITHUB + "/abyssal-portfolio",
                "Featured project", detail="Python / Django")
    yield Panel("about", "about", "About me", SITE + "#about", "Noida, India", about)
    groups = [("AI engineering projects", "Selected work", "AI engineering"),
              ("Web, mobile, and Python projects", "Web, mobile & Python", "Software projects")]
    for group, title, label in groups:
        key = "selected-work" if group.startswith("AI ") else "more-projects"
        yield Panel(key, "heading", title, SITE + "#work", label)
        for name, narrative, url in re.findall(r"^- \*\*(.+?)\.\*\* (.+?) \[[^\]]+\]\((https://dishank25.github.io/[^)]+)\)", body[group], re.M):
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            yield Panel(slug, "project", name, url, PROJECT_LABELS[slug], (narrative,))
    def table(name):
        return tuple(tuple(c.strip() for c in line.strip("|").split("|"))
                     for line in body[name].splitlines() if line.startswith("|"))[2:]
    yield Panel("skills", "skills", "Technical skills", SITE + "#skills", rows=table("Technical skills"))
    for key, title in (("experience", "Experience"), ("education", "Education")):
        narrative = body[title].strip().split(" [", 1)[0]
        action = "Explore work history" if key == "experience" else "View education"
        yield Panel(key, "reference", title, SITE + "#experience", paragraphs=(narrative,), detail=action)
    yield Panel("connect", "contact", "Connect on LinkedIn", LINKEDIN, "Contact")
    yield Panel("text", "text", "Read as text & browse source links", GITHUB + "/Dishank25/blob/main/PROFILE.md")


class Canvas:
    def __init__(self, width):
        self.width = width
        self.mobile = width == 360
        self.wide = width == 960
        self.rail = round(width * (18 / 420 if self.mobile else 32 / 960))
        self.left = round(width * (.085 if self.mobile else .067))
        self.right = width - self.left
        self.room = self.right - self.left
        self.body_size = 18 if not self.wide else 17
        self.elements = []
        self.marker_y = None

    def txt(self, x, y, value, size, color=LIGHT, family=SANS, weight=400, italic=False, tracking=0):
        self.elements.append(
            f'<text x="{x:g}" y="{y:g}" fill="{color}" font-family="{family}" font-size="{size:g}" '
            f'font-weight="{weight}" font-style="{"italic" if italic else "normal"}" '
            f'letter-spacing="{tracking:g}">{escape(value)}</text>')

    def line(self, x1, y1, x2, y2, color=LINE):
        self.elements.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" stroke="{color}" fill="none"/>')

    def label(self, value, y, color=MINT):
        size = 12
        self.txt(self.left, y, value.upper(), size, color, MONO, tracking=.9)
        return y

    def heading(self, title, y, size, width=None):
        lines = wrap(title, size, width or self.room, 700)
        for i, item in enumerate(lines):
            self.txt(self.left, y + i * (size + 2), item, size, weight=700, tracking=-.035 * size)
        return y + (len(lines)-1) * (size + 2)

    def mixed(self, start, end, y):
        size = 43 if self.mobile else (40 if self.wide else 34)
        width = font(SANS, size, 700).getlength(start) - .045 * size * len(start)
        self.txt(self.left, y, start, size, weight=700, tracking=-.045*size)
        self.txt(self.left + width + size * .20, y, end, size, MINT, SERIF, italic=True, tracking=-.045*size)

    def prose(self, x, y, value, width, size=None, color=BODY):
        size = size or self.body_size
        lines = wrap(value, size, width)
        leading = round(size * 1.43)
        for i, item in enumerate(lines):
            self.txt(x, y + i * leading, item, size, color)
        return y + (len(lines)-1) * leading

    def finish(self, panel, height, intrinsic_width=None, rail=True):
        physical_width = intrinsic_width or self.width
        physical_height = round(physical_width * height / self.width, 3)
        marker = ""
        if self.marker_y is not None:
            y = self.marker_y
            marker = (f'<circle cx="{self.rail}" cy="{y}" r="4.25" fill="{INK}" stroke="{MINT}"/>'
                      f'<circle cx="{self.rail}" cy="{y}" r="1.3" fill="{MINT}"/>')
        rail_line = f'<path d="M{self.rail} 0v{height}" stroke="#31515a"/>' if rail else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{physical_width}" height="{physical_height:g}" '
                f'viewBox="0 0 {self.width} {height}" role="img" aria-labelledby="title desc">'
                f'<title id="title">{escape(panel.title)}</title><desc id="desc">{escape(panel.alt())}</desc>'
                f'<rect width="100%" height="100%" fill="{INK}"/>{rail_line}{marker}' + "".join(self.elements) + '</svg>\n')


def render(panel, width, intrinsic_width=None):
    c = Canvas(width)
    w, left, right = width, c.left, c.right
    mobile, wide = c.mobile, c.wide
    if panel.kind == "feature":
        if mobile:
            c.label("Featured project  /  Python · Django", 19)
            c.txt(left, 53, panel.title, 27, weight=700, tracking=-.9)
            height = 78
        else:
            c.label("Featured project  /  Python · Django", 21)
            c.txt(left, 48, panel.title, 24, weight=700, tracking=-.8)
            height = 68
        c.line(left, height-1, right, height-1)
    elif panel.kind == "about":
        c.label(panel.label, 43 if mobile else 31)
        c.marker_y = 39 if mobile else 27
        c.mixed("About", "me.", 97 if mobile else 79)
        if not mobile:
            art_w = 130 if wide else 108
            c.elements.append(motif("overview", right-art_w, 12, art_w, 67))
        y = 139 if mobile else 115
        for p in panel.paragraphs:
            measure = min(c.room, 650) if wide else c.room
            y = c.prose(left, y, p, measure) + (36 if mobile else 29)
        height = y+4
    elif panel.kind == "heading":
        c.line(left, 1, right, 1)
        c.label(panel.label, 36 if mobile else 27)
        c.marker_y = 32 if mobile else 23
        if panel.key == "selected-work":
            c.mixed("Selected", "work.", 88 if mobile else 74)
        else:
            c.mixed("Web &", "mobile.", 88 if mobile else 74)
            c.label("Flutter, Django and Python", 117 if mobile else 98, MONO_COLOR)
        height = (110 if mobile else 96) + ((30 if mobile else 24) if panel.key == "more-projects" else 0)
    elif panel.kind == "project":
        c.line(left, 0.5, right, .5)
        art_w = 164 if wide else (68 if mobile else 108)
        art_h = round(art_w * .58)
        if mobile:
            c.elements.append(motif(panel.key, right-art_w, 2, art_w, art_h))
            c.label(panel.label, 33, MONO_COLOR)
            y = c.heading(panel.title, 77, 30)
            text_width = c.room
        else:
            c.elements.append(motif(panel.key, right-art_w, 26, art_w, art_h))
            c.label(panel.label, 24, MONO_COLOR)
            text_width = c.room - art_w - 24
            y = c.heading(panel.title, 56, 27 if wide else 25, text_width)
        y = c.prose(left, y+(34 if mobile else 29), panel.paragraphs[0], text_width)
        y += 34 if mobile else 26
        c.txt(left, y, "View project", 15 if mobile else 14, MINT, weight=700)
        height = y+(25 if mobile else 22)
    elif panel.kind == "skills":
        c.line(left, 1, right, 1)
        c.mixed("Technical", "skills.", 81 if mobile else 72)
        c.marker_y = 68 if mobile else 60
        y = 111 if mobile else 98
        for name, tools in panel.rows:
            c.line(left, y, right, y)
            y = c.heading(name, y+(35 if mobile else 33), 24 if mobile else 23)
            y = c.prose(left, y+(31 if mobile else 27), tools, c.room) + (25 if mobile else 22)
        height = y + (13 if mobile else 14)
    elif panel.kind == "reference":
        c.line(left, 1, right, 1)
        c.marker_y = 58 if mobile else 53
        y = c.heading(panel.title+".", 68 if mobile else 63, 42 if mobile else 38)
        y = c.prose(left, y + (40 if mobile else 32), panel.paragraphs[0], c.room)
        y += 35 if mobile else 27
        c.txt(left, y, panel.detail, 16 if mobile else 15, MINT, weight=700)
        height = y + (35 if mobile else 28)
    elif panel.kind == "contact":
        c.line(left, 1, right, 1)
        c.label(panel.label, 41 if mobile else 31)
        c.marker_y = 37 if mobile else 27
        if not mobile:
            art_w = 100 if wide else 84
            c.elements.append(motif("contact", right-art_w-28, 20, art_w, 56))
        if mobile:
            c.mixed("My", "LinkedIn.", 94)
        else:
            c.mixed("Connect on", "LinkedIn", 79)
        height = 127 if mobile else 104
    else:
        c.line(left, .5, right, .5)
        c.txt(left, 36 if mobile else 31, panel.title, 15, MONO_COLOR)
        height = 58 if mobile else 50
    return c.finish(panel, height, intrinsic_width)


def save_svg(key, variant, source):
    svg = source.encode()
    digest = hashlib.sha256(svg).hexdigest()[:10]
    path = ASSETS / f"{key}-{variant}-{digest}.svg"
    (ROOT / path).write_bytes(svg)
    return path.as_posix()


# A profile has a sidebar on desktop. These native picture sizes keep the
# chapter rail and the paired project rows aligned within GitHub's content column.
CELL_WIDTHS = ((1099, 296), (1219, 350), (1279, 396), (None, 426))


def linked_picture(panel, sources, image):
    source_tags = "".join(
        f'<source media="(max-width: {limit}px)" srcset="{RAW}{path}">'
        for limit, path in sources
    )
    return (f'<a href="{escape(panel.href, quote=True)}"><picture>{source_tags}'
            f'<img align="top" src="{image}" alt="{escape(panel.alt(), quote=True)}">'
            '</picture></a>')


def full_row(panel):
    variants = []
    for limit, width in ((600, 360), (959, 660)):
        path = save_svg(panel.key, f"stack-{width}", render(panel, width, intrinsic_width=1080))
        variants.append((limit, path))
    for limit, cell_width in CELL_WIDTHS:
        width = 660 if cell_width < 396 else 960
        physical_width = 2 * cell_width
        path = save_svg(panel.key, f"row-{physical_width}", render(panel, width, physical_width))
        variants.append((limit, path))
    return '<div align="center">' + linked_picture(panel, variants[:-1], variants[-1][1]) + '</div>'


def project_cell(panel, width, first):
    c = Canvas(width)
    # The rail follows the left edge of the page through both-column rows.
    c.left = round(width / 15) if not first else round(width * .134)
    c.right = width - round(width / 16)
    c.rail = round(width / 15)
    c.room = c.right - c.left
    c.line(c.left, .5, c.right, .5)
    label_size = 10 if width < 360 else 11
    title_size = 21 if width < 360 else 24
    c.txt(c.left, 27, panel.label.upper(), label_size, MONO_COLOR, MONO, tracking=.55)
    art_width = round(width * .135)
    c.elements.append(motif(panel.key, c.right-art_width, 5, art_width, 29))
    y = c.heading(panel.title, 61, title_size)
    y = c.prose(c.left, y+27, panel.paragraphs[0], c.room, 16)
    return c, y


def paired_row(pair):
    # GitHub sanitizes page CSS. A linked picture with an intrinsic width can
    # wrap like a word, retaining its own keyboard and touch target at every size.
    # A phone source wider than its container takes the whole line through
    # GitHub's standard max-width rule; desktop sources sit alongside each other.
    variants = [[], []]
    for i, panel in enumerate(pair):
        for limit, width in ((600, 360), (959, 660)):
            path = save_svg(panel.key, f"stack-{width}", render(panel, width, intrinsic_width=1080))
            variants[i].append((limit, path))
    for limit, width in CELL_WIDTHS:
        cells = [project_cell(panel, width, i == 0) for i, panel in enumerate(pair)]
        height = max(baseline for _, baseline in cells) + 51
        for i, (c, _) in enumerate(cells):
            c.txt(c.left, height-22, "View project", 14, MINT, weight=700)
            if i == 0:
                c.line(width-1, 10, width-1, height-10)
            path = save_svg(pair[i].key, f"cell-{width}", c.finish(pair[i], height, rail=i == 0))
            variants[i].append((limit, path))
    links = [linked_picture(panel, sizes[:-1], sizes[-1][1])
             for panel, sizes in zip(pair, variants)]
    # No whitespace between the pictures: adjacent replaced elements allow a
    # break between images but do not print a strip of GitHub's page background.
    return '<div align="center">' + ''.join(links) + '</div>'


def main():
    (ROOT / ASSETS).mkdir(parents=True, exist_ok=True)
    output = [f"<div>{HERO}</div>"]
    pending = None
    for panel in get_panels():
        if panel.kind == "project":
            if pending is None:
                pending = panel
            else:
                output.append(paired_row((pending, panel)))
                pending = None
        else:
            if pending is not None:
                output.append(full_row(pending))
                pending = None
            output.append(full_row(panel))
    if pending is not None:
        output.append(full_row(pending))
    (ROOT / "README.md").write_text("\n".join(output)+"\n")
    # Older READMEs reference immutable fingerprinted assets through main.


if __name__ == "__main__":
    main()
