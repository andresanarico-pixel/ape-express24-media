import os
from PIL import Image, ImageDraw, ImageFont

BG = (15, 77, 77); CARD2 = (24, 98, 98); CREAM = (246, 243, 234); AMBER = (242, 177, 52)
GREEN = (11, 122, 59); DARK = (16, 34, 43); WHITE = (255, 255, 255); SOFT = (213, 225, 230); MUTED = (52, 80, 92)
OUT = "/home/claude/ape/week1"
os.makedirs(OUT, exist_ok=True)
LEFT = 84

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/opentype/inter/{name}.otf", size)

def fit(s, name, size, maxw):
    while font(name, size).getlength(s) > maxw:
        size -= 2
    return font(name, size)

def base(w, h, bg):
    im = Image.new("RGB", (w, h), bg)
    return im, ImageDraw.Draw(im)

def brand(d, y, color, rule):
    d.text((LEFT, y), "APExpress24", font=font("Inter-ExtraBold", 44), fill=color)
    d.rectangle((LEFT, y + 66, LEFT + 120, y + 72), fill=rule)

def lines(d, x, y, items, maxw=912):
    """items: list of (text, fontname, size, color, gap_after)"""
    for s, fn, size, col, gap in items:
        f = fit(s, fn, size, maxw)
        d.text((x, y), s, font=f, fill=col)
        y += int(f.size * 1.12) + gap
    return y

def cover(name, head, sub, h=1350, y0=None, swipe=True):
    im, d = base(1080, h, BG)
    top = 120 if h == 1350 else 250
    brand(d, top, AMBER, AMBER)
    y = y0 or (420 if h == 1350 else 560)
    items = [(t, "Inter-Black", 124 if h == 1350 else 130, c, 8) for t, c in head]
    y = lines(d, LEFT, y, items)
    if sub:
        lines(d, LEFT, y + 30, [(sub, "Inter-SemiBold", 42, SOFT, 0)])
    if swipe:
        d.text((LEFT, h - 85), "Scorri →", font=font("Inter-Bold", 38), fill=CREAM)
    d.text((W_ - LEFT, h - 130), "apexpress24.it", font=font("Inter-Regular", 32), fill=SOFT, anchor="ra") if False else None
    im.save(f"{OUT}/{name}.png", optimize=True)

W_ = 1080

def statement(name, kicker, big, caption, bigcolor=None, h=1350):
    im, d = base(1080, h, CREAM)
    brand(d, 120, BG, AMBER)
    d.text((LEFT, 420), kicker, font=fit(kicker, "Inter-Bold", 50, 912), fill=MUTED)
    f = fit(big, "Inter-Black", 230, 912)
    d.text((LEFT, 520), big, font=f, fill=bigcolor or GREEN)
    y = 520 + int(f.size * 1.25)
    lines(d, LEFT, y + 20, [(c, "Inter-SemiBold", 48, DARK, 14) for c in caption], maxw=912)
    d.text((LEFT, h - 85), "Scorri →", font=font("Inter-Bold", 38), fill=BG)
    im.save(f"{OUT}/{name}.png", optimize=True)

def table(name, title, rows, foot, h=1350):
    im, d = base(1080, h, CREAM)
    brand(d, 120, BG, AMBER)
    y = lines(d, LEFT, 330, [(t, "Inter-Black", 92, DARK, 6) for t in title])
    y += 30
    for a, b in rows:
        d.rounded_rectangle((LEFT, y, 1080 - LEFT, y + 84), radius=16, fill=WHITE)
        d.text((LEFT + 32, y + 18), a, font=font("Inter-Bold", 42), fill=DARK)
        d.text((1080 - LEFT - 32, y + 18), b, font=font("Inter-Black", 44), fill=GREEN, anchor="ra")
        y += 98
    lines(d, LEFT, y + 14, [(f, "Inter-Regular", 32, MUTED, 4) for f in foot])
    d.text((LEFT, h - 85), "Scorri →", font=font("Inter-Bold", 38), fill=BG)
    im.save(f"{OUT}/{name}.png", optimize=True)

def points(name, title, pts, h=1350, foot=None):
    im, d = base(1080, h, CREAM)
    brand(d, 120, BG, AMBER)
    y = lines(d, LEFT, 330, [(t, "Inter-Black", 96, DARK, 6) for t in title]) + 40
    for i, p in enumerate(pts):
        d.rounded_rectangle((LEFT, y, 1080 - LEFT, y + 170), radius=22, fill=WHITE)
        d.ellipse((LEFT + 30, y + 42, LEFT + 116, y + 128), fill=GREEN)
        d.text((LEFT + 73, y + 85), str(i + 1), font=font("Inter-Black", 46), fill=WHITE, anchor="mm")
        f = fit(p, "Inter-Bold", 40, 700)
        d.text((LEFT + 150, y + 85), p, font=f, fill=DARK, anchor="lm")
        y += 190
    if foot:
        lines(d, LEFT, y + 6, [(foot, "Inter-Regular", 32, MUTED, 0)])
    d.text((LEFT, h - 85), "Scorri →", font=font("Inter-Bold", 38), fill=BG)
    im.save(f"{OUT}/{name}.png", optimize=True)

def cta(name, l1, l2, sub, h=1350, foot="Varese · Milano · Como · Monza"):
    im, d = base(1080, h, GREEN)
    top = 120 if h == 1350 else 250
    brand(d, top, WHITE, AMBER)
    y = 380 if h == 1350 else 520
    y = lines(d, LEFT, y, [(l1, "Inter-Black", 120, WHITE, 6), (l2, "Inter-Black", 120, AMBER if False else (255, 232, 160), 6)])
    lines(d, LEFT, y + 20, [(sub, "Inter-SemiBold", 42, (228, 243, 234), 0)])
    by = h - 520 if h == 1350 else h - 640
    d.rounded_rectangle((LEFT, by, 1080 - LEFT, by + 150), radius=30, fill=WHITE)
    d.text((540, by + 75), "Vai al preventivatore", font=fit("Vai al preventivatore", "Inter-ExtraBold", 56, 800), fill=GREEN, anchor="mm")
    d.text((LEFT, by + 190), "apexpress24.it/configuratore", font=font("Inter-Bold", 42), fill=WHITE)
    d.text((LEFT, by + 252), "Link in bio", font=font("Inter-Regular", 36), fill=(228, 243, 234))
    d.text((LEFT, by + 330), foot, font=font("Inter-SemiBold", 32), fill=(255, 232, 160))
    im.save(f"{OUT}/{name}.png", optimize=True)

def story(name, head, sub, accent_lines=None, bg=BG):
    im, d = base(1080, 1920, bg)
    brand(d, 250, AMBER, AMBER)
    y = lines(d, LEFT, 520, [(t, "Inter-Black", 130, c, 10) for t, c in head])
    if sub:
        y = lines(d, LEFT, y + 30, [(s, "Inter-SemiBold", 46, SOFT, 10) for s in sub])
    d.rounded_rectangle((LEFT, 1330, 1080 - LEFT, 1330 + 150), radius=30, fill=GREEN)
    d.text((540, 1405), "Vai al preventivatore", font=fit("Vai al preventivatore", "Inter-ExtraBold", 56, 800), fill=WHITE, anchor="mm")
    d.text((540, 1530), "apexpress24.it/configuratore", font=font("Inter-Bold", 38), fill=CREAM, anchor="ma")
    im.save(f"{OUT}/{name}.png", optimize=True)

# ===== Carosello A: affitto =====
cover("A1_affitto", [("Hai messo casa", CREAM), ("in affitto?", CREAM), ("E l'APE?", AMBER)], "Controlla prima di firmare il contratto.")
statement("A2_affitto", "Serve anche per l'affitto", "Sì.", ["Per ogni nuovo contratto di locazione l'APE è necessario."])
points("A3_affitto", ["E se il contratto", "si rinnova da solo?"], ["Rinnovo tacito = nuovo contratto", "L'APE deve essere ancora valida", "Se è scaduta, va rifatta"])
cta("A4_affitto", "Affitti casa?", "Parti dall'APE", "Calcola il prezzo prima di pagare.")

# ===== Carosello B: costi =====
cover("B1_costi", [("Quanto costa", CREAM), ("un APE?", AMBER)], "Dipende dai metri quadri. Ecco i prezzi.")
table("B2_costi", ["Prezzo per", "superficie"], [("Fino a 99 m²", "99 €"), ("100 – 149 m²", "119 €"), ("150 – 199 m²", "139 €"), ("200 – 299 m²", "169 €"), ("300 – 399 m²", "199 €"), ("400 – 499 m²", "239 €")], ["Prezzi + IVA 22%, più 10 € di contributo CENED.", "Oltre 500 m²: preventivo personalizzato."])
statement("B3_costi", "Esempio: appartamento da 90 m²", "130,78 €", ["Totale con IVA e contributo CENED.", "Sopralluogo incluso."], bigcolor=GREEN)
cta("B4_costi", "Il tuo prezzo", "in pochi clic", "Inserisci i dati nel preventivatore.")

# ===== Carosello C: durata =====
cover("C1_durata", [("Quanto dura", CREAM), ("un APE?", AMBER)], "La risposta breve: 10 anni. Ma c'è un'eccezione.")
statement("C2_durata", "Validità massima", "10 anni", ["Dalla data di registrazione", "dell'attestato."])
statement("C3_durata", "Decade prima se fai", "Lavori", ["che cambiano la prestazione", "energetica dell'edificio."], bigcolor=GREEN)
cta("C4_durata", "APE scaduta?", "Rifalla in 5 giorni", "Lavorativi, dal sopralluogo del tecnico.")

# ===== Carosello D: CURIT =====
cover("D1_curit", [("Hai controllato", CREAM), ("la caldaia?", CREAM), ("Il CURIT.", AMBER)], "Prima dell'APE, un controllo che conta.")
statement("D2_curit", "Cos'è il CURIT", "Catasto", ["Il Catasto Unico Regionale", "degli Impianti Termici."], bigcolor=GREEN)
points("D3_curit", ["Cosa tenere", "pronto"], ["Libretto di impianto della caldaia", "Targa dell'impianto (codice CURIT)", "Dati catastali dell'immobile"], foot="Meno intoppi durante il sopralluogo.")
cta("D4_curit", "Pronto per", "l'APE?", "Calcola il preventivo online.")

# ===== Stories =====
story("S1_durata", [("Quanto dura", CREAM), ("un APE?", AMBER)], ["10 anni", "dalla registrazione."])
story("S2_affitto", [("Affitti casa?", CREAM), ("Serve l'APE.", AMBER)], ["Per ogni nuovo contratto", "di locazione."])
story("S3_curit", [("Hai la targa", CREAM), ("CURIT?", AMBER)], ["Tienila pronta per il", "sopralluogo."])
story("S4_prezzo", [("APE da", CREAM), ("99 € + IVA", AMBER)], ["Fino a 99 m².", "+ 10 € contributo CENED."])
print(sorted(os.listdir(OUT)))
