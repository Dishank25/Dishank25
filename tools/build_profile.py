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
HERO_ALT = ("Dishank Jain, AI engineer. An illustrated engineer watches a luminous manta through the window "
            "of a deep-sea observatory. Open the portfolio.")
HERO_REV = "https://raw.githubusercontent.com/Dishank25/Dishank25/2a100f4d9834131c5c129b0d8cfeea1d2d21182d/assets/"


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
NARROW_DESKTOP_UNTIL = 1249


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
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{natural}" height="{round(natural*height/self.width)}" '
                f'viewBox="0 0 {self.width} {height}" preserveAspectRatio="none" style="background-color:{INK}" role="img" aria-labelledby="title desc">'
                f'<title id="title">{escape(panel.title)}</title><desc id="desc">{escape(panel.alt())}</desc>'
                f'<rect width="100%" height="100%" fill="{INK}"/>{track}' + ''.join(self.parts) + '</svg>\n')


def chapter_svg(panel, layout, intrinsic_width):
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
    return c.svg(panel, y + 24, intrinsic_width)


def project_cell(panel, layout, column=None):
    if column is None:
        c = Canvas(layout)
    else:
        width = layout.width // 2
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


def project_svgs(panels, layout, intrinsic_width, *, stacked=False):
    pair = len(panels) == 2 and not stacked
    cells = [project_cell(p, layout, i if pair else None) for i, p in enumerate(panels)]
    shared_height = max(y for _, y in cells) + 55
    result = []
    for i, (c, y) in enumerate(cells):
        height = shared_height if pair else y + 55
        c.action(height-24, "View project")
        result.append(c.svg(panels[i], height, natural_width=intrinsic_width))
    return result


def write_svg(key, variant, source):
    svg = source.encode()
    digest = hashlib.sha256(svg).hexdigest()[:10]
    path = ASSETS / f"{key}-{variant}-{digest}.svg"
    (ROOT / path).write_bytes(svg)
    return path.as_posix()


# Modern browsers use the selected source's percentage width. Providing an
# intrinsic canvas too keeps older renderers aligned if they ignore that hint.
# Columns are ordinary adjacent links; float padding would expose GitHub's page.
SIZES = ((440, PHONE, 1200), (600, LARGE_PHONE, 1200), (STACK_UNTIL, TABLET, 1200),
         (NARROW_DESKTOP_UNTIL, SMALL_DESKTOP, 608), (None, DESKTOP, 800))


def picture(sources, fallback, alt):
    tags = []
    for limit, url, width in sources:
        media = f' media="(max-width: {limit}px)"' if limit is not None else ""
        tags.append(f'<source{media} srcset="{url}" width="{width}%">')
    return (f'<picture>{"".join(tags)}<img align="top" src="{fallback}" '
            f'alt="{escape(alt, quote=True)}"></picture>')


def anchor(url, artwork):
    return f'<a href="{escape(url, quote=True)}">{artwork}</a>'


def row(links):
    # Intervening whitespace between two half-width images can force a line break.
    return '<div align="center">' + ''.join(links) + '</div>'


def hero():
    wide = RAW + "assets/observatory-breathing.svg"
    portrait = HERO_REV + "observatory-breathing-mobile.svg"
    # Keep the original animated files byte-for-byte. Density descriptors assign
    # the same fallback sizes as body panels (original widths are 960 and 420).
    choices = [(600, portrait + ' 0.35x', 100), (STACK_UNTIL, wide + ' 0.8x', 100),
               (NARROW_DESKTOP_UNTIL, wide + ' 1.57894737x', 100), (None, wide + ' 1.2x', 100)]
    return row([anchor(SITE, picture(choices, "assets/observatory-breathing.svg", HERO_ALT))])


def chapter(panel):
    sources = []
    for limit, layout, natural in SIZES:
        if panel.kind == "project":
            svg = project_svgs([panel], layout, natural)[0]
        else:
            svg = chapter_svg(panel, layout, natural)
        path = write_svg(panel.key, layout.width, svg)
        sources.append((limit, RAW + path, 100))
    return row([anchor(panel.href, picture(sources, path, panel.alt()))])


def project_pair(pair):
    variants = [[], []]
    for limit, layout, natural in SIZES:
        stacked = limit is not None and limit <= STACK_UNTIL
        artwork = project_svgs(pair, layout, natural if stacked else natural // 2, stacked=stacked)
        for i, (panel, svg) in enumerate(zip(pair, artwork)):
            path = write_svg(panel.key, f"{layout.width}-{'stack' if stacked else 'column'}", svg)
            variants[i].append((limit, RAW + path, 100 if stacked else 50))
    return row([anchor(panel.href, picture(sources, sources[-1][1].removeprefix(RAW), panel.alt()))
                for panel, sources in zip(pair, variants)])


def main():
    (ROOT / ASSETS).mkdir(parents=True, exist_ok=True)
    output = [hero()]
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
                output.append(chapter(pending))
                pending = None
            output.append(chapter(panel))
    if pending:
        output.append(chapter(pending))
    (ROOT / "README.md").write_text("\n".join(output) + "\n")
    # Retain older hashed assets: historical README source URLs resolve through main.


if __name__ == "__main__":
    main()
