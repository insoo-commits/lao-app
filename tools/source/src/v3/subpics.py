# Lao app: one flat picture per 소분류 (RYU 2026-11-24: "소그룹별 그림도 넣어주고").
# Helpers from the hotel English app (pics.py); output: SP = {sub id: svg string}.
import json
from pics import svg, r, c, ln, person, floor, desk, chair, bottle, glass, W, H, INK, SKIN

LF = "font-family=\"'Lao Local','Noto Sans Lao Looped','Noto Sans Lao',sans-serif\""
KF = "font-family=\"'Pretendard','Noto Sans KR',sans-serif\""
def t(x, y, s, size=16, fill=INK, anchor="middle", lao=True, w="700", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {LF if lao else KF} {extra}>{s}</text>'

# ---------- palette
SINH = ["#9a3b2e", "#6a3d7a", "#2f6a5a", "#b5651d", "#3b5a8a"]   # women's sinh skirts
SHIRT = ["#f1e3c6", "#5b7fa6", "#c25e4f", "#6d8c5e", "#e9a15b", "#ffffff", "#8a6a9a"]
HAIR, HAIR2 = "#2b1d16", "#4a3426"
WALL, WALL2, FLOOR = "#f3e8d6", "#e9dcc4", "#c9ab84"
GOLD, TEAK, TEAL = "#d49a2e", "#8a4a16", "#2fa59a"

def room(col=WALL, fl=FLOOR, y=200): return r(0, 0, W, y, col) + floor(y, fl)
def sky(col1="#cfe6ef", col2="#f6ead2", y=190, ground="#9cbf7a"):
    return (f'<defs><linearGradient id="g{col1[1:]}{col2[1:]}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col1}"/><stop offset="1" stop-color="{col2}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{y}" fill="url(#g{col1[1:]}{col2[1:]})"/>' + floor(y, ground))
def sun(x, y, rad=24, col="#f6c453"): return c(x, y, rad, col)
def cloud(x, y, s=1.0, col="#ffffff"):
    return c(x, y, 16 * s, col) + c(x + 18 * s, y - 8 * s, 20 * s, col) + c(x + 38 * s, y, 16 * s, col) + r(x, y, 38 * s, 16 * s, col)
def palm(x, foot, h=110, col="#5f8f52"):
    top = foot - h
    out = [f'<path d="M{x},{foot} Q{x+8},{foot-h/2} {x+2},{top}" stroke="#8a6a4a" stroke-width="7" fill="none"/>']
    for dx, dy in [(-46, 10), (-36, -14), (40, 12), (34, -16), (0, -26)]:
        out.append(f'<path d="M{x+2},{top} Q{x+2+dx/2},{top+dy-14} {x+2+dx},{top+dy}" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    return "".join(out)
def stupa(x, foot, s=1.0, col=GOLD):
    return "".join([r(x - 60 * s, foot - 16 * s, 120 * s, 16 * s, "#e2b65a"), r(x - 44 * s, foot - 30 * s, 88 * s, 14 * s, "#e8c26c"),
                    f'<path d="M{x-30*s},{foot-30*s} Q{x-30*s},{foot-62*s} {x},{foot-66*s} Q{x+30*s},{foot-62*s} {x+30*s},{foot-30*s} Z" fill="{col}"/>',
                    f'<path d="M{x-12*s},{foot-64*s} Q{x-4*s},{foot-100*s} {x},{foot-130*s} Q{x+4*s},{foot-100*s} {x+12*s},{foot-64*s} Z" fill="{col}"/>',
                    "".join(f'<path d="M{x+dx*s-5*s},{foot-30*s} L{x+dx*s},{foot-54*s} L{x+dx*s+5*s},{foot-30*s} Z" fill="#e8c26c"/>' for dx in (-52, -40, 40, 52))])
def temple(x, foot, s=1.0):
    return "".join([r(x - 50 * s, foot - 46 * s, 100 * s, 46 * s, "#f4ead6"), r(x - 12 * s, foot - 32 * s, 24 * s, 32 * s, TEAK, 2),
                    f'<path d="M{x-74*s},{foot-42*s} L{x-48*s},{foot-70*s} L{x+48*s},{foot-70*s} L{x+74*s},{foot-42*s} Z" fill="#b5442e"/>',
                    f'<path d="M{x-54*s},{foot-68*s} L{x-30*s},{foot-96*s} L{x+30*s},{foot-96*s} L{x+54*s},{foot-68*s} Z" fill="#c9562f"/>',
                    f'<path d="M{x-32*s},{foot-94*s} L{x},{foot-122*s} L{x+32*s},{foot-94*s} Z" fill="#b5442e"/>',
                    ln([(x - 74 * s, foot - 42 * s), (x - 82 * s, foot - 52 * s)], GOLD, 4 * s), ln([(x + 74 * s, foot - 42 * s), (x + 82 * s, foot - 52 * s)], GOLD, 4 * s),
                    ln([(x, foot - 122 * s), (x, foot - 134 * s)], GOLD, 3 * s)])
def stilt_house(x, foot, s=1.0):
    return "".join([r(x - 60 * s, foot - 60 * s, 8 * s, 60 * s, TEAK), r(x + 52 * s, foot - 60 * s, 8 * s, 60 * s, TEAK), r(x - 4 * s, foot - 60 * s, 8 * s, 60 * s, TEAK),
                    r(x - 66 * s, foot - 110 * s, 132 * s, 54 * s, "#b07a45"), r(x - 30 * s, foot - 98 * s, 22 * s, 22 * s, "#f3e8d6", 2), r(x + 14 * s, foot - 98 * s, 22 * s, 22 * s, "#f3e8d6", 2),
                    f'<path d="M{x-80*s},{foot-108*s} L{x},{foot-150*s} L{x+80*s},{foot-108*s} Z" fill="#7a4a24"/>',
                    ln([(x + 70 * s, foot), (x + 50 * s, foot - 58 * s)], TEAK, 4 * s)])
def basket(x, y, s=1.0):   # sticky rice basket (ຕິບເຂົ້າ)
    return "".join([f'<path d="M{x-14*s},{y-30*s} Q{x},{y-40*s} {x+14*s},{y-30*s} L{x+10*s},{y} L{x-10*s},{y} Z" fill="#d8b26a" stroke="#a07c3c" stroke-width="1.5"/>',
                    ln([(x - 12 * s, y - 18 * s), (x + 12 * s, y - 18 * s)], "#a07c3c", 1.5), r(x - 12 * s, y - 2, 24 * s, 5 * s, "#a07c3c", 2)])
def bowl(x, y, col="#ffffff", food="#d9663b"):
    return f'<path d="M{x-20},{y-12} Q{x},{y+8} {x+20},{y-12} Z" fill="{col}" stroke="#c9ced2" stroke-width="1.5"/>' + f'<ellipse cx="{x}" cy="{y-13}" rx="17" ry="4" fill="{food}"/>'
def table(x, y, w=170, col="#a5825c"): return r(x, y, w, 10, col, 3) + r(x + 12, y + 10, 8, 46, "#8a6a4a") + r(x + w - 20, y + 10, 8, 46, "#8a6a4a")
def board(x, y, w, h, lines, col="#2f5a46", ink="#f6f1e0"):
    out = [r(x - 6, y - 6, w + 12, h + 12, "#a5825c", 4), r(x, y, w, h, col, 2)]
    n = len(lines); gap = h / (n + 1)
    for i, (s, size, lao) in enumerate(lines):
        out.append(t(x + w / 2, y + gap * (i + 1) + size * 0.35, s, size, ink, lao=lao, w="600"))
    return "".join(out)
def bubble(x, y, s, w=70, size=18, lao=True, col="#ffffff", tail="l"):
    # RYU 2026-11-24: a bubble never covers a head: move it up, or sideways when there is no room above
    import pics as _P
    for hx, hy, hr in list(_P.HEADS):
        if hx + hr > x - 10 and hx - hr < x + w + 10 and hy - hr < y + 50 and hy + hr > y:
            ny = hy - hr - 50
            if ny >= 2: y = ny
            else:
                y = max(2, y)
                x = hx + hr + 12 if hx < x + w / 2 else hx - hr - w - 12
                x = min(max(12, x), 400 - w - 12)
    tl = f"l-10,10 l2,-10" if tail == "l" else f"l10,10 l-2,-10"
    if tail == "l":
        d = f"M{x},{y} h{w} a10,10 0 0 1 10,10 v18 a10,10 0 0 1 -10,10 h-{w-18} l-10,10 l2,-10 h-8 a10,10 0 0 1 -10,-10 v-18 a10,10 0 0 1 10,-10 z"
    else:
        d = f"M{x},{y} h{w} a10,10 0 0 1 10,10 v18 a10,10 0 0 1 -10,10 h-8 l2,10 l-10,-10 h-{w-28} a10,10 0 0 1 -10,-10 v-18 a10,10 0 0 1 10,-10 z"
    return f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="1.6"/>' + t(x + w / 2, y + 26, s, size, INK, lao=lao)
def card(x, y, s, w=64, h=50, col="#ffffff", size=26, ink=INK, lao=True, sub=None):
    out = [r(x, y, w, h, col, 8, f'stroke="{INK}" stroke-width="1.5"'), t(x + w / 2, y + h / 2 + size * 0.36 - (6 if sub else 0), s, size, ink, lao=lao)]
    if sub: out.append(t(x + w / 2, y + h - 7, sub, 11, "#7a6a5a", lao=False, w="500"))
    return "".join(out)
def waves(x, y, col="#c25e4f", n=3):
    return "".join(f'<path d="M{x+i*9},{y-8-i*5} Q{x+8+i*11},{y} {x+i*9},{y+8+i*5}" stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round"/>' for i in range(n))
def W_(i, female=None, x=0, foot=0, **k):   # Lao person: woman in sinh or man
    if female:
        return person(x, foot, SHIRT[i % len(SHIRT)], SINH[i % len(SINH)], HAIR, female=True, **k)
    return person(x, foot, SHIRT[(i + 2) % len(SHIRT)], "#3b4a5a", HAIR2 if i % 2 else HAIR, **k)
def two_talk(a, b, bg, ia=0, ib=1, fa=True, fb=False, size=18, wa=None, wb=None, extra=""):
    wa = wa or max(54, len(a) * size * 0.62); wb = wb or max(54, len(b) * size * 0.62)
    return bg + extra + W_(ia, fa, 130, 236, arms=[[(0, 0), (16, 20), (30, 28)]]) + W_(ib, fb, 270, 236, arms=[[(0, 0), (-16, 20), (-30, 28)]]) \
        + bubble(max(10, 130 - wa / 2 - 10), 34, a, wa, size) + bubble(min(W - wb - 30, 262 - wb / 2), 74, b, wb, size, tail="r")
def teacher_board(lines, bw=250, extra="", col="#2f5a46"):
    return svg("".join([room("#efe4cf", "#c9ab84", 205), board(110, 26, bw, 120, lines, col), W_(3, True, 66, 236, arms=[[(0, 0), (20, -20), (40, -46)]]), extra]))
def speaker(lines_cards, col="#c25e4f", bg="#f6ecdc"):
    out = [r(0, 0, W, H, bg), W_(2, True, 70, 250, arms=[[(0, 0), (14, 18), (26, 22)]]), waves(104, 104, col)]
    for (x, y, s, sub, cc) in lines_cards: out.append(card(x, y, s, 70, 58, cc, 26, sub=sub))
    return svg("".join(out), bg)
def tone_curve(x, y, w, kind, col):
    d = {"mid": f"M{x},{y} h{w}", "rise": f"M{x},{y+14} Q{x+w*.6},{y+12} {x+w},{y-14}", "fall": f"M{x},{y-14} Q{x+w*.4},{y-14} {x+w},{y+14}",
         "low": f"M{x},{y+10} h{w}", "high": f"M{x},{y-12} h{w}", "hf": f"M{x},{y-6} Q{x+w*.3},{y-18} {x+w},{y+14}"}[kind]
    return f'<path d="{d}" stroke="{col}" stroke-width="4" fill="none" stroke-linecap="round"/>'

SP = {}
# ===================== P5 기초회화 (scenes)
SP["P5-K"] = svg(two_talk("ສະບາຍດີ", "ສະບາຍດີ", sky("#d8ecf2", "#f7ecd8", 200, "#b9cf8f"), extra=temple(330, 200, .55) + palm(40, 200, 100)))
SP["P5-J"] = svg("".join([room(), c(200, 92, 64, "#ffffff", f'stroke="{TEAK}" stroke-width="6"'),
    "".join(t(200 + 50 * __import__("math").sin(i * 3.14159 / 6), 92 - 50 * __import__("math").cos(i * 3.14159 / 6) + 6, ["໑໒", "໑", "໒", "໓", "໔", "໕", "໖", "໗", "໘", "໙", "໑໐", "໑໑"][i], 13, INK) for i in range(12)),
    ln([(200, 92), (200, 56)], INK, 4), ln([(200, 92), (228, 104)], INK, 4), c(200, 92, 4, INK),
    card(30, 190, "໑", 52, 46, "#fff4dc", 26), card(90, 190, "໒", 52, 46, "#fff4dc", 26), card(258, 190, "໓", 52, 46, "#fff4dc", 26), card(318, 190, "໔", 52, 46, "#fff4dc", 26)]))
SP["P5-B"] = svg("".join([room("#f6e6cc", "#b98d5e", 196), r(30, 30, 110, 70, "#fffaf0", 4, f'stroke="{TEAK}" stroke-width="3"'), t(85, 58, "ເມນູ", 18, TEAK),
    r(46, 70, 78, 4, "#c9b79c"), r(46, 80, 60, 4, "#c9b79c"), table(70, 168, 200), basket(110, 168), bowl(160, 168), bowl(208, 168, food="#6e9a64"),
    W_(1, False, 60, 250, arms=[[(0, 0), (20, 10), (36, 2)]], scale=.9), W_(0, True, 320, 250, arms=[[(0, 0), (-24, 14), (-40, 10)]], scale=.95), bubble(196, 34, "ເອົາອັນນີ້", 84, 16, tail="r")]))
SP["P5-C"] = svg("".join([sky("#f3e2c3", "#f6ecdc", 200, "#c9ab84"), f'<path d="M30,60 L370,60 L350,30 L50,30 Z" fill="#c25e4f"/>', "".join(r(50 + i * 64, 30, 32, 30, "#f3e2c3") for i in range(5)),
    r(40, 140, 320, 14, TEAK, 3), r(50, 154, 10, 46, TEAK), r(340, 154, 10, 46, TEAK),
    "".join(c(80 + i * 18, 132, 9, "#f2b134") for i in range(4)), "".join(c(180 + i * 16, 130, 10, "#e0503a") for i in range(4)), "".join(c(272 + i * 16, 132, 9, "#7cae3f") for i in range(4)),
    W_(0, True, 200, 140, scale=.7), W_(5, False, 330, 252, arms=[[(0, 0), (-18, 12), (-32, 4)]], scale=.9), bubble(232, 70, "ເທົ່າໃດ?", 70, 16, tail="r")]))
tuk = lambda x, y: "".join([r(x, y - 60, 110, 52, "#2f6a8a", 8), r(x + 8, y - 54, 40, 26, "#cfe6ef", 3), r(x + 54, y - 54, 48, 26, "#cfe6ef", 3), f'<path d="M{x-4},{y-62} h118 l-8,-14 h-102 z" fill="#c25e4f"/>',
    r(x - 30, y - 34, 40, 26, "#2f6a8a", 6), c(x - 18, y - 4, 11, INK), c(x + 30, y - 4, 11, INK), c(x + 92, y - 4, 11, INK)])
SP["P5-E"] = svg("".join([sky("#cfe6ef", "#f2ead6", 196, "#bfb19a"), r(0, 216, W, 10, "#f3efe4"), tuk(150, 228), palm(360, 196, 100), cloud(50, 50), cloud(260, 40, .8),
    W_(4, False, 60, 250, arms=[[(0, 0), (16, -22), (28, -46)]], scale=.9), bubble(90, 60, "ໄປໃສ?", 60, 16)]))
SP["P5-A"] = teacher_board([("ກ ຂ ຄ ງ", 28, True), ("ຮຽນ", 22, True)], extra="".join([desk(250, 200, 110, 40), r(270, 186, 30, 14, "#e9a15b", 2), r(306, 190, 40, 6, "#5b7fa6", 2)]))
SP["P5-L"] = svg("".join([room("#efe4cf", "#c9ab84", 205), board(30, 24, 200, 100, [("ວິຊາ", 24, True), ("ຄະນິດ · ພາສາ", 18, True)]),
    desk(250, 170, 130, 40), r(262, 150, 36, 20, "#c25e4f", 2), r(304, 154, 30, 16, "#5b7fa6", 2), r(340, 140, 8, 30, "#f2b134", 2),
    W_(6, False, 150, 250, arms=[[(0, 0), (14, -24), (22, -52)]], scale=.85), W_(1, True, 220, 250, scale=.85)]))
SP["P5-F"] = svg("".join([sky("#d8ecf2", "#f5ead6", 200, "#9cbf7a"), stilt_house(150, 200, 1.0), palm(330, 200, 110), r(280, 170, 40, 30, "#5b7fa6", 4), c(300, 168, 0, INK),
    W_(0, True, 260, 246, arms=[[(0, 0), (18, 6), (28, -10)]], scale=.85)]))
SP["P5-D"] = svg("".join([room("#eef3f1", "#c3d0cc", 200), r(30, 30, 60, 60, "#ffffff", 6), r(54, 38, 12, 44, "#d9534f"), r(38, 54, 44, 12, "#d9534f"),
    r(250, 150, 120, 30, "#ffffff", 6, 'stroke="#c3d0cc" stroke-width="2"'), person(180, 236, "#ffffff", "#5b7fa6", HAIR, female=True, arms=[[(0, 0), (20, 14), (36, 12)]]),
    ln([(190, 150), (206, 168), (214, 190)], INK, 2), c(214, 192, 5, "#9aa7b1"), W_(3, False, 300, 236, arms=[[(0, 0), (-14, -18), (-6, -40)]]), bubble(296, 40, "ເຈັບຫົວ", 70, 16, tail="r")]))
SP["P5-G"] = svg("".join([room("#eef0f2", "#c9c0b2", 200), r(0, 20, W, 26, "#2f4f66"), t(200, 39, "ທະນາຄານ", 16, "#f3e2b3"),
    r(40, 60, 150, 76, "#d9e6ea", 3), W_(1, True, 110, 198, scale=.9), r(30, 140, 340, 60, "#8a6a4a", 4), r(234, 104, 60, 34, "#7cae3f", 3), t(264, 126, "₭", 18, "#ffffff", lao=False),
    r(300, 96, 28, 44, INK, 5), r(304, 102, 20, 28, "#9fd0e6", 2), W_(5, False, 330, 262, back=True)]))
SP["P5-H"] = svg("".join([sky("#bfe0ee", "#eaf4f2", 186, "#86b16a"), sun(320, 58, 30), cloud(60, 60), cloud(170, 40, .9, "#e3ebf0"),
    "".join(ln([(80 + i * 14, 86), (74 + i * 14, 104)], "#5b9ed6", 3) for i in range(5)), f'<path d="M0,186 Q100,150 200,170 T400,160 V186 Z" fill="#6e9a5a"/>',
    "".join(r(40 + i * 46, 220, 34, 18, col, 4) for i, col in enumerate(["#d9534f", "#f2b134", "#f6e04b", "#6cbf5a", "#4a8ad6", "#7a5ab8", "#ffffff", INK]))]))
SP["P5-I"] = svg("".join([sky("#f3c98b", "#f7e7c8", 200, "#c9ab84"), stupa(200, 200, 1.0), "".join(c(40 + i * 46, 30 + (i % 2) * 10, 6, ["#e0503a", "#f6c453", "#6cbf5a", "#4a8ad6"][i % 4]) for i in range(9)),
    W_(0, True, 70, 250, arms=[[(0, 0), (12, -20), (4, -40)]], scale=.85), W_(4, True, 330, 250, arms=[[(0, 0), (-12, -20), (-4, -40)]], scale=.85)]))
SP["P5-M"] = svg("".join([room("#eef0f2", "#c9c0b2", 200), r(40, 26, 120, 80, "#d9e6ea", 3, 'stroke="#9aa7b1" stroke-width="4"'), desk(150, 160, 200, 50),
    r(210, 120, 72, 40, "#3d4a55", 4), r(214, 124, 64, 30, "#9fd0e6", 2), r(196, 158, 100, 4, "#56646f"), r(300, 136, 18, 24, "#ffffff", 3, f'stroke="{INK}"'),
    W_(5, False, 110, 246, arms=[[(0, 0), (24, 8), (46, 8)]]), W_(3, True, 340, 246, arms=[[(0, 0), (-16, 10), (-30, 4)]], scale=.9)]))
# ===================== P6 글자
SP["P6-A"] = teacher_board([("ກ  ຈ  ດ  ຕ  ບ", 26, True), ("ຂ  ສ  ຖ  ຜ  ຫ", 26, True), ("ຄ  ງ  ຊ  ທ  ນ", 26, True)])
SP["P6-B"] = teacher_board([("ກະ  ກາ  ກິ  ກີ  ກຸ  ກູ", 24, True), ("ເກ  ແກ  ໂກ  ກໍ", 24, True)])
SP["P6-C"] = teacher_board([("ກັກ  ກັດ  ກັບ  ກັນ  ກັມ", 22, True), ("ກ່າ    ກ້າ", 30, True)])
SP["P6-D"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(card(28 + (i % 5) * 72, 30 + (i // 5) * 100, d, 62, 70, "#ffffff", 34, sub=str(i)) for i, d in enumerate("໐໑໒໓໔໕໖໗໘໙"))]), "#f6ecdc")
SP["P6-E"] = svg("".join([sky("#d8ecf2", "#f2ead6", 205, "#bfb19a"), r(30, 70, 160, 135, "#f3e8d6"), r(210, 50, 160, 155, "#e9dcc4"),
    r(36, 40, 148, 34, "#c25e4f", 4), t(110, 64, "ຮ້ານອາຫານ", 18, "#ffffff"), r(216, 20, 148, 34, "#2f6a8a", 4), t(290, 44, "ຮ້ານກາເຟ", 18, "#ffffff"),
    r(70, 120, 80, 85, TEAK, 3), r(250, 110, 80, 95, TEAK, 3), W_(1, True, 200, 252, arms=[[(0, 0), (14, -18), (28, -34)]], scale=.9)]))
# ===================== P7 문법
SP["P7-A"] = teacher_board([("ຂ້ອຍ + ກິນ + ເຂົ້າ", 22, True), ("나 + 먹다 + 밥", 18, False)], bw=260)
SP["P7-B"] = teacher_board([("ໄດ້ · ກຳລັງ · ຈະ", 24, True), ("ບໍ? · ແມ່ນບໍ?", 22, True)], bw=260)
SP["P7-C"] = teacher_board([("ໝາ ສອງ ໂຕ", 24, True), ("ແລະ · ແຕ່ · ເພາະວ່າ", 20, True)], bw=260)
SP["P7-D"] = svg(two_talk("ຊ່ວຍແດ່", "ໄດ້ເລີຍ", sky("#d8ecf2", "#f5ead6", 200, "#b9cf8f"), ia=4, ib=2, fa=False, fb=True, extra=palm(370, 200, 90)))
# ===================== P4 짝말
SP["P4-E"] = svg("".join([room("#f6ecdc", "#c9ab84", 205), W_(0, True, 90, 246, arms=[[(0, 0), (-10, 26), (0, 40)], [(0, 0), (10, 26), (0, 40)]]), person(200, 246, "#ffffff", "#6a3d7a", "#b8b8b8", female=True),
    W_(5, False, 310, 246, scale=.75), bubble(40, 40, "ຂ້ອຍ", 54, 17), bubble(170, 40, "ຂ້າພະເຈົ້າ", 96, 15), bubble(286, 80, "ເຮົາ", 50, 17, tail="r")]))
SP["P4-D"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), table(30, 196, 340), "".join(c(70 + i * 30, 184, 12, "#f2b134") for i in range(3)), t(100, 146, "ໜ່ວຍ", 20, TEAK),
    "".join(r(190 + i * 16, 150, 10, 46, "#5b7fa6", 3) for i in range(3)), t(214, 136, "ກ້ານ", 20, TEAK), "".join(r(282 + i * 24, 170, 20, 26, "#c25e4f", 4) for i in range(3)), t(316, 156, "ອັນ", 20, TEAK),
    t(200, 50, "ສາມ ___", 28, INK)]), "#f6ecdc")
SP["P4-B"] = svg("".join([sky("#cfe6ef", "#f2ead6", 196, "#9cbf7a"), sun(70, 60, 24), stilt_house(200, 196, .8), f'<path d="M290,120 h60 l-14,-14 M350,120 l-14,14" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>',
    f'<path d="M110,120 h-60 l14,-14 M50,120 l14,14" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>', t(80, 160, "ຊ້າຍ", 20, TEAK), t(320, 160, "ຂວາ", 20, TEAK),
    t(200, 28, "ເທິງ", 18, TEAK), t(200, 250, "ລຸ່ມ", 18, TEAK)]))
SP["P4-C"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), r(40, 40, 140, 180, "#ffffff", 10, f'stroke="{INK}" stroke-width="1.5"'), r(220, 40, 140, 180, "#ffffff", 10, f'stroke="{INK}" stroke-width="1.5"'),
    c(110, 120, 46, "#e0503a"), c(290, 130, 20, "#e0503a"), t(110, 204, "ໃຫຍ່", 22, TEAK), t(290, 204, "ນ້ອຍ", 22, TEAK)]), "#f6ecdc")
SP["P4-A"] = svg("".join([room("#f3e8d6", "#c9ab84", 205), W_(0, True, 110, 246, arms=[[(0, 0), (30, 14), (60, 10)]]), W_(5, False, 290, 246, arms=[[(0, 0), (-30, 14), (-60, 10)]]),
    r(180, 100, 40, 32, "#c25e4f", 4), ln([(200, 100), (200, 132)], "#f6c453", 4), ln([(180, 116), (220, 116)], "#f6c453", 4), bubble(40, 26, "ໃຫ້", 50, 18), bubble(280, 40, "ຮັບ", 50, 18, tail="r")]))
SP["P4-F"] = svg("".join([room("#f6e6cc", "#b98d5e", 200), table(80, 176, 240), basket(150, 176), bowl(200, 176), bowl(250, 176, food="#6e9a64"),
    person(90, 246, "#ffffff", "#6a3d7a", "#b8b8b8", female=True, scale=.9), W_(5, False, 320, 246, arms=[[(0, 0), (-10, -16), (-2, -34)], [(0, 0), (10, -16), (2, -34)]], scale=.9),
    bubble(30, 34, "ກິນ", 50, 18), bubble(250, 40, "ຮັບປະທານ", 88, 15, tail="r")]))
# ===================== P3 닮은말 (people and small scenes)
def duo(a, b, bg_top="#e3eef0", bg_bot="#f6ecdc", ground="#c9ab84", ia=0, ib=1, fa=True, fb=False, extra=""):
    return svg(two_talk(a, b, sky(bg_top, bg_bot, 205, ground), ia, ib, fa, fb, extra=extra))
SP["P3-H"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(c(60 + i * 36, 120, 14, "#f2b134") for i in range(4)), t(110, 170, "ທັງໝົດ", 20, TEAK),
    "".join(r(240 + i * 40, 100, 28, 40, "#5b7fa6", 6) for i in range(3)), t(300, 170, "ແຕ່ລະ", 20, TEAK), t(200, 230, "ຈັກ? · ໃຜ? · ຫຍັງ?", 20, INK), t(200, 50, "?", 40, "#c25e4f")]), "#f6ecdc")
SP["P3-B"] = svg("".join([room(), W_(0, True, 110, 246, arms=[[(0, 0), (30, 14), (60, 10)]]), W_(5, False, 290, 246, arms=[[(0, 0), (-30, 14), (-60, 10)]]),
    r(176, 104, 48, 28, "#fff4dc", 4, f'stroke="{INK}"'), t(200, 124, "₭", 16, TEAK, lao=False), bubble(150, 30, "ເອົາ · ໄດ້ · ເປັນ", 120, 15)]))
SP["P3-C"] = svg("".join([sky("#e3eef0", "#f6ecdc", 205, "#c9ab84"), W_(2, True, 120, 246, arms=[[(0, 0), (14, -20), (6, -40)]]), c(250, 80, 50, "#ffffff", f'stroke="{INK}" stroke-width="1.5"'),
    c(196, 140, 8, "#ffffff", f'stroke="{INK}"'), c(184, 158, 5, "#ffffff", f'stroke="{INK}"'), t(250, 76, "ຢາກ", 22, TEAK), t(250, 104, "ຕ້ອງ · ຄວນ", 16, INK)]))
SP["P3-A"] = svg("".join([room("#f3e8d6"), W_(0, True, 110, 246, arms=[[(0, 0), (16, 20), (30, 28)]]), waves(140, 110), W_(5, False, 290, 246, arms=[[(0, 0), (-18, -30), (-16, -64)]]),
    bubble(30, 30, "ເວົ້າ", 56, 18), bubble(250, 40, "ຟັງ · ເບິ່ງ", 90, 16, tail="r")]))
SP["P3-G"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), ln([(40, 140), (360, 140)], TEAK, 5), "".join(c(80 + i * 120, 140, 14, ["#e0503a", "#f2b134", "#6cbf5a"][i]) for i in range(3)),
    t(80, 186, "ກ່ອນ", 20, TEAK), t(200, 186, "ແລ້ວ", 20, TEAK), t(320, 186, "ຫຼັງ", 20, TEAK), t(200, 80, "ທຸກມື້ · ບາງເທື່ອ", 20, INK)]), "#f6ecdc")
SP["P3-I"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), card(40, 90, "ເຂົ້າ", 90, 60, "#ffffff", 22), card(270, 90, "ນ້ຳ", 90, 60, "#ffffff", 22),
    r(150, 98, 100, 44, "#f2b134", 22), t(200, 128, "ແລະ", 22, "#ffffff"), t(200, 210, "ຫຼື · ແຕ່ · ຂອງ", 20, TEAK)]), "#f6ecdc")
SP["P3-E"] = svg("".join([sky("#f3d9a8", "#f7ecd8", 205, "#c9ab84"), sun(320, 50, 26), W_(0, True, 140, 246, arms=[[(0, 0), (14, -24), (20, -50)], [(0, 0), (-14, -24), (-20, -50)]]),
    W_(5, False, 260, 246, arms=[[(0, 0), (14, -24), (20, -50)], [(0, 0), (-14, -24), (-20, -50)]]), bubble(150, 26, "ດີໃຈ!", 60, 18)]))
SP["P3-D"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(r(50 + i * 80, 200 - (i + 1) * 36, 50, (i + 1) * 36, ["#f6d58a", "#f2b134", "#d9822b", "#b5442e"][i], 4) for i in range(4)),
    t(75, 224, "ໜ້ອຍ", 16, TEAK), t(315, 224, "ຫຼາຍ", 16, TEAK), t(200, 40, "ຫຼາຍ · ໂພດ · ແທ້", 20, INK), ln([(40, 206), (360, 206)], INK, 2)]), "#f6ecdc")
SP["P3-K"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), r(60, 70, 90, 130, "#e8f1f6", 8, 'stroke="#9fb3c1" stroke-width="3"'), r(64, 90, 82, 106, "#5b9ed6", 6), t(105, 230, "ເຕັມ", 20, TEAK),
    r(250, 70, 90, 130, "#e8f1f6", 8, 'stroke="#9fb3c1" stroke-width="3"'), r(254, 186, 82, 10, "#5b9ed6", 4), t(295, 230, "ໝົດ", 20, TEAK)]), "#f6ecdc")
SP["P3-J"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), "".join(c(110 + dx, 110, 34, "#f2b134") for dx in (0,)), c(290, 110, 34, "#f2b134"), t(200, 118, "=", 40, TEAK, lao=False),
    t(110, 190, "ຄືກັນ", 20, TEAK), t(290, 190, "ຄື", 20, TEAK), t(200, 240, "ກວ່າ · ທີ່ສຸດ", 20, INK)]), "#f6ecdc")
SP["P3-O"] = duo("ໝູ່", "ແຟນ", ia=0, ib=6, extra=palm(360, 205, 90))
SP["P3-L"] = svg("".join([room(), r(240, 50, 100, 155, TEAK, 4), r(250, 60, 80, 140, "#a5825c", 3), c(262, 130, 5, GOLD), W_(5, False, 180, 246, arms=[[(0, 0), (40, -4), (74, -6)]]), bubble(40, 40, "ເປີດ · ປິດ", 90, 16)]))
SP["P3-M"] = svg("".join([room("#efe4cf"), desk(120, 180, 200, 30), r(160, 160, 70, 20, "#fffaf0", 2, f'stroke="{INK}"'), ln([(196, 160), (196, 180)], INK, 1.5),
    W_(1, True, 200, 250, arms=[[(0, 0), (14, 26), (20, 34)]], scale=.9), c(270, 70, 34, "#ffffff", f'stroke="{INK}"'), t(270, 76, "ຄິດ", 22, TEAK), c(236, 116, 6, "#ffffff", f'stroke="{INK}"')]))
SP["P3-F"] = svg("".join([sky("#e3eef0", "#f6ecdc", 205, "#c9ab84"), W_(0, True, 90, 246), W_(5, False, 200, 246, scale=1.1), W_(3, True, 310, 246, scale=.8),
    t(90, 40, "ງາມ", 20, TEAK), t(200, 30, "ສູງ", 20, TEAK), t(310, 60, "ສະຫຼາດ", 18, TEAK)]))
# ===================== P2 말뿌리 (root word on a card + a picture)
def root(word, meaning, pic):
    return svg("".join([r(0, 0, W, H, "#f6ecdc"), r(20, 20, 150, 220, "#ffffff", 14, f'stroke="{GOLD}" stroke-width="3"'), t(95, 120, word, 40, TEAK), t(95, 164, meaning, 16, "#7a6a5a", lao=False, w="600"),
                        r(190, 20, 190, 220, "#fffaf0", 14, 'stroke="#e1d3bb" stroke-width="2"'), pic]), "#f6ecdc")
SP["P2-K"] = root("ເຮັດ", "하다·만들다", W_(5, False, 285, 220, arms=[[(0, 0), (24, 10), (40, 2)], [(0, 0), (-24, 10), (-40, 2)]], scale=.9) + r(250, 196, 70, 10, TEAK, 2))
SP["P2-G"] = root("ລົດ", "차", tuk(240, 170))
SP["P2-D"] = root("ນ້ຳ", "물", r(255, 70, 60, 110, "#e8f1f6", 10, 'stroke="#9fb3c1" stroke-width="3"') + r(259, 110, 52, 66, "#5b9ed6", 8) + basket(330, 200, .8))
SP["P2-H"] = root("ວັນ", "날", sun(285, 100, 34) + "".join(r(214 + i * 24, 170, 20, 20, "#f3e2c3" if i != 3 else "#e0503a", 3) for i in range(7)))
SP["P2-B"] = root("ນັກ", "~하는 사람", W_(1, True, 250, 220, scale=.85) + W_(5, False, 320, 220, scale=.85))
SP["P2-F"] = root("ໂຮງ", "건물", r(220, 70, 130, 130, "#e9dcc4", 3) + f'<path d="M210,74 L285,36 L360,74 Z" fill="#b5442e"/>' + "".join(r(236 + (i % 3) * 40, 90 + (i // 3) * 40, 22, 22, "#9fd0e6", 2) for i in range(6)) + r(270, 170, 30, 30, TEAK))
SP["P2-E"] = root("ເຄື່ອງ", "물건·기계", r(222, 90, 120, 80, "#3d4a55", 6) + r(230, 98, 104, 60, "#9fd0e6", 3) + r(266, 170, 32, 14, "#56646f") + r(250, 184, 64, 6, "#56646f", 3))
SP["P2-L"] = root("ສຸດ", "가장·끝", "".join(r(220 + i * 36, 200 - (i + 1) * 30, 28, (i + 1) * 30, "#f2b134" if i < 3 else "#b5442e", 4) for i in range(4)) + t(328, 64, "★", 22, GOLD, lao=False))
SP["P2-J"] = root("ຮຽນ", "배우다", r(225, 80, 120, 90, "#fffaf0", 4, f'stroke="{INK}" stroke-width="2"') + ln([(285, 80), (285, 170)], INK, 2) + "".join(r(236, 96 + i * 16, 40, 4, "#c9b79c") for i in range(4)) + "".join(r(296, 96 + i * 16, 40, 4, "#c9b79c") for i in range(4)))
SP["P2-C"] = root("ຕາ", "눈", f'<ellipse cx="285" cy="120" rx="60" ry="32" fill="#ffffff" stroke="{INK}" stroke-width="3"/>' + c(285, 120, 22, "#6a4a2e") + c(285, 120, 10, INK) + c(293, 112, 4, "#ffffff"))
SP["P2-A"] = root("ໃຈ", "마음", '<path d="M285,190 C200,130 230,60 285,100 C340,60 370,130 285,190 Z" fill="#e0503a"/>')
SP["P2-I"] = root("ສີ", "색", "".join(c(245 + (i % 3) * 40, 90 + (i // 3) * 50, 17, col) for i, col in enumerate(["#e0503a", "#f2b134", "#6cbf5a", "#4a8ad6", "#7a5ab8", INK])))
SP["P2-M"] = root("ເພງ", "노래", f'<path d="M260,170 V80 L330,66 V150" stroke="{INK}" stroke-width="6" fill="none"/>' + c(250, 172, 14, INK) + c(320, 152, 14, INK) + r(220, 196, 130, 10, GOLD, 3))
SP["P2-N"] = root("ຄວາມ", "~함", card(205, 80, "ຄວາມ", 76, 50, "#f6d58a", 18) + t(290, 112, "+", 26, TEAK, lao=False) + card(300, 80, "ຮັກ", 66, 50, "#ffffff", 20) + t(285, 180, "ຄວາມຮັກ", 26, TEAK))
# ===================== P1 말소리 (speaker + syllable cards + tone lines)
def sounds(cards, curves=None, bg="#f6ecdc"):
    out = [r(0, 0, W, H, bg), W_(2, True, 64, 250, arms=[[(0, 0), (14, 18), (26, 22)]]), waves(100, 110)]
    for i, (s, sub) in enumerate(cards):
        x = 140 + (i % 3) * 84; y = 30 + (i // 3) * 110
        out.append(card(x, y, s, 74, 64, "#ffffff", 28, sub=sub))
        if curves: out.append(tone_curve(x + 8, y + 88, 58, curves[i % len(curves)], ["#e0503a", "#f2b134", "#4a8ad6", "#6cbf5a", "#7a5ab8", TEAK][i % 6]))
    return svg("".join(out), bg)
SP["P1-A"] = sounds([("ມາ", "마"), ("ມ່າ", "마"), ("ມ້າ", "마")], ["mid", "low", "fall"])
SP["P1-B"] = sounds([("ເສືອ", "쓰아"), ("ເສື່ອ", "쓰아"), ("ເສື້ອ", "쓰아")], ["rise", "low", "fall"])
SP["P1-C"] = sounds([("ສື", "쓰"), ("ສື່", "쓰"), ("ສື້", "쓰"), ("ປີ", "삐"), ("ປີ່", "삐"), ("ປີ້", "삐")], ["rise", "low", "hf"])
SP["P1-D"] = sounds([("ຂາ", "카"), ("ຄາ", "카"), ("ຫ້າ", "하"), ("ຮ້າ", "하")], ["rise", "mid", "low", "hf"])
SP["P1-E"] = sounds([("ກັນ", "깐"), ("ການ", "까~안"), ("ມັກ", "막"), ("ມາກ", "마~악")], None)
SP["P1-F"] = sounds([("ກ", "ㄲ"), ("ຂ", "ㅋ"), ("ຄ", "ㅋ")])
SP["P1-G"] = sounds([("ບ", "ㅂ"), ("ປ", "ㅃ"), ("ດ", "ㄷ"), ("ຕ", "ㄸ"), ("ພ", "ㅍ"), ("ຟ", "f")])
SP["P1-H"] = sounds([("ເກ", "께"), ("ແກ", "깨"), ("ໂກ", "꼬"), ("ກໍ", "꺼")])
SP["P1-I"] = sounds([("ງ", "응"), ("ຍ", "냐"), ("ຢ", "야")])
SP["P1-K"] = sounds([("ກ", "ㄲ"), ("ຄ", "ㅋ"), ("ຈ", "ㅉ"), ("ສ", "ㅆ")])
SP["P1-L"] = sounds([("ຕ", "ㄸ"), ("ທ", "ㅌ"), ("ດ", "ㄷ"), ("ປ", "ㅃ"), ("ພ", "ㅍ"), ("ບ", "ㅂ")])
SP["P1-M"] = sounds([("ມ", "ㅁ"), ("ນ", "ㄴ"), ("ລ", "ㄹ"), ("ຫ", "ㅎ"), ("ອ", "ㅇ")])
SP["P1-Z"] = sounds([("ກ່າ", "◌່"), ("ກ້າ", "◌້"), ("ກ໊າ", "◌໊"), ("ກ໋າ", "◌໋")], ["low", "fall", "high", "rise"])
# ===================== P9 듣기연습
def headphones(x, y): return f'<path d="M{x-26},{y} a26,26 0 0 1 52,0" stroke="{INK}" stroke-width="5" fill="none"/>' + r(x - 32, y - 4, 12, 22, "#c25e4f", 5) + r(x + 20, y - 4, 12, 22, "#c25e4f", 5)
SP["P9-A"] = svg("".join([sky("#f3d9a8", "#f7ecd8", 205, "#9cbf7a"), W_(0, True, 120, 246, arms=[[(0, 0), (14, -24), (20, -50)]], scale=.8), W_(6, False, 200, 246, scale=.8), W_(3, True, 280, 246, arms=[[(0, 0), (-14, -24), (-20, -50)]], scale=.8),
    t(110, 60, "♪", 30, TEAK, lao=False), t(200, 40, "໑ ໒ ໓", 22, TEAK), t(296, 66, "♫", 30, TEAK, lao=False)]))
cat = lambda x, y: "".join([f'<ellipse cx="{x}" cy="{y}" rx="34" ry="20" fill="#e9a15b"/>', c(x + 30, y - 18, 16, "#e9a15b"), f'<path d="M{x+18},{y-30} l4,-14 l8,10 z M{x+34},{y-32} l6,-12 l6,12 z" fill="#e9a15b"/>',
    c(x + 26, y - 20, 2, INK), c(x + 36, y - 20, 2, INK), f'<path d="M{x-34},{y-4} q-20,-10 -14,-30" stroke="#e9a15b" stroke-width="7" fill="none" stroke-linecap="round"/>'])
SP["P9-B"] = svg("".join([r(0, 0, W, H, "#f6ecdc"), r(40, 30, 320, 200, "#fffaf0", 10, f'stroke="{TEAK}" stroke-width="4"'), ln([(200, 30), (200, 230)], TEAK, 3), cat(120, 160), sun(300, 80, 22), t(290, 170, "ແມວນ້ອຍ", 20, TEAK)]), "#f6ecdc")
SP["P9-C"] = svg("".join([sky("#2f3a5a", "#6a5a7a", 205, "#4a3a2a"), c(320, 50, 22, "#f6e6b0"), "".join(c(40 + i * 50, 30 + (i % 3) * 12, 2, "#ffffff") for i in range(7)), stilt_house(110, 205, .7),
    f'<path d="M230,205 l20,-30 l20,30 z" fill="#e0703a"/>', W_(0, True, 300, 246, scale=.8), person(350, 246, "#ffffff", "#3b4a5a", "#b8b8b8", scale=.9)]))
SP["P9-D"] = duo("ສະບາຍດີ", "ຍິນດີທີ່ຮູ້ຈັກ", ia=1, ib=4, size=15) if False else svg(two_talk("ສະບາຍດີ", "ຍິນດີຮູ້ຈັກ", sky("#d8ecf2", "#f7ecd8", 205, "#b9cf8f"), 1, 4, True, False, size=15))
SP["P9-E"] = teacher_board([("ເປີດປຶ້ມ", 26, True), ("ຟັງ · ຂຽນ · ອ່ານ", 20, True)], extra=headphones(330, 190))
SP["P9-F"] = svg("".join([room("#eef0f2", "#c9c0b2", 200), r(30, 30, 210, 70, "#24323f", 6), t(135, 60, "ຖ້ຽວບິນ QV 312", 15, "#f6c453"), t(135, 86, "→ 08:30", 15, "#9fd0e6", lao=False),
    f'<path d="M300,40 l60,20 l-60,20 l10,-20 z" fill="#c25e4f"/>', c(330, 130, 24, "#3d4a55"), waves(356, 130, "#3d4a55"), W_(5, False, 120, 250, back=True), r(150, 210, 36, 40, "#5b7fa6", 5)]))
SP["P9-G"] = svg("".join([room("#f3e8d6"), r(110, 90, 180, 100, "#a5825c", 12), c(160, 140, 30, "#3d4a55"), c(160, 140, 18, "#56646f"), r(210, 110, 64, 24, "#f3e2c3", 4), c(226, 160, 9, INK), c(256, 160, 9, INK),
    ln([(140, 90), (110, 40)], INK, 3), waves(300, 140, TEAK), sun(60, 50, 20), cloud(320, 50, .8)]))
SP["P9-H"] = svg("".join([room("#e9eef2", "#c3ccd3", 200), r(40, 30, 320, 150, "#24323f", 8), r(52, 42, 296, 126, "#3b5a8a", 4), W_(3, True, 140, 168, scale=.8), r(200, 70, 130, 70, "#f3e8d6", 3),
    stupa(265, 136, .4), r(52, 140, 296, 28, "#c25e4f"), t(200, 160, "ຂ່າວ", 18, "#ffffff")]))
SP["P9-I"] = svg("".join([sky("#f3c98b", "#f7e7c8", 205, "#c9ab84"), f'<path d="M110,150 h120 l-10,90 h-100 z" fill="#f6e6cc" stroke="{TEAK}" stroke-width="2"/>', r(150, 110, 8, 40, "#f6c453"), r(180, 110, 8, 40, "#f6c453"),
    c(154, 104, 5, "#e0503a"), c(184, 104, 5, "#e0503a"), t(300, 80, "♪ ♫", 30, TEAK, lao=False), W_(0, True, 330, 246, arms=[[(0, 0), (-14, -24), (-20, -50)]], scale=.85)]))

if __name__ == "__main__":
    import sys
    json.dump(SP, open(sys.argv[1], "w"), ensure_ascii=False)
    print(len(SP), sum(len(v) for v in SP.values()))
