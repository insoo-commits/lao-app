# TOEIC Part 1 pictures (RYU 2026-11-23: "사진묘사 문제는 그림이나 사진으로 보여줘").
# Flat SVG drawings, one per Part 1 question, keyed by the question's Korean description.
W, H = 400, 260
SKIN, SKIN2 = "#f1c7a3", "#e0b08a"
INK = "#33414e"

HEADS = []   # head circles drawn since the last svg(): speech bubbles move off them (RYU 2026-11-24)
def svg(body, bg="#eef3f6"):
    HEADS.clear()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" class="pic">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')

def r(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'

def c(x, y, rad, fill, extra=""):
    return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" {extra}/>'

def ln(pts, color, w=9):
    p = " ".join(f"{a},{b}" for a, b in pts)
    return f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def person(x, foot, shirt, pants, hair, female=False, arms=(), lean=0, cap=None, scale=1.0, back=False):
    """x = body centre, foot = floor y. arms: list of point lists starting at the shoulder (relative to the shoulder)."""
    s = scale
    hip = foot - 62 * s; sh = hip - 52 * s; hx = x + lean
    out = []
    # legs
    if female:
        out.append(f'<path d="M{x-17*s},{hip} L{x+17*s},{hip} L{x+21*s},{hip+34*s} L{x-21*s},{hip+34*s} Z" fill="{pants}"/>')
        out.append(ln([(x - 8 * s, hip + 30 * s), (x - 8 * s, foot - 3)], SKIN2, 8 * s))
        out.append(ln([(x + 8 * s, hip + 30 * s), (x + 8 * s, foot - 3)], SKIN2, 8 * s))
    else:
        out.append(ln([(x - 8 * s, hip), (x - 9 * s, foot - 4)], pants, 13 * s))
        out.append(ln([(x + 8 * s, hip), (x + 9 * s, foot - 4)], pants, 13 * s))
    out.append(r(x - 17 * s, foot - 6 * s, 15 * s, 7 * s, INK, 3)); out.append(r(x + 2 * s, foot - 6 * s, 15 * s, 7 * s, INK, 3))
    # body
    out.append(f'<path d="M{hx-19*s},{sh} Q{hx},{sh-6*s} {hx+19*s},{sh} L{x+18*s},{hip+4*s} L{x-18*s},{hip+4*s} Z" fill="{shirt}"/>')
    # arms (behind the head, in front of the body)
    # RYU 2026-11-24: never one-armed or armless: a side without a posed arm gets a relaxed arm hanging down
    if True:   # also people seen from behind
        arms = list(arms); sides = {(-1 if sum(q[0] for q in a) < 0 else 1) for a in arms}
        for sd in (-1, 1):
            if sd not in sides and len(arms) < 2: arms.append([(sd * 6, 0), (sd * 10, 40)])
    # arms a shade darker than the shirt, so an arm in front of the body still shows (RYU 2026-11-24)
    def _dk(h, k=0.8):
        h = h.lstrip("#")
        if len(h) != 6: return h
        return "#" + "".join(f"{int(int(h[i:i+2], 16) * k):02x}" for i in (0, 2, 4))
    arm_col = _dk(shirt) if str(shirt).startswith("#") else shirt
    for a in arms:
        side = -1 if sum(q[0] for q in a) < 0 else 1
        pts = [(hx + side * 15 * s + px * s, sh + 6 * s + py * s) for px, py in a]
        out.append(ln(pts, arm_col, 10 * s)); out.append(c(pts[-1][0], pts[-1][1], 5.5 * s, SKIN))
    # head
    hy = sh - 20 * s
    HEADS.append((hx, hy, 18 * s))
    out.append(ln([(hx, sh), (hx, sh - 8 * s)], SKIN, 9 * s))
    out.append(c(hx, hy, 15 * s, SKIN))
    if back:
        out.append(c(hx, hy - 2 * s, 15.5 * s, hair))
    elif female:
        out.append(f'<path d="M{hx-16*s},{hy+14*s} Q{hx-19*s},{hy-18*s} {hx},{hy-17*s} Q{hx+19*s},{hy-18*s} {hx+16*s},{hy+14*s} L{hx+11*s},{hy+14*s} Q{hx+13*s},{hy-6*s} {hx},{hy-9*s} Q{hx-13*s},{hy-6*s} {hx-11*s},{hy+14*s} Z" fill="{hair}"/>')
    else:
        out.append(f'<path d="M{hx-15*s},{hy-1*s} Q{hx-15*s},{hy-17*s} {hx},{hy-16*s} Q{hx+15*s},{hy-17*s} {hx+15*s},{hy-1*s} Q{hx+6*s},{hy-9*s} {hx-15*s},{hy-1*s} Z" fill="{hair}"/>')
    if cap:
        out.append(r(hx - 12 * s, hy - 22 * s, 24 * s, 10 * s, cap, 3)); out.append(r(hx - 14 * s, hy - 13 * s, 28 * s, 3 * s, INK))
    if not back:
        out.append(c(hx - 5 * s, hy + 1 * s, 1.6 * s, INK)); out.append(c(hx + 5 * s, hy + 1 * s, 1.6 * s, INK))
        out.append(f'<path d="M{hx-4*s},{hy+7*s} Q{hx},{hy+10*s} {hx+4*s},{hy+7*s}" stroke="{INK}" stroke-width="{1.4*s}" fill="none"/>')
    return "".join(out)

def suitcase(x, y, w, h, color, handle=True):
    out = [r(x, y, w, h, color, 5), r(x + 4, y + 4, w - 8, 3, "#00000022", 1)]
    if handle: out.append(f'<path d="M{x+w*0.35},{y} v-7 h{w*0.3} v7" stroke="{INK}" stroke-width="3" fill="none"/>')
    out.append(r(x + w * 0.5 - 1, y + 3, 2, h - 6, "#00000022"))
    return "".join(out)

def cart(x, foot, w=120):
    """brass luggage cart: base, two posts, top bar"""
    base = foot - 16
    return "".join([r(x, base - 6, w, 8, "#b8913a", 3), c(x + 14, foot - 7, 7, INK), c(x + w - 14, foot - 7, 7, INK),
                    r(x + 4, base - 120, 6, 116, "#c9a34a", 3), r(x + w - 10, base - 120, 6, 116, "#c9a34a", 3),
                    f'<path d="M{x+7},{base-118} Q{x+w/2},{base-150} {x+w-7},{base-118}" stroke="#c9a34a" stroke-width="6" fill="none"/>'])

def floor(y, col="#d9cbb6"):
    return r(0, y, W, H - y, col)

PICS = {}

# 1 엘리베이터 옆 안내 표지판 (no people)
PICS["사진: 엘리베이터 옆에 안내 표지판이 서 있다."] = svg("".join([
    r(0, 0, W, 200, "#e7e1d6"), floor(200), r(0, 196, W, 5, "#c9b79c"),
    r(150, 30, 130, 170, "#9aa7b1"), r(158, 38, 114, 162, "#c3ccd3"), r(214, 38, 2, 162, "#8e9aa4"),
    r(190, 12, 50, 14, INK, 3), f'<text x="215" y="23" font-size="11" fill="#ffd36b" text-anchor="middle" font-family="sans-serif">▲ 5</text>',
    r(290, 100, 16, 30, "#8e9aa4", 3), c(298, 109, 4, "#f5f5f5"), c(298, 121, 4, "#f5f5f5"),
    # easel sign
    ln([(70, 198), (86, 112)], "#7a5a3a", 6), ln([(122, 198), (106, 112)], "#7a5a3a", 6), ln([(96, 198), (96, 150)], "#7a5a3a", 5),
    r(56, 70, 80, 82, "#fdfaf3", 4, 'stroke="#7a5a3a" stroke-width="4"'),
    r(68, 84, 56, 8, "#2f6f8f", 2), r(68, 100, 48, 5, "#9aa7b1", 2), r(68, 110, 52, 5, "#9aa7b1", 2), r(68, 120, 40, 5, "#9aa7b1", 2),
    f'<path d="M78,136 l10,0 l0,-5 l9,8 l-9,8 l0,-5 l-10,0 Z" fill="#2f6f8f"/>',
    r(330, 150, 34, 50, "#7d9b76", 6), c(347, 140, 22, "#6e9a64"), c(334, 130, 14, "#7fae72"), c(360, 128, 14, "#7fae72"),
]))

# 2 호텔 현관에서 직원이 짐 카트를 밀고 있다
PICS["사진: 호텔 현관에서 직원이 짐 카트를 밀고 있다."] = svg("".join([
    r(0, 0, W, 205, "#e9e4da"), floor(205, "#cfc6b8"),
    r(30, 18, 230, 20, "#2f4f66", 3), f'<text x="145" y="33" font-size="13" fill="#f3e2b3" text-anchor="middle" font-family="serif" letter-spacing="4">HOTEL</text>',
    r(45, 38, 200, 167, "#7a8a96"), r(52, 45, 90, 160, "#b9d3e0"), r(148, 45, 90, 160, "#b9d3e0"),
    ln([(70, 60), (110, 140)], "#ffffff88", 4), ln([(166, 60), (206, 140)], "#ffffff88", 4),
    r(132, 110, 4, 30, "#c9a34a", 2), r(154, 110, 4, 30, "#c9a34a", 2),
    cart(250, 232, 110),
    suitcase(262, 160, 40, 56, "#5b7fa6"), suitcase(306, 172, 44, 44, "#a65b5b"), suitcase(268, 128, 70, 30, "#6d8c5e"),
    person(215, 232, "#2f4f66", "#24323f", "#3a2a22", arms=[[(0, 0), (8, 18), (18, 28)], [(0, 0), (10, 14), (20, 22)]], lean=6, cap="#2f4f66"),
]))

# 3 뷔페 테이블 위 과일 접시들 (no people)
def fruit_plate(x, y, k):
    cols = [["#e85d4a", "#f2a93b", "#7cbf5a"], ["#f2d03b", "#e85d4a", "#9b5bb5"], ["#7cbf5a", "#f2a93b", "#e85d4a"]][k % 3]
    return "".join([f'<ellipse cx="{x}" cy="{y}" rx="34" ry="11" fill="#ffffff" stroke="#c9ced2" stroke-width="2"/>',
                    c(x - 12, y - 6, 8, cols[0]), c(x + 2, y - 8, 8, cols[1]), c(x + 15, y - 5, 7, cols[2]), c(x - 3, y - 2, 6, cols[2])])
PICS["사진: 뷔페 테이블 위에 과일 접시들이 줄지어 놓여 있다."] = svg("".join([
    r(0, 0, W, 170, "#efe6d8"), floor(170, "#d8c7ae"),
    r(40, 40, 70, 60, "#d9e6ea", 4, 'stroke="#b8a888" stroke-width="5"'), r(290, 40, 70, 60, "#d9e6ea", 4, 'stroke="#b8a888" stroke-width="5"'),
    r(20, 140, 360, 22, "#ffffff"), f'<path d="M20,162 h360 v62 h-360 Z" fill="#f4f1ea"/>', r(20, 160, 360, 6, "#d4cbbb"),
    r(30, 224, 10, 18, "#8a7a62"), r(360, 224, 10, 18, "#8a7a62"),
    fruit_plate(70, 146, 0), fruit_plate(155, 146, 1), fruit_plate(240, 146, 2), fruit_plate(325, 146, 0),
    r(150, 112, 100, 14, "#ffffff", 3, 'stroke="#c9ced2" stroke-width="2"'), f'<text x="200" y="123" font-size="10" fill="#6b5a40" text-anchor="middle" font-family="sans-serif">FRESH FRUIT</text>',
]))

# 4 프런트 데스크에서 여자 직원이 손님에게 카드키를 건넨다
PICS["사진: 여자가 프런트 데스크에서 카드키를 건네고 있다."] = svg("".join([
    r(0, 0, W, 210, "#e6ded2"), floor(210, "#cdbfa9"),
    r(70, 20, 260, 26, "#2f4f66", 3), f'<text x="200" y="38" font-size="13" fill="#f3e2b3" text-anchor="middle" font-family="sans-serif" letter-spacing="3">RECEPTION</text>',
    r(30, 70, 50, 60, "#d9e6ea", 3, 'stroke="#b8a888" stroke-width="4"'),
    person(150, 210, "#2f4f66", "#24323f", "#2b1d16", female=True, arms=[[(0, 0), (8, 30), (6, 44)], [(0, 0), (40, 18), (72, 14)]]),
    r(40, 140, 320, 100, "#8a6a4a", 4), r(34, 132, 332, 12, "#a5825c", 3), r(60, 160, 280, 4, "#7a5a3a"),
    r(110, 118, 50, 14, "#3d4a55", 2), r(116, 98, 38, 22, "#56646f", 2),
    person(300, 262, "#b55d4c", "#3b4a5a", "#4a3426", arms=[[(0, 0), (-30, 16), (-50, 10)]], back=True),
    r(226, 104, 22, 14, "#ffffff", 2, f'stroke="{INK}" stroke-width="1.5"'), r(229, 107, 10, 3, "#2f6f8f"),
]))

# 5 빈 레스토랑, 테이블이 차려져 있다 (no people)
def set_table(x, y):
    return "".join([f'<ellipse cx="{x}" cy="{y}" rx="58" ry="14" fill="#ffffff" stroke="#d3cfc6" stroke-width="2"/>',
                    f'<path d="M{x-58},{y} v34 h116 v-34" fill="#f6f3ec"/>', r(x - 4, y + 34, 8, 30, "#6b5a40"),
                    f'<ellipse cx="{x-24}" cy="{y-1}" rx="13" ry="4.5" fill="#fbfbfb" stroke="#b9bec2" stroke-width="1.5"/>',
                    f'<ellipse cx="{x+22}" cy="{y-1}" rx="13" ry="4.5" fill="#fbfbfb" stroke="#b9bec2" stroke-width="1.5"/>',
                    f'<path d="M{x-6},{y-22} q4,10 8,0 Z M{x-2},{y-13} v10" stroke="#9fb3c1" stroke-width="1.8" fill="#e8f1f6"/>',
                    f'<path d="M{x+6},{y-22} q4,10 8,0 Z M{x+10},{y-13} v10" stroke="#9fb3c1" stroke-width="1.8" fill="#e8f1f6"/>',
                    r(x - 42, y - 4, 2, 9, "#9a9a9a"), r(x + 39, y - 4, 2, 9, "#9a9a9a")])
def chair(x, y, flip=False):
    d = -1 if flip else 1
    return "".join([r(x - 14, y, 28, 6, "#8a5a3a", 2), ln([(x - d * 12, y), (x - d * 14, y - 40)], "#8a5a3a", 5),
                    ln([(x - 11, y + 6), (x - 12, y + 34)], "#8a5a3a", 4), ln([(x + 11, y + 6), (x + 12, y + 34)], "#8a5a3a", 4)])
PICS["사진: 빈 레스토랑에 테이블마다 접시와 잔이 놓여 있다."] = svg("".join([
    r(0, 0, W, 175, "#efe4d2"), floor(175, "#b89a76"),
    r(150, 26, 100, 70, "#d4e3ea", 4, 'stroke="#8a6a4a" stroke-width="5"'), r(198, 26, 4, 70, "#8a6a4a"),
    c(80, 30, 10, "#ffe7a8"), ln([(80, 0), (80, 20)], INK, 2), c(320, 30, 10, "#ffe7a8"), ln([(320, 0), (320, 20)], INK, 2),
    chair(40, 190), chair(170, 190, True), set_table(105, 170),
    chair(240, 190), chair(370, 190, True), set_table(305, 170),
]))

# 6 남자가 객실 창문 커튼을 열고 있다
PICS["사진: 남자가 객실 창문의 커튼을 열고 있다."] = svg("".join([
    r(0, 0, W, 210, "#e9e2d6"), floor(210, "#b9a58c"),
    r(110, 20, 180, 140, "#a9d3ea"), c(250, 55, 16, "#fff3b0"), f'<path d="M110,140 l40,-30 l30,18 l40,-36 l70,48 v20 h-180 Z" fill="#7fae8a"/>',
    r(106, 16, 188, 8, "#8a6a4a", 3),
    f'<path d="M106,24 q12,8 0,16 q12,8 0,16 q12,8 0,16 q12,8 0,16 q12,8 0,16 q12,8 0,16 q12,8 0,16 l34,0 l-8,-112 Z" fill="#c25e4f"/>',
    f'<path d="M294,24 q-12,8 0,16 q-12,8 0,16 q-12,8 0,16 q-12,8 0,16 q-12,8 0,16 q-12,8 0,16 q-12,8 0,16 l-34,0 l8,-112 Z" fill="#c25e4f"/>',
    person(200, 232, "#ffffff", "#3b4a5a", "#2b1d16", arms=[[(0, 0), (-28, -16), (-44, -30)], [(0, 0), (28, -16), (44, -30)]], back=True),
    r(300, 176, 100, 50, "#f4f1ea", 4), r(300, 168, 100, 12, "#dcd6ca", 4), r(306, 160, 40, 14, "#ffffff", 6),
]))

# 7 벨맨이 짐 카트에 가방을 싣고 있다
PICS["사진: 벨맨이 짐 카트에 가방을 싣고 있다."] = svg("".join([
    r(0, 0, W, 205, "#e7e0d4"), floor(205, "#cdbfa9"),
    r(20, 30, 60, 120, "#d9e6ea", 3, 'stroke="#8a6a4a" stroke-width="4"'),
    cart(200, 232, 130),
    suitcase(214, 170, 44, 46, "#5b7fa6"), suitcase(262, 178, 52, 38, "#6d8c5e"),
    person(150, 232, "#8a2f36", "#24323f", "#2b1d16", arms=[[(0, 0), (26, -2), (48, -10)], [(0, 0), (30, 6), (50, -2)]], cap="#8a2f36"),
    suitcase(196, 120, 50, 34, "#a65b5b"),
    suitcase(60, 186, 36, 30, "#7d6b9a"), suitcase(100, 194, 30, 22, "#c9a34a"),
]))

# ---------- question bank pictures (RYU 2026-11-23: TOEIC 문제은행) ----------
def desk(x, y, w, h=60, col="#8a6a4a"):
    return r(x, y, w, 8, col, 2) + r(x + 6, y + 8, 6, h, col) + r(x + w - 12, y + 8, 6, h, col)
def bed(x, y, w=200):
    return "".join([r(x, y, w, 40, "#f4f1ea", 6), r(x, y + 40, w, 18, "#dcd6ca", 3), r(x - 8, y - 50, 14, 108, "#8a6a4a", 3),
                    r(x + 10, y - 14, 60, 18, "#ffffff", 8, 'stroke="#d3cfc6" stroke-width="2"')])
def towel(x, y, col):
    return r(x, y, 46, 12, col, 3) + r(x, y + 10, 46, 4, "#00000018", 2)
def glass(x, y):
    return f'<path d="M{x-8},{y-24} L{x+8},{y-24} L{x+6},{y} L{x-6},{y} Z" fill="#e8f1f6" stroke="#9fb3c1" stroke-width="1.8"/>'
def bottle(x, y, col):
    return r(x - 6, y - 34, 12, 34, col, 3) + r(x - 2.5, y - 46, 5, 14, col, 2)
def lounger(x, y):
    return "".join([r(x, y, 70, 8, "#ffffff", 3, 'stroke="#c9ced2" stroke-width="2"'), ln([(x + 70, y + 2), (x + 90, y - 22)], "#ffffff", 8),
                    ln([(x + 6, y + 8), (x + 6, y + 20)], "#9aa7b1", 3), ln([(x + 64, y + 8), (x + 64, y + 20)], "#9aa7b1", 3)])

PICS["사진: 남자가 책상에서 노트북으로 타이핑하고 있다."] = svg("".join([
    r(0, 0, W, 200, "#e6e2da"), floor(200, "#c9c0b2"), r(250, 30, 110, 70, "#d9e6ea", 3, 'stroke="#8a8a8a" stroke-width="4"'),
    person(180, 232, "#5b7fa6", "#2c3a48", "#2b1d16", arms=[[(0, 0), (20, 22), (44, 26)], [(0, 0), (22, 26), (50, 28)]]),
    desk(200, 162, 150), r(232, 150, 56, 12, "#3d4a55", 2), f'<path d="M236,150 L246,112 L296,112 L290,150 Z" fill="#56646f"/>',
    r(306, 140, 20, 22, "#ffffff", 3), r(310, 132, 12, 10, "#7a5a3a", 2)]))
PICS["사진: 여자가 잔에 물을 따르고 있다."] = svg("".join([
    r(0, 0, W, 180, "#efe4d2"), floor(180, "#b89a76"), set_table(250, 176),
    person(150, 232, "#ffffff", "#24323f", "#2b1d16", female=True, arms=[[(0, 0), (30, 6), (58, -4)], [(0, 0), (10, 30), (8, 44)]]),
    f'<path d="M206,120 l18,0 l2,24 l-22,0 Z" fill="#cfe3ee" stroke="#9fb3c1" stroke-width="2"/>', ln([(226, 128), (236, 136)], "#9fb3c1", 3),
    ln([(234, 140), (238, 158)], "#7fb8de", 3), glass(240, 172)]))
PICS["사진: 침대 위에 수건이 개어져 있다."] = svg("".join([
    r(0, 0, W, 190, "#e9e2d6"), floor(190, "#b9a58c"), r(270, 30, 90, 70, "#a9d3ea", 3, 'stroke="#8a6a4a" stroke-width="4"'),
    bed(80, 140, 240), towel(170, 128, "#ffffff"), towel(170, 116, "#ffffff"), towel(226, 128, "#cfe3ee"), towel(226, 116, "#cfe3ee"),
    r(330, 150, 50, 60, "#8a6a4a", 3), c(355, 140, 9, "#ffe7a8")]))
PICS["사진: 두 사람이 로비에서 악수하고 있다."] = svg("".join([
    r(0, 0, W, 205, "#e6ded2"), floor(205, "#cdbfa9"), r(30, 40, 60, 110, "#d9e6ea", 3, 'stroke="#b8a888" stroke-width="4"'),
    r(320, 150, 34, 55, "#7d9b76", 6), c(337, 140, 22, "#6e9a64"),
    person(160, 232, "#2f4f66", "#24323f", "#2b1d16", arms=[[(0, 0), (20, 16), (36, 20)], [(0, 0), (-6, 30), (-6, 44)]]),
    person(240, 232, "#6d6d6d", "#2c3a48", "#4a3426", female=True, arms=[[(0, 0), (-20, 16), (-36, 20)], [(0, 0), (6, 30), (6, 44)]])]))
PICS["사진: 남자가 계단을 올라가고 있다."] = svg("".join([
    r(0, 0, W, H, "#e7e1d6"),
    "".join(r(120 + i * 34, 232 - i * 26, W, 26, "#cdbfa9" if i % 2 else "#d8cbb6") for i in range(8)),
    ln([(110, 200), (380, -10)], "#8a6a4a", 5),
    person(190, 180, "#a65b5b", "#2c3a48", "#2b1d16", arms=[[(0, 0), (10, 18), (16, 34)], [(0, 0), (-10, 20), (-14, 34)]], back=True)]))
PICS["사진: 수영장 옆에 선베드가 줄지어 놓여 있다."] = svg("".join([
    r(0, 0, W, 120, "#bfe0f2"), c(330, 40, 18, "#fff3b0"), r(0, 120, W, 140, "#e9dcc4"),
    r(20, 190, 360, 60, "#6cc0e0", 6), ln([(40, 210), (90, 205), (140, 212)], "#ffffff88", 3),
    lounger(30, 150), lounger(130, 150), lounger(230, 150),
    ln([(355, 180), (355, 90)], "#9aa7b1", 4), f'<path d="M315,100 Q355,60 395,100 Z" fill="#e85d4a"/>']))
PICS["사진: 여자가 진공청소기로 바닥을 청소하고 있다."] = svg("".join([
    r(0, 0, W, 190, "#e9e2d6"), floor(190, "#b9a58c"), bed(250, 150, 160),
    person(150, 232, "#7a8a96", "#2c3a48", "#2b1d16", female=True, arms=[[(0, 0), (20, 20), (36, 34)], [(0, 0), (16, 26), (30, 38)]]),
    ln([(186, 160), (224, 222)], "#56646f", 5), r(212, 218, 36, 12, "#3d4a55", 4), r(96, 196, 40, 30, "#c25e4f", 8), ln([(136, 210), (186, 162)], "#3d4a55", 3)]))
PICS["사진: 남자가 지도를 보고 있다."] = svg("".join([
    r(0, 0, W, 190, "#cfe3ee"), r(0, 190, W, 70, "#b9b3a6"), r(40, 90, 80, 100, "#d8c7ae"), f'<path d="M30,92 L80,60 L130,92 Z" fill="#8a5a3a"/>',
    r(290, 70, 90, 120, "#c9b79c"), r(300, 90, 20, 26, "#a9d3ea"), r(340, 90, 20, 26, "#a9d3ea"),
    person(200, 232, "#6d8c5e", "#3b4a5a", "#2b1d16", arms=[[(0, 0), (-16, 14), (-30, 10)], [(0, 0), (16, 14), (30, 10)]]),
    r(166, 112, 68, 46, "#fdfaf3", 2, f'stroke="{INK}" stroke-width="1.5"'), ln([(172, 120), (196, 140), (228, 124)], "#e85d4a", 2), ln([(180, 150), (214, 116)], "#7cbf5a", 2)]))
PICS["사진: 버스가 호텔 앞에 서 있다."] = svg("".join([
    r(0, 0, W, 200, "#e9e4da"), r(0, 200, W, 60, "#9a9a9a"), r(0, 196, W, 6, "#cfc6b8"),
    r(20, 18, 200, 20, "#2f4f66", 3), f'<text x="120" y="33" font-size="13" fill="#f3e2b3" text-anchor="middle" font-family="serif" letter-spacing="4">HOTEL</text>',
    r(30, 38, 180, 158, "#7a8a96"), r(40, 50, 70, 146, "#b9d3e0"), r(130, 50, 70, 146, "#b9d3e0"),
    r(150, 120, 230, 96, "#e8b23b", 10), r(162, 132, 200, 34, "#b9d3e0", 4), r(150, 176, 230, 6, "#c9932b"),
    c(196, 220, 14, INK), c(336, 220, 14, INK), c(196, 220, 6, "#9a9a9a"), c(336, 220, 6, "#9a9a9a")]))
PICS["사진: 여자가 여행 가방을 끌고 걸어가고 있다."] = svg("".join([
    r(0, 0, W, 200, "#e6ded2"), floor(200, "#cdbfa9"), r(300, 40, 70, 120, "#d9e6ea", 3, 'stroke="#b8a888" stroke-width="4"'),
    person(170, 232, "#c25e4f", "#3b4a5a", "#2b1d16", female=True, arms=[[(0, 0), (26, 22), (48, 30)], [(0, 0), (-10, 24), (-18, 36)]], lean=4),
    ln([(220, 146), (236, 176)], INK, 3), suitcase(220, 176, 46, 50, "#5b7fa6", handle=False), c(228, 228, 4, INK), c(258, 228, 4, INK)]))
PICS["사진: 요리사가 프라이팬으로 요리하고 있다."] = svg("".join([
    r(0, 0, W, 160, "#e3e7e9"), r(0, 160, W, 100, "#b8bfc4"), r(220, 150, 170, 70, "#9aa3a9", 3), r(214, 142, 182, 12, "#c3cbd0", 3),
    c(260, 140, 14, "#e8743b"), c(320, 140, 14, "#3d4a55"),
    person(150, 232, "#ffffff", "#3b4a5a", "#2b1d16", arms=[[(0, 0), (40, 4), (80, 0)], [(0, 0), (16, 26), (20, 40)]], cap="#ffffff"),
    f'<ellipse cx="262" cy="128" rx="30" ry="7" fill="#3d4a55"/>', ln([(232, 126), (196, 124)], "#3d4a55", 5),
    c(256, 124, 6, "#f2d03b"), c(270, 125, 5, "#7cbf5a"), ln([(250, 108), (254, 96)], "#ffffff", 2), ln([(268, 108), (272, 94)], "#ffffff", 2)]))
PICS["사진: 선반에 와인병들이 진열되어 있다."] = svg("".join([
    r(0, 0, W, H, "#efe4d2"), r(60, 20, 280, 220, "#8a6a4a", 4), r(70, 30, 260, 200, "#6b4f35"),
    "".join(r(70, 86 + i * 64, 260, 8, "#a5825c") for i in range(3)),
    "".join(bottle(92 + j * 34, 86 + i * 64, ["#6a1f2b", "#2f5a3a", "#c9a34a"][(i + j) % 3]) for i in range(3) for j in range(7))]))
PICS["사진: 남자가 전화 통화를 하고 있다."] = svg("".join([
    r(0, 0, W, 200, "#e6e2da"), floor(200, "#c9c0b2"), r(40, 40, 90, 70, "#d9e6ea", 3, 'stroke="#8a8a8a" stroke-width="4"'),
    desk(230, 160, 140), r(260, 146, 40, 14, "#3d4a55", 3),
    person(190, 232, "#2f4f66", "#24323f", "#2b1d16", arms=[[(0, 0), (-6, 30), (-6, 44)], [(0, 0), (14, 4), (4, -16)]]),
    r(201, 88, 8, 24, INK, 3), c(209, 108, 5.5, SKIN)]))
