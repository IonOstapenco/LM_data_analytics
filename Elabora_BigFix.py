import csv
import Common as cm
import unicodedata

# --------------------------------------------------------------------------
# Normalizzazione del testo (rimozione BOM, accenti, spazi e differenze di formattazione)
# Normalizare text (elimina BOM, accente, spaces, diffs)
# --------------------------------------------------------------------------
def norm(s):
    if s is None:
        return ""
    s = s.replace("\ufeff", "")       # eliminare  BOM
                                      # rimozione del BOM
    s = s.strip().lower()             # eliminare spatii + lowercase
                                      # rimozione spazi iniziali/finali + conversione in minuscolo
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s

# --------------------------------------------------------------------------
# Classe utilizzata per salvare i dati letti dal file BigFix
# Clasa folosita pentru salvarea datelor din BigFix
# --------------------------------------------------------------------------
class c_BGFX:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

# --------------------------------------------------------------------------
# Lista che conterrà i record BigFix processati
# Lista unde salvam recordurile BigFix procesate
# --------------------------------------------------------------------------
BGFX = []

# prendiamo in considerazione solo i campi effettivamente presenti
# luam in considereare campuri care sunt, s-au eliminat acele care nu-s
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
# Avvio procedura di elaborazione dati BigFix
# Pornim procedura de prelucrare date BigFix
# --------------------------------------------------------------------------
print("Procedura per la elaborazione dei dati da BigFix.")

cm.check_outdir(cm.out_path)

# Identificazione del file BigFix più recente
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
# Lettura file con DictReader + rilevamento separatore + normalizzazione header
# citim cu dictreader, si mai detectam separator + normalizam headeruri caci mi dadea erori
# --------------------------------------------------------------------------
with open(input_file, encoding="utf-8") as fc:
    sample = fc.read(2048)

    # rilevamento automatico del delimitatore
    # detectare automata separator
    dialect = csv.Sniffer().sniff(sample)

    fc.seek(0)

    reader = csv.DictReader(fc, dialect=dialect)

    # Costruiamo una mappa tra header normalizzato e header reale (che poteva contenere BOM)
    # Construim mapping dintre header normalizat si header real(care avea BOM)
    header_map = {}

    for h in reader.fieldnames:
        clean = h.replace("\ufeff", "")  # rimozione BOM
                                         # facem replace

        header_map[norm(clean)] = h

        #print("afisam headeruri")
        #print(header_map)

    # elaboriamo ogni riga del file
    # trecem fiecare rind
    for row in reader:

        # identifichiamo la colonna reale per "Nome computer"
        # gasim coloana reala pentru "Nome computer"
        key_nome = header_map.get(norm("Nome computer"))

        if not key_nome:
            continue

     #   nome = row.get(key_nome, "").lower()
        nome = norm(row.get(key_nome, ""))

        if not nome:
            continue

        # verifica duplicati
        # verificam duplicate
        if nome in nomi:
            nomi_doppi.append(nome)
            continue

        nomi.add(nome)

        # estraiamo i valori nell'ordine definito da BGFX_field
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
# Scrittura file di output ICTG-HW (definito in parametri.json come OUT_BGFX)
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
# Scrittura file con server duplicati (opzionale)
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