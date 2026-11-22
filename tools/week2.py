import os
src = open(os.path.join(os.path.dirname(__file__), "static.py")).read().split("# ===== Carosello A")[0]
src = src.replace('OUT = "/home/claude/ape/week1"', 'OUT = "/home/claude/ape/week2"')
exec(src)

# Carosello E: annuncio con classe energetica (Milano)
cover("E1_annuncio", [("Annuncio", CREAM), ("immobiliare?", CREAM), ("Indica la classe.", AMBER)], "Milano e hinterland: cosa serve prima di pubblicare.")
statement("E2_annuncio", "Nell'annuncio va indicata", "La classe", ["energetica dell'immobile.", "Serve un APE valido."], bigcolor=GREEN)
points("E3_annuncio", ["Prima di", "pubblicare"], ["Controlla che l'APE sia valida", "Se manca, richiedilo online", "Sopralluogo e firma digitale inclusi"], foot="Prezzo chiaro prima di pagare.")
cta("E4_annuncio", "Vendi o affitti", "a Milano?", "Calcola il preventivo APE online.")

# Stories
story("S5_tempi", [("APE in", CREAM), ("5 giorni", AMBER)], ["Lavorativi dal sopralluogo.", "Priority 3 giorni. Urgente 48 ore."])
story("S6_varese", [("Varese e", CREAM), ("provincia", AMBER)], ["Gallarate, Busto Arsizio,", "Saronno, Cassano Magnago..."])
