# ==============================================================================
# ELABORA_ORACLE_FINAL
# Procedura robusta, bazata pe header (nu pe pozitii)
# Output identic logic cu cel obtinut de codul vechi
# ==============================================================================

import csv
import unicodedata
import Common as cm


# ------------------------------------------------------------------------------
# FUNCTII DE NORMALIZARE STRINGHE
# ------------------------------------------------------------------------------

def norm(s):
    """
    Normalizeaza o stringa:
    - elimina BOM
    - lower case
    - elimina spatii
    - elimina accente (unicode)
    """
    if s is None:
        return ""
    s = s.replace("\ufeff", "")   # elimina BOM
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s


def normalize_feature(f):
    """
    Replica comportamentul vechi:
    'Oracle Database Licensable Option - Diagnostics Pack'
    devine:
    'diagnostics pack'
    """
    f = norm(f)
    if " - " in f:
        f = f.split(" - ", 1)[1]
    return f


# ------------------------------------------------------------------------------
# LISTA FEATURE ORACLE "OFICIALE"
# Exact ca in codul vechi (ordine si denumiri controlate)
# ------------------------------------------------------------------------------

KNOWN_FEATURES = [
    "diagnostics pack",
    "advanced compression",
    "tuning pack",
    "partitioning",
    "real application clusters",
    "active data guard",
    "potential use of diagnostics pack",
    "potential use of tuning pack",
    "golden gate",
    "real application testing"
]


# ------------------------------------------------------------------------------
# CLASA ORACLE
# Contine datele principale + setul de feature
# ------------------------------------------------------------------------------

class c_ORACLE:
    def __init__(self, nome):
        self.nome = nome
        self.data = {}        # campuri principale Oracle + HW
        self.features = set() # feature Oracle identificate


# ------------------------------------------------------------------------------
# CAMPI ORACLE DIN ICTG-0-database-oracle
# Ordinea este cea dorita in output
# ------------------------------------------------------------------------------


#aici am pus caimpuri care s-au gasit numa, nu-s in celea precedente
ORACLE_FIELDS = [
    "Nome computer",
    "Nome",
    "Versione",
    "Edizione",
    "Sistema operativo",
    "SID",
    "Tipo di computer",
    "Core partizione",
    "Stringa marchio processore",
    "Fattore core Oracle",
    "Processori logici",
    "Socket attivi del server"
]

FEATURE_FIELD = "Funzione"
HW_FIELDS = ["ambiente", "contratto", "cliente"]


# ------------------------------------------------------------------------------
# STRUCTURI DATE
# ------------------------------------------------------------------------------

Oracle = {}     # dictionar cu serverele Oracle
Hardware = {}   # dictionar cu datele HW


# ==============================================================================
# INCARCARE TABELLA_HW
# ==============================================================================

print(">>> Caricamento Tabella_HW") # ---> asa cum este in original 

hw_file = cm.dr.join([cm.out_path, cm.pr["OUT_Hardware_TAB"]])

with open(hw_file, encoding="utf-8") as f:
    # prima linie contine separatorele: sep=|
    first = f.readline()
    sep = first.strip().split("=")[1]

    reader = csv.DictReader(f, delimiter=sep)
    for row in reader:
        nome = norm(row.get("nome"))
        if nome:
            Hardware[nome] = row

print(f">>> Tabella_HW caricata: {len(Hardware)} record")


# ==============================================================================
# IDENTIFICARE CEL MAI RECENT FILE ORACLE ICTG
# ==============================================================================

print(">>> Ricerca file Oracle")

cm.list_files_scandir(
    cm.start_path,
    cm.pr["Oracle_Database_Pattern"],
    cm.pr["Extension_end"]
)

oracle_file = sorted(cm.files, reverse=True)[0]
print(">>> Elaborazione file:", oracle_file)


# ==============================================================================
# CITIRE FILE ORACLE (HEADER-BASED, ROBUST)
# ==============================================================================

with open(oracle_file, encoding="utf-8") as f:
    # detectare automata delimitator
    sample = f.read(2048)
    dialect = csv.Sniffer().sniff(sample) # trebuie, , ghiceste automat separator
    f.seek(0)

    reader = csv.DictReader(f, dialect=dialect)

    # mapa: header normalizat -> header real din fisier
    header_map = {}
    for h in reader.fieldnames:
        clean = h.replace("\ufeff", "")
        header_map[norm(clean)] = h

    # parcurgere randuri
    for i, row in enumerate(reader):
        print(f"\rElemento [{i}]", end="", flush=True)

        key_nome = header_map.get(norm("Nome computer"))
        if not key_nome:
            continue

        nome_raw = norm(row.get(key_nome))
        if not nome_raw:
            continue

        # elimina domeniul din hostname
        nome = cm.togli_dominio(nome_raw)[0]

        if nome not in Oracle:
            Oracle[nome] = c_ORACLE(nome)

        obj = Oracle[nome]

        # citire campuri principale Oracle
        for field in ORACLE_FIELDS:
            key = header_map.get(norm(field))
            obj.data[field] = row.get(key, "").strip() if key else ""

        # citire si normalizare feature Oracle
        key_funz = header_map.get(norm(FEATURE_FIELD))
        funzione_raw = row.get(key_funz, "") if key_funz else ""
        funzione = normalize_feature(funzione_raw)

        if funzione in KNOWN_FEATURES:
            obj.features.add(funzione)

print(f"\n>>> Record Oracle caricati: {len(Oracle)}")


# ==============================================================================
# MERGE DATE ORACLE CU TABELLA_HW
# ==============================================================================

for nome, obj in Oracle.items():
    if nome in Hardware:
        for f in HW_FIELDS:
            obj.data[f] = Hardware[nome].get(f, "-")
    else:
        for f in HW_FIELDS:
            obj.data[f] = "-"


# ==============================================================================
# CONSTRUCTIE HEADER OUTPUT
# Identic cu structura istorica
# ==============================================================================

HEADER = ORACLE_FIELDS + HW_FIELDS + KNOWN_FEATURES


# ==============================================================================
# SCRIERE FISIER OUTPUT Tabella_Oracle.csv
# ==============================================================================

output_file = cm.dr.join([cm.out_path, cm.pr["OUT_Oracle_TAB"]])

print("\n>>> Scrittura file:", output_file)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("sep=" + cm.cs + "\n")
    f.write(cm.cs.join(HEADER) + "\n")

    for nome in sorted(Oracle.keys()):
        obj = Oracle[nome]
        row = []

        for h in HEADER:
            if h in obj.data:
                row.append(obj.data[h])
            elif h in obj.features:
                row.append("X")
            else:
                row.append("")

        f.write(cm.cs.join(row) + "\n")

print("\n>>> ELABORAZIONE ORACLE COMPLETATA CON SUCCESSO")
