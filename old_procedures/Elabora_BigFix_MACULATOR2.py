import csv
import Common as cm
import unicodedata

# --------------------------------------------------------------------------
# Normalizare text (elimina BOM, accente, spaces, diffs)
# --------------------------------------------------------------------------
def norm(s):
    if s is None:
        return ""
    s = s.replace("\ufeff", "")       # eliminare  BOM
    s = s.strip().lower()             # eliminare spatii (caci inca nu am curatit ) + lowercase
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

#luam in considereare campuri care sunt, s-au eliminat acele care nu-s
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

# Identificăm file  BigFix cel mai recent
file_pattern = cm.pr["BGFX_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)
input_file = temp[0]

print("Elaborazione file " + input_file)

delimiter = cm.cs
nomi = set()
nomi_doppi = []

# --------------------------------------------------------------------------
# 
#citim cu dictreader, si mai detectam separator + normalizam headeruri caci mi dadea erori
# --------------------------------------------------------------------------
with open(input_file, encoding="utf-8") as fc:
    sample = fc.read(2048)
    dialect = csv.Sniffer().sniff(sample)
    fc.seek(0)

    reader = csv.DictReader(fc, dialect=dialect)

    # Construim mapping dintre header normalizat si header real(care avea BOM)
    header_map = {}
    for h in reader.fieldnames:
        clean = h.replace("\ufeff", "")  # facem replace

        header_map[norm(clean)] = h

        #print("afisam headeruri")
        #print(header_map)

    # trecem fiecare rrind
    for row in reader:
        # gasim coloana reala pentru "Nome computer"
        key_nome = header_map.get(norm("Nome computer"))
        if not key_nome:
            continue

     #   nome = row.get(key_nome, "").lower()
        nome = norm(row.get(key_nome, ""))

        if not nome:
            continue

        if nome in nomi:
            nomi_doppi.append(nome)
            continue

        nomi.add(nome)

        # extragem valorile în ordinea BGFX_field
        valori = []

        for field in BGFX_field:
            key = header_map.get(norm(field))
            if key is None:
                valori.append("")
            else:
                valori.append(row.get(key, "").strip())


        BGFX.append(c_BGFX(nome, valori))

# --------------------------------------------------------------------------
# scriem fisier output ictg-hw, care in parametri.json se numeste out_bgfx
# --------------------------------------------------------------------------
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_BGFX"]])

with open(output_file, "w", encoding="utf-8") as f:
    f.write("sep=" + delimiter + "\n")
    f.write(delimiter.join(BGFX_field) + "\n")

    for obj in BGFX:
        f.write(delimiter.join(map(str, obj.dati)) + "\n")


print("\nScrittura completata:", output_file)

'''
# --------------------------------------------------------------------------
# SCRIERE FILE CU DUPLICATE (optional)
# --------------------------------------------------------------------------
if nomi_doppi:
    dup_file = cm.dr.join([cm.out_path, "BGFX_Duplicati.csv"])
    with open(dup_file, "w", encoding="utf-8") as f:
        f.write("Nome computer\n")
        for n in nomi_doppi:
            f.write(n + "\n")

    print("Trovati duplicati. File salvato:", dup_file)
    '''