import sys, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (15, 77, 77); CARD2 = (24, 98, 98); CREAM = (246, 243, 234); AMBER = (242, 177, 52)
GREEN = (11, 122, 59); DARK = (16, 34, 43); WHITE = (255, 255, 255); RED = (179, 38, 47)
SOFT = (213, 225, 230)
LEFT = 84
CLASSES = {"A4": (11, 122, 59), "A3": (31, 138, 60), "B": (232, 217, 58), "C": (244, 183, 58),
           "D": (238, 107, 69), "G": (179, 38, 47)}


def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/{name}.otf", size)

def fit(s, name, size, maxw):
    while font(name, size).getlength(s) > maxw:
        size -= 2
    return font(name, size)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def clamp(x):
    return max(0.0, min(1.0, x))

def eo(t):
    t = clamp(t); return 1 - (1 - t) ** 3

def back(t):
    t = clamp(t); c1 = 1.4; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def ap(t, t0, dur=0.45):
    return eo((t - t0) / dur)

def fo(t, end, d=0.28):
    return 1 - clamp((t - (end - d)) / d)

def rise(t, t0, dist=60, dur=0.5):
    return int((1 - eo((t - t0) / dur)) * dist)

def T(d, x, y, s, f, color, a=1.0, bg=BG):
    if a > 0.01:
        d.text((x, y), s, font=f, fill=lerp(bg, color, clamp(a)))

def R(d, box, r, color, a=1.0, bg=BG):
    if a > 0.01:
        d.rounded_rectangle(box, radius=r, fill=lerp(bg, color, clamp(a)))

def brand(d, a=1.0):
    T(d, LEFT, 250, "APExpress24", font("Inter-ExtraBold", 46), AMBER, a)
    if a > 0.01:
        d.rectangle((LEFT, 316, LEFT + 120, 322), fill=lerp(BG, AMBER, clamp(a)))

def head(d, lines, t, t0, o, colors=None, size=130, y=380, step=None):
    step = step or int(size * 1.12)
    for i, s in enumerate(lines):
        c = (colors[i] if colors else CREAM)
        f = fit(s, "Inter-Black", size, 912)
        T(d, LEFT, y + i * step + rise(t, t0 + i * 0.22), s, f, c, ap(t, t0 + i * 0.22) * o)

def check(d, x, y, s, a, bg=BG, col=GREEN):
    d.ellipse((x, y, x + s, y + s), fill=lerp(bg, col, clamp(a)))
    c = lerp(bg, WHITE, clamp(a)); k = s / 76.0
    d.line((x + 20 * k, y + 40 * k, x + 33 * k, y + 53 * k), fill=c, width=max(3, int(9 * k)))
    d.line((x + 33 * k, y + 53 * k, x + 57 * k, y + 24 * k), fill=c, width=max(3, int(9 * k)))

def stamp(im, label, color, cx, cy, angle, scale, a, size=96):
    f = font("Inter-Black", size)
    tw = int(f.getlength(label)) + 80
    th = size + 60
    lay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle((4, 4, tw - 4, th - 4), radius=18, fill=CREAM + (240,), outline=color + (255,), width=10)
    ld.text((tw // 2, th // 2), label, font=f, fill=color + (255,), anchor="mm")
    lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    nw, nh = max(2, int(lay.width * scale)), max(2, int(lay.height * scale))
    lay = lay.resize((nw, nh), Image.BICUBIC)
    al = lay.getchannel("A").point(lambda v: int(v * clamp(a)))
    im.paste(lay.convert("RGB"), (int(cx - nw / 2), int(cy - nh / 2)), al)

def poly(d, pts, frac, width, color):
    segs = []; total = 0
    for i in range(len(pts) - 1):
        L = math.dist(pts[i], pts[i + 1]); segs.append(L); total += L
    left = total * clamp(frac)
    for i, L in enumerate(segs):
        if left <= 0: break
        k = min(1.0, left / L)
        a, b = pts[i], pts[i + 1]
        e = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        d.line((a, e), fill=color, width=width, joint="curve")
        left -= L

def doc(d, x, y, w, h, a=1.0):
    R(d, (x, y, x + w, y + h), 24, CREAM, a)
    if a > 0.5:
        T(d, x + 40, y + 36, "ATTESTATO DI", font("Inter-Bold", 30), DARK, 1, CREAM)
        T(d, x + 40, y + 74, "PRESTAZIONE ENERGETICA", font("Inter-Bold", 30), DARK, 1, CREAM)
        by = y + 150
        for i, (c, wd) in enumerate([(CLASSES["A4"], 200), (CLASSES["B"], 280), (CLASSES["C"], 360), (CLASSES["D"], 440), (CLASSES["G"], 520)]):
            d.rounded_rectangle((x + 40, by, x + 40 + min(wd, w - 80), by + 44), radius=6, fill=c)
            by += 62

# ---------- shared CTA scene ----------
def cta(im, d, u, l1, l2, sub):
    brand(d)
    f1 = fit(l1, "Inter-Black", 130, 912); f2 = fit(l2, "Inter-Black", 130, 912)
    T(d, LEFT, 480 + rise(u, 0.0), l1, f1, CREAM, ap(u, 0.0))
    T(d, LEFT, 640 + rise(u, 0.2), l2, f2, AMBER, ap(u, 0.2))
    T(d, LEFT, 830 + rise(u, 0.4, 40), sub, font("Inter-SemiBold", 44), SOFT, ap(u, 0.4))
    pulse = 1 + 0.035 * math.sin(u * 6.0) if u > 0.8 else 1
    bp = back((u - 0.7) / 0.5)
    cx, cy = W / 2, 1090
    if bp > 0.02:
        bw, bh = 912 * pulse * bp, 170 * pulse * bp
        d.rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=34, fill=GREEN)
        if bp > 0.8:
            d.text((cx, cy), "Vai al preventivatore", font=fit("Vai al preventivatore", "Inter-ExtraBold", 62, 820), fill=WHITE, anchor="mm")
    T(d, LEFT, 1230, "apexpress24.it/configuratore", font("Inter-Bold", 44), CREAM, ap(u, 1.1))
    T(d, LEFT, 1300, "Link in bio", font("Inter-Regular", 38), SOFT, ap(u, 1.2))
    T(d, LEFT, 1400, "Varese · Milano · Como · Monza", font("Inter-SemiBold", 36), AMBER, ap(u, 1.4))

# ================= REEL 1: rogito =================
def r1_s1(im, d, t, o):
    brand(d, o)
    head(d, ["Il rogito è", "fissato."], t, 0.0, o, size=140, y=360)
    cy = 700 + rise(t, 0.5, 90)
    a = ap(t, 0.5) * o
    R(d, (LEFT, cy, W - LEFT, cy + 500), 28, CREAM, a)
    if a > 0.9:
        R(d, (LEFT, cy, W - LEFT, cy + 96), 28, GREEN, 1, CREAM)
        d.rectangle((LEFT, cy + 60, W - LEFT, cy + 96), fill=GREEN)
        T(d, LEFT + 40, cy + 22, "CHECKLIST ROGITO", font("Inter-ExtraBold", 40), WHITE, 1, GREEN)
        rows = ["Contratto", "Visura catastale", "Documenti notaio", "APE"]
        for i, s in enumerate(rows):
            ry = cy + 130 + i * 90
            T(d, LEFT + 40, ry + 8, s, font("Inter-Bold", 44), DARK, 1, CREAM)
            t0 = 0.9 + i * 0.4
            if i < 3:
                if t > t0: check(d, W - LEFT - 40 - 60, ry, 60, 1, CREAM)
            else:
                if t > t0:
                    blink = 0.5 + 0.5 * math.sin((t - t0) * 9)
                    d.ellipse((W - LEFT - 100, ry, W - LEFT - 40, ry + 60), fill=lerp(CREAM, AMBER, 0.55 + 0.45 * blink))
                    d.text((W - LEFT - 70, ry + 30), "?", font=font("Inter-Black", 46), fill=DARK, anchor="mm")
    T(d, LEFT, 1290 + rise(t, 2.4, 50), "Ti manca l'APE?", fit("Ti manca l'APE?", "Inter-Black", 110, 912), AMBER, ap(t, 2.4) * o)

def r1_s2(im, d, u, o):
    brand(d, o)
    head(d, ["Al rogito", "serve l'APE."], u, 0.0, o, size=130, y=360)
    x, y, w, h = 270, 660, 540, 720
    p = ap(u, 0.4)
    doc(d, x, y + int((1 - p) * 80), w, h, p * o)
    if u > 1.2:
        s = back((u - 1.2) / 0.4)
        stamp(im, "FIRMATO", GREEN, x + w / 2, y + 560, -12, 1.0 * s, o)
    if u > 1.8:
        s2 = back((u - 1.8) / 0.4)
        stamp(im, "REGISTRATO", GREEN, x + w / 2 + 10, y + 650, -8, 0.7 * s2, o, size=70)
    T(d, LEFT, 1470, "Firmato digitalmente e registrato", font("Inter-SemiBold", 40), SOFT, ap(u, 2.0) * o)

def r1_s3(im, d, u, o):
    brand(d, o)
    head(d, ["Ci pensiamo", "noi."], u, 0.0, o, size=140, y=360)
    steps = [("1", "Preventivo online", "Calcoli il prezzo prima di pagare"),
             ("2", "Sopralluogo", "Un tecnico accreditato viene da te"),
             ("3", "APE pronto", "PDF firmato, in 5 giorni lavorativi")]
    y0 = 690
    lp = ap(u, 0.4, 1.4)
    d.line((LEFT + 44, y0 + 44, LEFT + 44, y0 + 44 + 2 * 220 * lp), fill=lerp(BG, AMBER, o), width=8)
    for i, (n, a1, a2) in enumerate(steps):
        t0 = 0.4 + i * 0.6
        a = ap(u, t0) * o
        yy = y0 + i * 220 + rise(u, t0, 40)
        d.ellipse((LEFT, yy, LEFT + 88, yy + 88), fill=lerp(BG, AMBER, a))
        d.text((LEFT + 44, yy + 44), n, font=font("Inter-Black", 50), fill=lerp(BG, DARK, a), anchor="mm")
        T(d, LEFT + 130, yy - 6, a1, font("Inter-ExtraBold", 56), CREAM, a)
        T(d, LEFT + 130, yy + 62, a2, fit(a2, "Inter-Regular", 36, 780), SOFT, a)

def reel1():
    return [(0, 3.6, r1_s1), (3.6, 6.9, r1_s2), (6.9, 9.6, r1_s3),
            (9.6, 12.0, lambda im, d, u, o: cta(im, d, u, "Calcola il tuo", "preventivo", "Prezzo chiaro prima di pagare"))]

# ================= REEL 2: agenzie =================
def listing(d, y, a, label_state, cls=None, flip=1.0):
    R(d, (LEFT, y, W - LEFT, y + 200), 24, CREAM, a)
    if a < 0.6: return
    d.rounded_rectangle((LEFT + 24, y + 24, LEFT + 176, y + 176), radius=14, fill=(190, 205, 210))
    d.polygon([(LEFT + 24, y + 110), (LEFT + 100, y + 44), (LEFT + 176, y + 110)], fill=(120, 150, 158))
    d.rectangle((LEFT + 52, y + 110, LEFT + 148, y + 176), fill=(150, 175, 182))
    d.rounded_rectangle((LEFT + 210, y + 40, LEFT + 640, y + 66), radius=8, fill=(205, 212, 214))
    d.rounded_rectangle((LEFT + 210, y + 88, LEFT + 540, y + 112), radius=8, fill=(222, 227, 228))
    d.rounded_rectangle((LEFT + 210, y + 134, LEFT + 420, y + 158), radius=8, fill=(222, 227, 228))
    bx, by = W - LEFT - 240, y + 60
    bw = int(200 * abs(flip))
    cx = bx + 100
    if label_state == "?":
        d.rounded_rectangle((cx - bw / 2, by, cx + bw / 2, by + 80), radius=14, fill=AMBER)
        if bw > 120:
            d.text((cx, by + 40), "Classe ?", font=font("Inter-ExtraBold", 36), fill=DARK, anchor="mm")
    else:
        col = CLASSES[cls]
        d.rounded_rectangle((cx - bw / 2, by, cx + bw / 2, by + 80), radius=14, fill=col)
        if bw > 120:
            tc = WHITE if cls in ("A4", "A3", "G") else DARK
            d.text((cx, by + 40), f"Classe {cls}", font=font("Inter-ExtraBold", 36), fill=tc, anchor="mm")

def cards_layer(im, d, t, o, flips):
    ys = [680, 910, 1140]
    cls = ["B", "A3", "C"]
    for i, y in enumerate(ys):
        t0 = 0.6 + i * 0.35
        a = ap(t, t0) * o
        yy = y + rise(t, t0, 90)
        ft = flips[i]
        if ft is None or t < ft:
            listing(d, yy, a, "?")
        else:
            k = (t - ft) / 0.5
            if k < 0.5:
                listing(d, yy, a, "?", flip=1 - k * 2)
            else:
                listing(d, yy, a, "c", cls[i], flip=min(1, (k - 0.5) * 2))

def r2_s12(im, d, t, o):
    brand(d, o)
    if t < 3.3:
        head(d, ["Annuncio", "pronto?"], t, 0.0, o, size=140, y=340)
        T(d, LEFT, 650 - 0, "", font("Inter-Bold", 10), CREAM, 0)
    else:
        head(d, ["L'APE per ogni", "immobile."], t, 3.35, o, size=120, y=340)
    flips = [3.8, 4.4, 5.0]
    cards_layer(im, d, t, o, flips)
    if t < 3.3:
        T(d, LEFT, 1400, "Manca solo l'APE.", font("Inter-ExtraBold", 60), AMBER, ap(t, 1.9) * fo(t, 3.3))

def r2_s3(im, d, u, o):
    brand(d, o)
    head(d, ["Tu segui", "il cliente."], u, 0.0, o, size=140, y=340)
    T(d, LEFT, 700 + rise(u, 0.5), "Noi l'APE.", fit("Noi l'APE.", "Inter-Black", 140, 912), AMBER, ap(u, 0.5) * o)
    items = ["Preventivo online per ogni immobile", "Sopralluogo di un tecnico accreditato", "APE firmato digitalmente"]
    for i, s in enumerate(items):
        t0 = 1.1 + i * 0.35
        a = ap(u, t0) * o
        yy = 960 + i * 170 + rise(u, t0, 40)
        R(d, (LEFT, yy, W - LEFT, yy + 140), 22, CARD2, a)
        if a > 0.05: check(d, LEFT + 32, yy + 32, 76, a)
        ff = fit(s, "Inter-Bold", 38, 700)
        T(d, LEFT + 140, yy + 70 - ff.size // 2 - 4, s, ff, CREAM, a)

def reel2():
    return [(0, 6.6, r2_s12), (6.6, 9.4, r2_s3),
            (9.4, 11.8, lambda im, d, u, o: cta(im, d, u, "Un preventivo", "per ogni immobile", "Prezzo in base ai metri quadri"))]

# ================= REEL 3: APE scaduta =================
def r3_s1(im, d, t, o):
    brand(d, o)
    head(d, ["La tua APE", "è scaduta?"], t, 0.0, o, size=140, y=340)
    x, y, w, h = 270, 760, 540, 640
    a = ap(t, 0.3) * o
    doc(d, x, y + rise(t, 0.3, 70), w, h, a)
    if t > 1.0:
        k = clamp((t - 1.0) / 0.35)
        sc = 2.6 - 1.6 * eo(k)
        shake = int(math.sin((t - 1.35) * 40) * 8 * clamp(1 - (t - 1.35) / 0.4)) if t > 1.35 else 0
        stamp(im, "SCADUTA", RED, x + w / 2 + shake, y + 480, -14, sc, o * clamp(k * 2), size=110)

def r3_s2(im, d, u, o):
    brand(d, o)
    head(d, ["Vale al massimo", "10 anni."], u, 0.0, o, size=120, y=340)
    bx, by, bw, bh = LEFT, 820, 912, 70
    d.rounded_rectangle((bx, by, bx + bw, by + bh), radius=16, fill=lerp(BG, CARD2, o))
    p = ap(u, 0.4, 1.8)
    d.rounded_rectangle((bx, by, bx + max(1, int(bw * p)), by + bh), radius=16, fill=lerp(BG, GREEN, o))
    for i, lab in enumerate(["0", "5", "10 anni"]):
        xx = bx + int(bw * i / 2)
        d.line((xx, by + bh + 8, xx, by + bh + 28), fill=lerp(BG, SOFT, o), width=4)
        f = font("Inter-SemiBold", 36)
        tw = f.getlength(lab)
        T(d, min(max(xx - tw / 2, bx), bx + bw - tw), by + bh + 40, lab, f, SOFT, ap(u, 0.6) * o)
    if u > 2.0:
        a = ap(u, 2.0) * o
        mx = bx + int(bw * 0.38)
        d.line((mx, by - 90, mx, by + bh), fill=lerp(BG, AMBER, a), width=8)
        d.ellipse((mx - 20, by - 110, mx + 20, by - 70), fill=lerp(BG, AMBER, a))
        T(d, LEFT, 1160 + rise(u, 2.0, 40), "Ma decade prima", font("Inter-Black", 76), AMBER, a)
        T(d, LEFT, 1260 + rise(u, 2.2, 40), "se fai lavori che cambiano", font("Inter-SemiBold", 44), CREAM, ap(u, 2.2) * o)
        T(d, LEFT, 1320 + rise(u, 2.3, 40), "la prestazione energetica.", font("Inter-SemiBold", 44), CREAM, ap(u, 2.3) * o)

def r3_s3(im, d, u, o):
    brand(d, o)
    head(d, ["Te la rifacciamo", "noi."], u, 0.0, o, size=130, y=340)
    x, y, w, h = 270, 700, 540, 560
    doc(d, x, y + rise(u, 0.2, 70), w, h, ap(u, 0.2) * o)
    if u > 0.9:
        s = back((u - 0.9) / 0.4)
        stamp(im, "NUOVA", GREEN, x + w / 2, y + 430, -10, s, o, size=110)
    T(d, LEFT, 1340 + rise(u, 1.3, 40), "Consegna in 5 giorni lavorativi", fit("Consegna in 5 giorni lavorativi", "Inter-ExtraBold", 52, 912), AMBER, ap(u, 1.3) * o)
    T(d, LEFT, 1410 + rise(u, 1.5, 40), "dal sopralluogo del tecnico", font("Inter-SemiBold", 40), SOFT, ap(u, 1.5) * o)

def reel3():
    return [(0, 3.4, r3_s1), (3.4, 7.0, r3_s2), (7.0, 9.6, r3_s3),
            (9.6, 12.0, lambda im, d, u, o: cta(im, d, u, "Rinnova", "la tua APE", "Calcola il prezzo in pochi minuti"))]

# ================= REEL 4: sopralluogo =================
HOUSE = [(270, 1060), (270, 840), (540, 620), (810, 840), (810, 1060), (270, 1060)]

def r4_s12(im, d, t, o):
    brand(d, o)
    if t < 3.2:
        head(d, ["Chi viene a casa", "tua per l'APE?"], t, 0.0, o, size=112, y=340, step=124)
    else:
        head(d, ["Un tecnico", "accreditato."], t, 3.3, o, size=130, y=340)
    p = ap(t, 0.5, 1.6)
    poly(d, HOUSE, p, 12, lerp(BG, CREAM, o))
    if t > 1.9:
        a = ap(t, 1.9)
        d.rectangle((470, 900, 610, 1060), outline=lerp(BG, CREAM, a * o), width=10)
        d.rectangle((330, 880, 410, 960), outline=lerp(BG, CREAM, a * o), width=10)
        d.rectangle((670, 880, 750, 960), outline=lerp(BG, CREAM, a * o), width=10)
    if 3.2 < t < 6.0:
        sy = 620 + int(((t - 3.2) / 1.6 % 1.0) * 440)
        d.line((250, sy, 830, sy), fill=lerp(BG, AMBER, o), width=8)
    items = ["Superfici e misure", "Impianto di riscaldamento", "Infissi", "Dati catastali"]
    for i, s in enumerate(items):
        t0 = 3.6 + i * 0.5
        if t >= t0:
            a = ap(t, t0) * o
            yy = 1160 + i * 88 + rise(t, t0, 30)
            check(d, LEFT, yy, 60, a)
            T(d, LEFT + 90, yy + 4, s, font("Inter-Bold", 44), CREAM, a)

def r4_s3(im, d, u, o):
    brand(d, o)
    head(d, ["Sempre incluso", "nel prezzo."], u, 0.0, o, size=130, y=340)
    cx, cy = W // 2, 880
    s = back((u - 0.4) / 0.5)
    if s > 0.02:
        r = int(190 * s)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=lerp(BG, GREEN, o))
        if s > 0.9:
            k = 190 / 76.0
            c = lerp(BG, WHITE, o)
            d.line((cx - 80, cy + 5, cx - 25, cy + 60), fill=c, width=26)
            d.line((cx - 25, cy + 60, cx + 90, cy - 60), fill=c, width=26)
    T(d, LEFT, 1160 + rise(u, 1.1, 40), "Tecnico abilitato", font("Inter-Black", 72), AMBER, ap(u, 1.1) * o)
    T(d, LEFT, 1260 + rise(u, 1.3, 40), "iscritto all'elenco regionale", font("Inter-SemiBold", 44), CREAM, ap(u, 1.3) * o)
    T(d, LEFT, 1330 + rise(u, 1.5, 40), "Firma digitale e registrazione", font("Inter-SemiBold", 44), CREAM, ap(u, 1.5) * o)

def reel4():
    return [(0, 6.6, r4_s12), (6.6, 9.2, r4_s3),
            (9.2, 11.6, lambda im, d, u, o: cta(im, d, u, "Prenota il", "sopralluogo", "Parti dal preventivo online"))]

REELS = {"1": reel1, "2": reel2, "3": reel3, "4": reel4}

def frame(scenes, t):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for i, (a, b, fn) in enumerate(scenes):
        if a <= t < b or (i == len(scenes) - 1 and t >= a):
            last = i == len(scenes) - 1
            o = 1.0 if last else fo(t, b)
            fn(im, d, t - a if True else t, o) if i not in () else None
            break
    return im

if __name__ == "__main__":
    key = sys.argv[1]; mode = sys.argv[2]
    scenes = REELS[key]()
    dur = scenes[-1][1]
    if mode == "stills":
        for t in [float(x) for x in sys.argv[3].split(",")]:
            frame(scenes, t).save(f"/home/claude/ape/r{key}_{t}.png")
    else:
        out = sys.argv[3]; tmp = out.replace(".mp4", ".tmp.mp4")
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
                              "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
        for i in range(int(dur * FPS)):
            p.stdin.write(frame(scenes, i / FPS).tobytes())
        p.stdin.close()
        if p.wait() == 0:
            os.rename(tmp, out)
