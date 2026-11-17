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
  <img align="top" src="assets/observatory-breathing.svg" width="100%" alt="Dishank Jain, AI engineer. An illustrated engineer watches a luminous manta through the window of a deep-sea observatory. Open the portfolio.">
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
    sections = re.split(r"^#{2,3} (.+)$", (ROOT / "PROFILE.md").read_text(), flags=re.M)
    body = dict(zip(sections[1::2], sections[2::2]))
    about = tuple(body["About me"].strip().split("\n\n"))
    projects = []
    for group in ("AI engineering projects", "Web, mobile, and Python projects"):
        for name, narrative, url in re.findall(r"^- \*\*(.+?)\.\*\* (.+?) \[[^\]]+\]\((https://dishank25.github.io/[^)]+)\)", body[group], re.M):
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            projects.append(Panel(slug, "project", name, url, PROJECT_LABELS[slug], (narrative,)))
    featured = next(p for p in projects if p.key == "abyssal-portfolio")
    yield Panel("featured", "feature", featured.title, featured.href, "Featured project / Python · Django",
                featured.paragraphs, detail="View project")
    yield Panel("about", "about", "About me", SITE + "#about", "Noida, India", about)
    yield Panel("my-works", "heading", "My works", SITE + "#work")
    yield from (p for p in projects if p.key != featured.key)

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


@dataclass(frozen=True)
class Layout:
    """All type and horizontal coordinates are in the page's viewBox units."""
    width: int
    margin: int
    rail: int
    section: int
    title: int
    body: int
    label: int
    action: int


# Page ratios match the anchors in the illustrated hero (63/960 and 36/420).
PHONE = Layout(360, 31, 15, 32, 22, 16, 11, 14)
LARGE_PHONE = Layout(475, 40, 20, 33, 23, 17, 11, 15)
TABLET = Layout(660, 44, 22, 34, 23, 16, 11, 14)
SMALL_DESKTOP = Layout(800, 53, 27, 35, 23, 16, 11, 14)
DESKTOP = Layout(920, 60, 31, 40, 26, 18, 12, 16)
STACK_UNTIL = 1023
NARROW_DESKTOP_UNTIL = 1199
COLUMN_PERCENT = 47
GHOST = ASSETS / "inline-layout.svg"


class Canvas:
    def __init__(self, layout, width=None, left=None, right=None, rail=True):
        self.layout = layout
        self.width = width or layout.width
        self.left = layout.margin if left is None else left
        self.right = self.width - layout.margin if right is None else right
        self.room = self.right - self.left
        self.rail = rail
        self.parts = []

    def text(self, x, y, value, size, *, family=SANS, color=LIGHT, weight=400, italic=False, tracking=0):
        self.parts.append(
            f'<text x="{x:g}" y="{y:g}" fill="{color}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" font-style="{"italic" if italic else "normal"}" '
            f'letter-spacing="{tracking:g}">{escape(value)}</text>')

    def line(self, x1, y1, x2, y2):
        self.parts.append(f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}" stroke="{LINE}" fill="none"/>')

    def marker(self, y):
        self.parts.append(f'<circle cx="{self.layout.rail}" cy="{y}" r="4" fill="{INK}" stroke="{MINT}"/>'
                          f'<circle cx="{self.layout.rail}" cy="{y}" r="1.2" fill="{MINT}"/>')

    def label(self, value, y):
        self.text(self.left, y, value.upper(), self.layout.label, family=MONO, color=MONO_COLOR, tracking=.7)

    def text_lines(self, y, value, available=None, *, heading=False):
        size = self.layout.title if heading else self.layout.body
        weight = 700 if heading else 400
        lines = wrap(value, size, available or self.room, weight)
        leading = round(size * (1.17 if heading else 1.5))
        for item in lines:
            self.text(self.left, y, item, size, weight=weight,
                      color=LIGHT if heading else BODY, tracking=-.025 * size if heading else 0)
            y += leading
        return y - leading

    def chapter(self, first, last):
        self.line(self.left, .5, self.right, .5)
        size = self.layout.section
        y = 25 + size
        self.marker(y - size // 3)
        self.text(self.left, y, first, size, weight=700, tracking=-.04 * size)
        if last:
            word_width = font(SANS, size, 700).getlength(first) - .04 * size * len(first)
            self.text(self.left + word_width + .22 * size, y, last, size, family=SERIF, italic=True,
                      color=MINT, tracking=-.04 * size)
        return y

    def action(self, y, value):
        self.text(self.left, y, value, self.layout.action, color=MINT, weight=700)

    def svg(self, panel, height, natural_width=None):
        natural = natural_width or self.width
        track = (f'<path d="M{self.layout.rail} 0v{height}" stroke="#31515a"/>' if self.rail else '')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{natural}" height="{natural*height/self.width:g}" '
                f'viewBox="0 0 {self.width} {height}" role="img" aria-labelledby="title desc">'
                f'<title id="title">{escape(panel.title)}</title><desc id="desc">{escape(panel.alt())}</desc>'
                f'<rect width="100%" height="100%" fill="{INK}"/>{track}' + ''.join(self.parts) + '</svg>\n')


def chapter_svg(panel, layout):
    c = Canvas(layout)
    k = panel.kind
    if k == "feature":
        c.label(panel.label, 27)
        y = c.text_lines(27 + 11 + layout.title, panel.title, heading=True)
        y = c.text_lines(y + 28, panel.paragraphs[0], min(c.room, 685)) + 31
        c.action(y, panel.detail)
    elif k == "about":
        y = c.chapter("About", "me")
        c.label(panel.label, y + 26)
        if layout is DESKTOP:
            c.parts.append(motif("overview", c.right-111, 16, 111, 56))
        y += 55
        for paragraph in panel.paragraphs:
            y = c.text_lines(y, paragraph, min(c.room, 685)) + 26
        y -= 26
    elif k == "heading":
        y = c.chapter("My", "works")
    elif k == "skills":
        y = c.chapter("Technical", "skills")
        for name, tools in panel.rows:
            y += 22
            c.line(c.left, y, c.right, y)
            y = c.text_lines(y + 33, name, heading=True)
            y = c.text_lines(y + 27, tools)
    elif k == "reference":
        y = c.chapter(panel.title, "")
        y = c.text_lines(y + 32, panel.paragraphs[0], min(c.room, 685))
        y += 31
        c.action(y, panel.detail)
    elif k == "contact":
        y = c.chapter("Connect", "")
        y += 34
        c.action(y, panel.title)
        if layout is not PHONE:
            c.parts.append(motif("contact", c.right-82, 18, 82, 49))
    else:
        c.line(c.left, .5, c.right, .5)
        y = 32
        c.action(y, panel.title)
    return c.svg(panel, y + 24)


def project_cell(panel, layout, column=None):
    if column is None:
        c = Canvas(layout)
    else:
        width = round(layout.width * COLUMN_PERCENT / 100)
        gutter = layout.margin // 2
        c = Canvas(layout, width, layout.margin if column == 0 else gutter,
                   width - (gutter if column == 0 else layout.margin), rail=(column == 0))
    c.line(c.left, .5, c.right, .5)
    art_width = 51 if c.room < 300 else 70
    c.parts.append(motif(panel.key, c.right-art_width, 4, art_width, 29))
    c.label(panel.label, 25)
    y = c.text_lines(25+15+layout.title, panel.title, heading=True)
    y = c.text_lines(y + 28, panel.paragraphs[0], min(c.room, 685))
    return c, y


def project_svgs(panels, layout, *, stacked=False):
    pair = len(panels) == 2 and not stacked
    cells = [project_cell(p, layout, i if pair else None) for i, p in enumerate(panels)]
    shared_height = max(y for _, y in cells) + 55
    result = []
    for i, (c, y) in enumerate(cells):
        height = shared_height if pair else y + 55
        c.action(height-24, "View project")
        result.append(c.svg(panels[i], height, natural_width=1200 if stacked else None))
    return result


def write_svg(key, variant, source):
    svg = source.encode()
    digest = hashlib.sha256(svg).hexdigest()[:10]
    path = ASSETS / f"{key}-{variant}-{digest}.svg"
    (ROOT / path).write_bytes(svg)
    return path.as_posix()


def picture(sources, image, alt, width=None, align="top"):
    # Whitespace between adjacent images reserves space and can wrap the last cell.
    attributes = f' width="{width}"' if width else ''
    tags = []
    for limit, path in sources:
        dimensions = ' width="0" height="0"' if path == GHOST.as_posix() else ''
        tags.append(f'<source media="(max-width: {limit}px)" srcset="{RAW}{path}"{dimensions}>')
    tags = ''.join(tags)
    return (f'<picture>{tags}<img align="{align}"{attributes} src="{image}" '
            f'alt="{escape(alt, quote=True)}"></picture>')


def anchor(panel, inside):
    return f'<a href="{escape(panel.href, quote=True)}">{inside}</a>'


def chapter(panel):
    paths = [write_svg(panel.key, layout.width, chapter_svg(panel, layout))
             for layout in (PHONE, LARGE_PHONE, TABLET, SMALL_DESKTOP, DESKTOP)]
    widths = [(440, paths[0]), (600, paths[1]), (STACK_UNTIL, paths[2]), (NARROW_DESKTOP_UNTIL, paths[3])]
    return '<div>' + anchor(panel, picture(widths, paths[4], panel.alt(), "100%")) + '</div>'


def single_project(panel):
    # Keep the full index usable when the collection grows to an odd count.
    paths = [write_svg(panel.key, f"{layout.width}-single", project_svgs([panel], layout)[0])
             for layout in (PHONE, LARGE_PHONE, TABLET, SMALL_DESKTOP, DESKTOP)]
    return '<div>' + anchor(panel, picture([(440, paths[0]), (600, paths[1]), (STACK_UNTIL, paths[2]), (NARROW_DESKTOP_UNTIL, paths[3])],
                                           paths[4], panel.alt(), "100%")) + '</div>'


def project_pair(pair):
    variants = []
    for layout, stacked in ((PHONE, True), (LARGE_PHONE, True), (TABLET, True), (SMALL_DESKTOP, False), (DESKTOP, False)):
        suffix = f"{layout.width}-{'stack' if stacked else 'column'}"
        variants.append([write_svg(p.key, suffix, art)
                         for p, art in zip(pair, project_svgs(pair, layout, stacked=stacked))])
    links = []
    for i, panel in enumerate(pair):
        # GitHub's stylesheet adds inward padding to floated images. Opposing
        # floats anchor the painted outer edges to the hero while keeping room
        # for that padding. A zero-height float never creates a mobile line box.
        desktop = picture([(STACK_UNTIL, GHOST.as_posix()), (NARROW_DESKTOP_UNTIL, variants[3][i])],
                          variants[4][i], panel.alt(), f"{COLUMN_PERCENT}%", "left" if i == 0 else "right")
        phone = picture([(440, variants[0][i]), (600, variants[1][i]), (STACK_UNTIL, variants[2][i])],
                        GHOST.as_posix(), "")
        links.append(anchor(panel, desktop + phone))
    return '<div>' + ''.join(links) + '</div>'


def main():
    (ROOT / ASSETS).mkdir(parents=True, exist_ok=True)
    # GitHub permits art-directed pictures but strips custom page styles. A
    # transparent no-content source retires the alternative painting while one
    # anchor keeps the same case-study destination and accessible name in both.
    (ROOT / GHOST).write_text('<svg xmlns="http://www.w3.org/2000/svg" width=".001" height=".000001" '
                             'viewBox="0 0 1000 1"/>\n')
    output = [f'<div>{HERO}</div>']
    pending = None
    for panel in get_panels():
        if panel.kind == "project":
            if pending is None:
                pending = panel
            else:
                output.append(project_pair((pending, panel)))
                pending = None
        else:
            if pending is not None:
                output.append(single_project(pending))
                pending = None
            output.append(chapter(panel))
    if pending:
        output.append(single_project(pending))
    (ROOT / "README.md").write_text("\n".join(output) + "\n")
    # Retain older hashed assets: historical README source URLs resolve through main.


if __name__ == "__main__":
    main()
