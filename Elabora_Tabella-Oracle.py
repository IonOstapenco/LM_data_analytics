# ==============================================================================
# ELABORA_ORACLE_FINAL
# Procedura robusta, bazata pe header (nu pe pozitii)
# Output identic logic cu cel obtinut de codul vechi
#
# Procedura robusta basata sugli header (non sulle posizioni)
# Output logicamente identico a quello ottenuto dal codice precedente
# ==============================================================================

import csv
import unicodedata
import Common as cm


# ------------------------------------------------------------------------------
# FUNCTII DE NORMALIZARE STRINGHE
# Funzioni per la normalizzazione delle stringhe
# ------------------------------------------------------------------------------

def norm(s): # --> functia normalizeaza rand, dar si sterge spatii
    """
    Normalizeaza o stringa:
    - elimina BOM
    - lower case
    - elimina spatii
    - elimina accente (unicode)

    Normalizza una stringa:
    - rimuove il BOM
    - converte in minuscolo
    - rimuove spazi iniziali/finali
    - rimuove accenti (unicode)
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

    Replica il comportamento del codice precedente:
    'Oracle Database Licensable Option - Diagnostics Pack'
    diventa:
    'diagnostics pack'
    """
    f = norm(f)
    if " - " in f:
        f = f.split(" - ", 1)[1]
    return f


# ------------------------------------------------------------------------------
# LISTA FEATURE ORACLE "OFICIALE"
# Lista delle feature Oracle "ufficiali"
#
# Exact ca in codul vechi (ordine si denumiri controlate)
# Esattamente come nel codice precedente (ordine e nomi controllati)
# ------------------------------------------------------------------------------

Funzioni = [
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
# Classe che rappresenta un server Oracle
#
# Contine datele principale + setul de feature
# Contiene i dati principali + il set di feature Oracle
# ------------------------------------------------------------------------------

class c_ORACLE:
    def __init__(self, nome):
        self.nome = nome
        self.data = {}        # campuri principale Oracle + HW
                              # campi principali Oracle + dati Hardware
        self.features = set() # feature Oracle identificate
                              # insieme delle feature Oracle identificate


# ------------------------------------------------------------------------------
# CAMPI ORACLE DIN ICTG-0-database-oracle
# Campi Oracle provenienti dal file ICTG-0-database-oracle
#
# Ordinea este cea dorita in output
# L'ordine è quello desiderato nell'output
# ------------------------------------------------------------------------------


#aici am pus caimpuri care s-au gasit numa, nu-s in celea precedente
# qui sono stati inseriti solo i campi trovati nel file attuale
Oracle_Field = [ # ---> BGFX_FIELD
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


# de modificat inapoi denumiri la variabile!!
# probabilmente bisogna ripristinare i nomi originali delle variabili

Funzione_Field = "Funzione"
HW_field = ["ambiente", "contratto", "cliente"]


# ------------------------------------------------------------------------------
# STRUCTURI DATE
# Strutture dati utilizzate nella procedura
# ------------------------------------------------------------------------------

Oracle = {}     # dictionar cu serverele Oracle
                # dizionario con i server Oracle
Hardware = {}   # dictionar cu datele HW
                # dizionario con i dati Hardware


# ==============================================================================
# INCARCARE TABELLA_HW
# Caricamento della Tabella_HW
# ==============================================================================

print(">>> Caricamento Tabella_HW") # ---> asa cum este in original 

hw_file = cm.dr.join([cm.out_path, cm.pr["OUT_Hardware_TAB"]])

with open(hw_file, encoding="utf-8") as f:
    # prima linie contine separatorele: sep=|
    # la prima riga contiene il separatore: sep=|
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
# Identificazione del file Oracle ICTG più recente
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
# Lettura del file Oracle basata sugli header (robusta)
# ==============================================================================

with open(oracle_file, encoding="utf-8") as f:
    # detectare automata delimitator
    # rilevamento automatico del delimitatore
    sample = f.read(2048)
    dialect = csv.Sniffer().sniff(sample) # trebuie, , ghiceste automat separator
                                          # rileva automaticamente il separatore
    f.seek(0)

    reader = csv.DictReader(f, dialect=dialect)

    # mapa: header normalizat -> header real din fisier
    # mappa: header normalizzato -> header reale nel file
    header_map = {}
    for h in reader.fieldnames:
        clean = h.replace("\ufeff", "")
        header_map[norm(clean)] = h

    # parcurgere randuri
    # iterazione delle righe del file
    for i, row in enumerate(reader):
        print(f"\rElemento [{i}]", end="", flush=True)

        key_nome = header_map.get(norm("Nome computer"))
        if not key_nome:
            continue

        nome_raw = norm(row.get(key_nome))
        if not nome_raw:
            continue

        # elimina domeniul din hostname
        # rimuove il dominio dall'hostname
        nome = cm.togli_dominio(nome_raw)[0]

        if nome not in Oracle:
            Oracle[nome] = c_ORACLE(nome)

        obj = Oracle[nome]

        # citire campuri principale Oracle
        # lettura dei campi principali Oracle
        for field in Oracle_Field:
            key = header_map.get(norm(field))
            obj.data[field] = row.get(key, "").strip() if key else ""

        # citire si normalizare feature Oracle
        # lettura e normalizzazione delle feature Oracle
        key_funz = header_map.get(norm(Funzione_Field))
        funzione_raw = row.get(key_funz, "") if key_funz else ""
        funzione = normalize_feature(funzione_raw)

        if funzione in Funzioni:
            obj.features.add(funzione)

print(f"\n>>> Record Oracle caricati: {len(Oracle)}")


# ==============================================================================
# MERGE DATE ORACLE CU TABELLA_HW
# Merge dei dati Oracle con la Tabella_HW
# ==============================================================================

for nome, obj in Oracle.items():
    if nome in Hardware:
        for f in HW_field:
            obj.data[f] = Hardware[nome].get(f, "-")
    else:
        for f in HW_field:
            obj.data[f] = "-"


# ==============================================================================
# CONSTRUCTIE HEADER OUTPUT
# Costruzione dell'header dell'output
#
# Identic cu structura istorica
# Identico alla struttura storica
# ==============================================================================

HEADER = Oracle_Field + HW_field + Funzioni


# ==============================================================================
# SCRIERE FISIER OUTPUT Tabella_Oracle.csv
# Scrittura del file di output Tabella_Oracle.csv
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