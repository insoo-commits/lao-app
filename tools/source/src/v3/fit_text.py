# v3.34 (RYU 2026-11-24): intro + tips should be about as tall as the 소분류 picture.
# Rules shorten repeated long tips everywhere; EDITS rewrites single bundles. Usage: python3 fit_text.py app.js [edits.json]
import json, re, sys
p = sys.argv[1]
lines = open(p, encoding="utf8").read().split("\n", 1)
L = lines[0]; pre = "const DATA=JSON.parse("
lit = L[len(pre):L.rindex(")")]
d = json.loads(json.loads(lit))
RULES = [
    ("• 성조 번호는 교재의 6성조(1~6성)를 따랐어요. 앱 음성은 컴퓨터 음성이라 몇몇 낱말은 높낮이가 다르게 들릴 수 있어요.", "• 성조 번호는 교재의 6성조(1~6성)를 따랐어요."),
    ("• 부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 4성(낮게 시작해 올라감), 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 가운데 자음처럼 1성(평성)입니다. 받침 ກ ດ ບ로 끝나도 같아요.", "• 부호가 없으면 높은 자음(ຂ ສ ຖ ຜ ຝ ຫ)은 4성, 낮은 자음(ຄ ຊ ທ ພ ຟ ຮ)은 1성이에요."),
    ("• ◌່ 가 붙으면 5성(높게 평평, 낮은 자음은 3성으로 적음), ◌້ 가 붙으면 2성(높게 시작해 떨어짐)이 됩니다. 높은 자음에 ◌້ 는 6성이에요.", "• ◌່는 5성(낮은 자음은 3성), ◌້는 2성, 높은 자음에 ◌້는 6성이에요."),
]
IRULES = [
    ("글자는 같고 성조 부호만 다른 짝이에요. 부호 하나로 소리 높이와 뜻이 바뀝니다.", "글자는 같고 성조 부호만 다른 짝이에요."),
    ("한글로는 같은 소리인데 첫 자음이 높은 자음이냐 낮은 자음이냐에 따라 성조가 달라지는 짝이에요.", "같은 소리지만 높은·낮은 자음이라 성조가 다른 짝이에요."),
]
first = {s["b"][0] for p in d["P"] for s in p["subs"]}
n = 0
for k, b in d["B"].items():
    for a, z in IRULES:
        if b["i"] == a: b["i"] = z
    if k[:4] in ("7-03", "7-04") and b["tp"] and len(b["tp"][0]) > 90 and len(b["tp"]) == 3:
        b["tp"] = b["tp"][:2]
    if k not in first and "• 성조 번호는 교재의 6성조(1~6성)를 따랐어요." in b["tp"] and len(b["tp"]) > 3:
        b["tp"] = [t for t in b["tp"] if t != "• 성조 번호는 교재의 6성조(1~6성)를 따랐어요."]
    tp = []
    for t in b["tp"]:
        for a, z in RULES:
            if t == a: t = z
        if t.startswith("• 소리 높이:"):
            t = re.sub(r"(\d성)\([^()]*(\([^()]*\)[^()]*)*\)", r"\1", t)
        tp.append(t)
    if tp != b["tp"]: b["tp"] = tp; n += 1
if len(sys.argv) > 2:
    E = json.load(open(sys.argv[2], encoding="utf8"))
    for k, e in E.items():
        if "i" in e: d["B"][k]["i"] = e["i"]
        if "tp" in e: d["B"][k]["tp"] = e["tp"]
        n += 1
out = pre + json.dumps(json.dumps(d, ensure_ascii=False, separators=(",", ":")), ensure_ascii=False) + ")" + L[L.rindex(")") + 1:]
open(p, "w", encoding="utf8").write(out + "\n" + lines[1])
print("changed", n)
