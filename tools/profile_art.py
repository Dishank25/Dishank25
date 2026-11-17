"""Small original vector studies for the Abyssal Observatory's project index."""

DEEP = "#0b1922"
SHADOW = "#112830"
GLASS = "#15363d"
TEAL = "#426870"
LINE = "#32515b"
WATER = "#699c9e"
MINT = "#a1ecd7"


def path(d, stroke=LINE, width=1.2, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width:g}" {extra}/>'


def circle(x, y, radius, stroke=TEAL, fill="none", width=1):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def dot(x, y, radius=2, color=MINT):
    return circle(x, y, radius, "none", color)


def echo(x, y):
    return circle(x, y, 5.1, WATER) + dot(x, y, 2.4)


def overview():
    parts = []
    # Submerged shelf contours, each shifting around the same underwater ridge.
    for i in range(7):
        offset = i * 6
        d = f"M{4 + offset} 101 C{13 + offset} 86 {4 + offset} 73 {21 + offset} 65 S{48 + offset} 59 {52 + offset} 44 S{46 + offset} 18 {72 + offset} 3"
        parts.append(path(d, LINE, .85))
    for i in range(4):
        dx = i * 6
        parts.append(path(f"M{121 + dx} 102 Q{152 + dx} 87 {150 + dx} 68 T{162 + dx} 26 Q{174 + dx} 16 {191 + dx} 15", LINE, .8))
    parts.extend([
        path("M31 77 C57 67 72 60 91 49 S134 32 164 28", WATER, .85, extra='stroke-dasharray="2 5"'),
        # Manta observed from above, sweeping around the crest.
        path("M78 40 C82 44 89 48 98 48 C89 39 88 27 87 19 C101 26 109 37 115 42 Q120 43 124 40 Q125 43 122 47 Q125 47 128 45 Q128 49 124 51 C126 61 131 67 143 74 C130 73 114 68 105 57 C103 63 97 67 93 67 Q98 58 98 54 Q86 47 78 40Z", WATER, 1.15, GLASS),
        path("M87 19 Q96 43 116 49 Q129 61 143 74 M116 49 C107 48 100 49 98 54 C88 58 74 55 62 58 S43 67 37 65", MINT, 1.3),
        path("M104 36 L109 45 L114 47 M114 56 L118 61 L124 64", TEAL, .9),
        dot(119, 47, 1.35), echo(164, 28), dot(31, 77, 1.7, WATER)
    ])
    return "".join(parts)


def pawsupport():
    parts = [
        path("M70 61 113 34 165 48 123 77Z", TEAL, 1, SHADOW),
        path("M70 58 113 31 165 45 123 74Z", TEAL, 1, DEEP),
        path("M66 51 110 23 166 37 121 68Z", WATER, 1.1, GLASS),
        path("M63 44 108 16 163 29 118 60Z", WATER, 1.25, SHADOW),
        path("M63 44 118 60 163 29 M118 60V64", MINT, 1.15),
        path("M77 43 103 27 M86 45 115 27 M95 47 112 37", WATER, 1.05),
        path("M124 33 130 37 145 28", MINT, 1.7),
        path("M13 72 C29 72 31 65 42 58 S58 50 69 51", TEAL),
        path("M13 55 C31 53 41 46 63 44", MINT, 1.3),
        path("M23 82 C42 83 45 71 56 66 S65 63 71 62", TEAL),
        path("M91 80 122 89 164 60", LINE, .9, extra='stroke-dasharray="2 4"'),
        dot(13, 72, 1.8, WATER), echo(13, 55), dot(23, 82, 1.8, WATER),
    ]
    return "".join(parts)


def supportpilot():
    parts = []
    for r in (17, 24, 31, 39):
        parts.append(path(f"M{58 + r*.5:.1f} {53 - r*.866:.1f} A{r} {r} 0 0 1 {58 + r*.5:.1f} {53 + r*.866:.1f}", TEAL, .85))
    parts.extend([
        path("M17 25 C45 25 50 41 67 46", TEAL, 1.15),
        path("M12 53 H107", MINT, 1.35),
        path("M24 78 C46 78 54 65 71 60", TEAL, 1.15),
        path("M107 53 120 40 133 53 120 66Z", MINT, 1.35, GLASS),
        path("M133 53 C147 53 147 32 162 32 H180", MINT, 1.35),
        path("M133 53 C148 53 147 75 163 75 H180", WATER, 1, extra='stroke-dasharray="3 4"'),
        circle(180, 75, 3.4, WATER, DEEP), echo(180, 32), dot(120, 53, 2),
        dot(17, 25, 2.5, WATER), echo(12, 53), dot(24, 78, 2.5, WATER),
        path("M107 19 H133 M120 14 V24 M107 83 H133", LINE, .8),
    ])
    return "".join(parts)


def veterinary():
    parts = [
        path("M28 29 65 17 84 26 86 72 33 89Z", TEAL, 1, SHADOW),
        path("M36 23 70 14 86 23 87 68 39 82Z", WATER, 1.2, GLASS),
        path("M70 14 70 28 86 23", WATER, 1.15),
        path("M45 39 62 34 M45 45 69 38 M46 66 70 58", TEAL, .95),
        path("M45 56 51 54 54 47 58 59 61 51 68 49", MINT, 1.4),
        path("M86 47 H100 Q106 47 106 41 V33 Q106 27 113 27 H122 M105 47 V62 Q105 69 113 69 H122", TEAL, 1.1),
        path("M86 47 H122", MINT, 1.4), dot(105, 47, 2, MINT)
    ]
    for n, y in enumerate((21, 42, 63)):
        color = MINT if n == 1 else WATER
        parts.append(path(f"M123 {y} H173 L178 {y+5} V{y+13} H123Z", color, 1.1, SHADOW))
        parts.append(path(f"M135 {y+1} V{y+12} M140 {y+6.5} H162", TEAL, .9))
        parts.append(dot(129, y + 6.5, 1.5, color))
    return "".join(parts)


def recommendations():
    parts = []
    inputs = [(23, 24), (22, 52), (30, 81)]
    outputs = [(158, 19), (166, 46), (158, 71), (145, 90)]
    for i, j in [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2), (1, 3)]:
        start, end = inputs[i], outputs[j]
        parts.append(path(f"M{start[0]} {start[1]} C74 {start[1]} 110 {end[1]} {end[0]} {end[1]}", LINE, 1))
    for i, j in [(1, 0), (2, 1)]:
        s, e = inputs[i], outputs[j]
        parts.append(path(f"M{s[0]} {s[1]} C78 {s[1]} 103 {e[1]} {e[0]} {e[1]}", MINT if i == 1 else WATER, 1.6))
    for x, y in inputs:
        parts.append(circle(x, y, 4.5, WATER, SHADOW))
        parts.append(dot(x, y, 1.5))
    for i, (x, y) in enumerate(outputs):
        parts.append(path(f"M{x-3} {y-3} h6 v6 h-6Z", MINT if i < 2 else TEAL, 1.1, SHADOW))
        parts.append(path(f"M{x+10} {y} h{18-i*4}", MINT if i == 0 else TEAL, 1.7))
    parts.append(path("M77 12 V89 M103 12 V89", LINE, .75, extra='stroke-dasharray="1 5"'))
    return "".join(parts)


def breed():
    parts = [
        path("M52 35 V20 H69 M132 20 H149 V35 M149 69 V84 H132 M69 84 H52 V69", WATER, 1.3),
        path("M70 50 Q69 43 69 28 Q82 31 88 38 Q99 34 110 37 Q119 31 127 26 Q130 39 125 48 Q130 58 123 65 Q114 78 100 80 Q86 79 79 70 Q68 65 70 50Z", WATER, 1.25, SHADOW),
        path("M73 34 76 45 82 40Z M122 33 114 40 123 43Z", TEAL, 1, GLASS),
        path("M79 52 Q83 48 89 51 M107 50 Q115 46 119 49 M94 61 Q100 57 105 60 L100 65Z M100 65 Q97 69 93 68 M100 65 Q103 68 108 66", MINT, 1.3),
        path("M85 60 65 57 M86 64 65 68 M112 58 133 53 M113 63 134 64", WATER, .95),
        path("M26 44 H50 M30 58 H61 M151 52 H162 Q166 52 169 48 L177 40 H186", LINE, .95),
        dot(83, 52, 1.4), dot(115, 50, 1.4), echo(182, 40)
    ]
    return "".join(parts)


def observatory():
    parts = [
        path("M21 79 Q34 35 68 21 Q106 7 146 26 Q169 38 183 65", TEAL, 1.1),
        path("M25 83 Q37 38 72 24 Q110 11 146 31 Q166 42 178 66 L161 76 Q149 51 129 44 Q97 33 76 47 Q61 57 53 79Z", WATER, 1.25, SHADOW),
        path("M38 78 Q50 44 78 32 Q111 21 141 37 Q155 44 168 63 L156 67 Q144 47 127 42 Q97 31 74 46 Q59 54 50 77Z", TEAL, 1, GLASS),
        path("M36 78 Q49 44 78 32 Q110 21 141 37 Q154 44 163 57", MINT, 1.35),
        path("M66 24 76 37 M105 17 105 29 M145 27 139 39", WATER, 1.1),
        path("M19 84 49 82 137 90 180 69 M50 82 64 73 124 79 145 73", TEAL, 1),
        path("M69 66 C84 67 87 56 102 58 Q111 59 116 54 Q112 61 101 62 Q96 70 92 71 Q95 65 94 63 Q82 69 69 66Z", WATER, .85, GLASS),
        dot(112, 56, 1), dot(75, 54, 1.05, WATER), dot(127, 53, 1.1, WATER),
        path("M88 87 112 89 M139 85 148 82", MINT, 1)
    ]
    return "".join(parts)


def portal():
    parts = [
        path("M20 71 67 87 169 54", LINE, 1, extra='stroke-dasharray="2 5"'),
        path("M26 31 71 17 76 20 75 69 31 84 26 82Z", TEAL, 1.05, SHADOW),
        path("M31 34 76 20 75 69 31 84Z", WATER, 1.1, DEEP),
        path("M37 39 69 29 69 62 37 73Z", TEAL, 1, GLASS),
        path("M42 50 53 47 M42 55 61 49 M42 60 55 56", WATER, 1),
        path("M111 30 154 16 160 19 160 67 116 82 111 79Z", TEAL, 1.05, SHADOW),
        path("M116 33 160 19 160 67 116 82Z", WATER, 1.1, DEEP),
        path("M122 38 154 28 154 59 122 70Z", TEAL, 1, GLASS),
        path("M129 51 134 54 145 41", MINT, 1.5),
        path("M60 66 C79 75 87 41 109 47 L118 51 M71 42 C88 29 92 55 107 56", MINT, 1.2),
        dot(60, 66, 1.8), echo(109, 47),
        path("M48 74 58 71 M133 72 143 69", WATER, .85),
    ]
    return "".join(parts)


def discovery():
    parts = []
    for y, knob in [(29, 37), (49, 63), (69, 49)]:
        parts.append(path(f"M20 {y} H77", TEAL, 1.1))
        parts.append(path(f"M20 {y} H{knob}", WATER, 1.1))
        parts.append(circle(knob, y, 3.5, MINT, SHADOW, 1.15))
    parts.extend([
        path("M83 49 H102", WATER, .9, extra='stroke-dasharray="2 3"'),
        circle(130, 49, 28, WATER, SHADOW, 1.25), circle(130, 49, 21, LINE), circle(130, 49, 12, LINE),
        path("M105 49 H154 M130 25 V74", LINE, .7),
        path("M130 49 149 31 Q153 35 155 41Z", WATER, .85, GLASS),
        path("M130 49 149 31", MINT, 1.25),
        path("M149 70 166 87 172 81 155 64", WATER, 1.1, SHADOW),
        path("M161 77 167 82", MINT, 1.05),
        dot(140, 40, 2.1), dot(120, 57, 1.3, WATER), dot(133, 65, 1.3, WATER),
    ])
    return "".join(parts)


def tic_tac_toe():
    parts = [
        path("M46 16 H143 L151 23 V85 H46Z", WATER, 1.1, SHADOW),
        path("M46 26 H151 M52 91 H145", LINE, 1),
        dot(52, 21, 1, MINT), dot(57, 21, 1, TEAL), dot(62, 21, 1, TEAL),
        path("M87 29 V79 M107 29 V79 M68 44 H126 M68 62 H126", TEAL, .95),
        path("M19 48 H36 M24 55 H38 M157 69 H178", LINE, 1),
    ]
    for x, y in [(77, 36), (97, 53), (117, 71)]:
        parts.append(path(f"M{x-3} {y-3} l6 6 M{x+3} {y-3} l-6 6", MINT, 1.5))
    for x, y in [(117, 36), (77, 54), (97, 71)]:
        parts.append(circle(x, y, 3.7, WATER, "none", 1.25))
    return "".join(parts)


def contact():
    parts = [
        path("M25 81 Q41 73 57 79 T91 79 Q103 74 115 77", LINE, .95),
        path("M16 86 Q35 77 56 84 T91 84", TEAL, .95),
        path("M42 73 55 67 66 72 56 78Z", WATER, 1, GLASS),
        path("M55 67 55 61 73 48", MINT, 1.2),
        path("M61 51 Q73 62 85 54 Q79 42 72 39Z", WATER, 1.1, GLASS),
        path("M72 39 Q71 46 85 54", MINT, 1.1),
        path("M83 44 149 20", TEAL, .9, extra='stroke-dasharray="2 4"'),
        dot(77, 47, 1.65), echo(151, 19)
    ]
    for delta, radius in [(0, 12), (12, 23), (25, 34), (39, 44)]:
        x = 83 + delta
        parts.append(path(f"M{x} {35-delta*.4:g} A{radius} {radius} 0 0 1 {x+7+delta*.15:g} {50+delta*.17:g}", MINT if delta == 0 else TEAL, 1.1))
    return "".join(parts)


STUDIES = {
    "overview": overview, "pawsupport": pawsupport, "supportpilot": supportpilot,
    "veterinary-records": veterinary, "recommendations": recommendations,
    "breed-identification": breed, "abyssal-portfolio": observatory,
    "job-portal": portal, "job-discovery": discovery, "terminal-tic-tac-toe": tic_tac_toe,
    "contact": contact,
}


def motif(kind, x, y, width, height):
    """Place a line drawing in an arbitrary bounding box without stretching it."""
    drawing = STUDIES[kind]()
    return (
        f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 200 105" '
        f'preserveAspectRatio="xMidYMid meet" overflow="hidden" aria-hidden="true" '
        f'stroke-linecap="round" stroke-linejoin="round">{drawing}</svg>'
    )
