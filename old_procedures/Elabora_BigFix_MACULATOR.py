import csv
import Common as cm
import unicodedata

# --------------------------------------------------------------------------
# Normalizare text (elimina BOM, accente, spaces, diffs)
# --------------------------------------------------------------------------
def norm(s):
    if s is None:
        return ""
    s = s.replace("\ufeff", "")
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s

# --------------------------------------------------------------------------
class c_BGFX:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

# --------------------------------------------------------------------------
BGFX = []

# câmpurile pe care le vrei în output
BGFX_field = [
    "Stato",
    "Nome computer",
    "Sistema operativo",
    "Nome DNS",
    "Tipo di computer",
    "Core partizione",
    "Core server",
    "Stringa marchio processore",
    "Vendor",
    "PVU per core",
    "Valore PVU modificato",
    "Valore PVU predefinito",
    "Fattore core Oracle",
    "Socket attivi del server",
    "Nome cluster",
    "Core cluster"
]

# --------------------------------------------------------------------------
print("Procedura per la elaborazione dei dati da BigFix.")

cm.check_outdir(cm.out_path)

# Identificăm file BigFix cel mai recent
file_pattern = cm.pr["BGFX_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
input_file = sorted(cm.files, reverse=True)[0]

print("Elaborazione file " + input_file)

nomi = set()
nomi_doppi = []

# --------------------------------------------------------------------------
# CITIRE ROBUSTĂ CU trova_separa + togli_apici + mapare după nume
# --------------------------------------------------------------------------
with open(input_file, encoding="utf-8") as fc:

    # citim prima linie
    first_line = fc.readline()

    # dacă e "sep=," o ignorăm
    if first_line.lower().startswith("sep="):
        separa = first_line.strip().split("=", 1)[1]
    else:
        separa = cm.trova_separa(first_line)
        fc.seek(0)

    # citim headerul real
    header_raw = fc.readline()
    header_clean = cm.togli_apici(header_raw, separa)
    header_list = [h.replace("\ufeff", "") for h in header_clean.split(separa)]

    # construim mapare normalizată
    header_map = {norm(h): h for h in header_list}

    # citim restul liniilor
    for line in fc:
        tmp = cm.togli_apici(line, separa)
        cols = tmp.split(separa)

        # construim dict row = {header: valoare}
        row = {}
        for i, h in enumerate(header_list):
            row[h] = cols[i] if i < len(cols) else ""

        # găsim numele serverului
        key_nome = header_map.get(norm("Nome computer"))
        if not key_nome:
            continue

        nome = row.get(key_nome, "").lower()
        if not nome:
            continue

        if nome in nomi:
            nomi_doppi.append(nome)
            continue

        nomi.add(nome)

        # extragem valorile în ordinea BGFX_field
        valori = []
        for field in BGFX_field:
            key = header_map.get(norm(field), "")
            valori.append(row.get(key, ""))

        BGFX.append(c_BGFX(nome, valori))

# --------------------------------------------------------------------------
# scriem fisier output
# --------------------------------------------------------------------------
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_BGFX"]])

with open(output_file, "w", encoding="utf-8") as f:
    f.write("sep=" + separa + "\n")
    f.write(separa.join(BGFX_field) + "\n")

    for obj in BGFX:
        f.write(separa.join(map(str, obj.dati)) + "\n")

print("\nScrittura completata:", output_file)