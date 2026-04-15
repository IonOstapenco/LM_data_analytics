import csv
import Common as cm


# Integrazione di tre procedure "Extract_columns" in una sola funzione
#3 in one, s-a integrat procedurele Extract_columns in 1, cu functie

# ----------------------------------------------------------
# normalizzazione del testo (BOM + spazi) utilizzata in tutte le procedure Extract_columns_asset
# normalizare   text (BOM + spatii) (este in toate Extract_columns _asset)  --: n
# !!nota-- : de incluis in exercitii
# --------------------------------------------------------------------------
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()

# ---------------------------------------------
# funzione/metodo generico per la processazione dei file asset
# functie/metoda  pentru procesare fissiere
# --------------------------------------------------------------------------
def process_asset(name_class, fieldnames, file_pattern, main_field, output_file):
    
    # classe generica utilizzata per memorizzare i record letti dal file
    # clasa generica pentru memorarea unui record
    class c_generic:
        def __init__(self, nome, dati):  # ca in java -- equals and hash code
            self.nome = nome
            self.dati = dati

# ===============================================================================================
#  --------------------------  2.A   PREGATIRI INiTIALE -------------------
# =================================================================================================
    data = [] # --- > cream lista "data", unde se vor salva inregistrarile

    # verifica / crea cartella output
    # verificam daca exista directorul de output
    cm.check_outdir(cm.out_path)

    # pulizia lista dei file trovati
    # golim lista de fisiere gasite anterior
    cm.files.clear()

    # ricerca file secondo pattern configurato dopo Parametri.json
    # cautam fisiere conform patternului configuratm dupa standartul de la Parametri.json
    cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

# ===================================================================================================
# -------------- Alegerea fisierului cel mai recent ------------------------------------------

# ====================================================================================================
    # ordiniamo i file per data (decrescente)
    # sortam fisierele descrescator
    temp = sorted(cm.files, reverse=True)

    if not temp:
        raise FileNotFoundError(f"Nu exista fisier {name_class}!")
    #  Scop: să știe ce coloane există și cum sunt separate.
    # prendiamo il file più recente
    # luam fisierul cel mai recent
    input_file = temp[0]
       #•	Sortează fișierele descrescător (cel mai nou primul). 
        #•	Lua fișierul cel mai recent pentru procesare. 

    print(f"Elaborare {name_class}:", input_file)

    with open(input_file, "r", encoding="utf-8") as f:

        # delimitatore default
        # delimiter implicit
        delimiter = cm.cs  # --> Detectarea header-ului și separatorului
        header_line = None

        # ricerca dinamica dell'header nel file
        # cautare dinamica a headerului in fisier
        while True:
            pos = f.tell()
            line = f.readline()
            if not line:
                break

            # rimuoviamo eventuale BOM
            # stergem unde se gaseste BOM
            clean = line.replace("\ufeff", "").strip()

            # rilevamento separatore (es: sep=|)
            # detectare separator
            if clean.lower().startswith("sep="):
                delimiter = clean.split("=")[1]
                continue

            # identificazione riga header
            # identificare linia de header
            if main_field.lower() in clean.lower():
                header_line = clean
                f.seek(pos)
                break

        # se header non trovato -> errore
        # daca headerul nu a fost gasit -> eroare
        if not header_line:
            raise RuntimeError(f"Header {name_class} nu a fost gasit!")
        # ---------------------------------------------------------------------------------------
        # -- Citirea fișierului CSV ------------------------
        # ---------------------------------------------------------------------------------------
        # lettura CSV tramite DictReader
        # citire fisier CSV cu DictReader
        reader = csv.DictReader(f, delimiter=delimiter)

        # normalizzazione header (rimozione BOM/spazi)
        # normalizare header
        reader.fieldnames = [norm(h) for h in reader.fieldnames]

        # stampa header per debug
        # este un oarecare debug
        print("Header detectat:", reader.fieldnames)

        # -----------------------------------------------------------------
        # -- PRELUCRAREA RANDURILOR  CSV
        # ----------------------------------------------------------------------
        #•	Normalizează cheile rândurilor. 
        #•	Extrage main_field ca și cheie principală (nome). 
        #•	Creează obiect c_generic pentru fiecare rând și îl adaugă în listă. 
        #•	În data ajunge doar rândul procesat pentru coloanele definite în fieldnames. 

        # -------------------------------------------------------------
        for row in reader:


            # normalizziamo anche le chiavi delle righe
            # normalizam si cheile din rand
            row = {norm(k): v for k, v in row.items() if k is not None}

            # chiave principale (hostname / server)
            # cheia principala
            nome = row.get(main_field, "").strip().lower()

            if not nome:
                continue

            # salvare record nella lista
            # salvam recordul
            data.append(c_generic(
                nome,
                [nome if field == main_field else row.get(field, "") for field in fieldnames]
            ))

    print(f"Record {name_class} citite:", len(data))


    # utilizziamo separatore configurato per output
    # folosim separatorul configurat pentru output
    #!! modificat 12/02/26 -- separator pentru output, cu out_sep!!
    out_sep = cm.cs

    # scrittura file output
    # scriem fisierul de output
    out_path_file = cm.dr.join([cm.out_path, output_file])
    print("Scriere output:", out_path_file)

    with open(out_path_file, "w", encoding="utf-8", newline="") as f:
        f.write("sep=" + out_sep + "\n")
        f.write(out_sep.join(fieldnames) + "\n")

        for obj in data:
            f.write(out_sep.join(map(str, obj.dati)) + "\n")

    print(f"{name_class} finalizat \n")

    return data


# ----------------------------------------------------------------------------------------
# configurazione dei campi e dei file di input
# Configurare la campuri asi files
# ----------------------------------------------------------------------------------
CMDB_field = ["Nome CI","OS","DNS","Domain Name","Is Virtual","Numero CPU","Numero Socket",
              "Processore","Modello","VM_Cluster","VM_Virtualcenter","VM_Host",
              "VMWare_LastReportDate","Bigfix_LastReportDate","Applicazioni (lista)",
              "Ruolo","Category","Type","Ambiente","Responsabile (Server)",
              "Used By","Contratto","server_iscloud","Ip_primary"] # --> din asset server (all)

DISS_field = ["server","datadismissione"] # din asset server dismessi

PDL_field = ["Nome CI","Category","Type","Domain Name","Used By"] # din asset client


# -------------------------------------------------------------
# elaborazione dati CMDB
# prelucram pe toate
# -----------------------------------------------------------------
CMDB_data = process_asset("CMDB", CMDB_field, cm.pr["CMDB_Pattern"], "Nome CI", cm.pr["OUT_CMDB"])



# =================================================================================

# Generarea listei ESX --> OUT_CMDB_ESX  (AssetCMDB_Esx.csv)

# ==========================================================================

# -------------------------------------------------------------
# generazione file OUT_CMDB_ESX (senza modificare OUT_CMDB)
# Generare OUT_CMDB_ESX (fara a modifica OUT_CMDB)
# -------------------------------------------------------------
print("Generare lista ESX...")

CMDB_ESX_data = []

for obj in CMDB_data:

    # individuiamo gli indici dei campi necessari
    # gasim indexurile necesare
    try:
        idx_ruolo = CMDB_field.index("Ruolo")
        idx_cpu = CMDB_field.index("Numero CPU")
        idx_socket = CMDB_field.index("Numero Socket")
    except ValueError:
        continue

    ruolo = str(obj.dati[idx_ruolo]).lower()

    # consideriamo solo server ESX
    # doar ESX
    if not ruolo.startswith("esx"):
        continue

    # copia lista per evitare modifica dell'originale
    # copiem lista ca sa nu modificam originalul
    dati_esx = obj.dati.copy()

    # scambio valori CPU -> Socket
    # swap CPU -> Socket
    old_cpu = dati_esx[idx_cpu]
    dati_esx[idx_socket] = old_cpu

    # CPU diventa server_numerocore se esiste in CMDB originale
    # CPU devine server_numerocore daca exista in CMDB original
    # (in varianta DictReader nu l-am inclus in field list)
    # daca nu exista, ramane gol
    dati_esx[idx_cpu] = ""

    CMDB_ESX_data.append(type(obj)(obj.nome, dati_esx))


# -------------------------------------------------------------
# scrittura file OUT_CMDB_ESX
# Scriere fisier OUT_CMDB_ESX
# -------------------------------------------------------------
out_esx_path = cm.dr.join([cm.out_path, cm.pr["OUT_CMDB_ESX"]])
print("Scriere output ESX:", out_esx_path)

with open(out_esx_path, "w", encoding="utf-8", newline="") as f:
    f.write("sep=" + cm.cs + "\n")
    f.write(cm.cs.join(CMDB_field) + "\n")

    for obj in CMDB_ESX_data:
        f.write(cm.cs.join(map(str, obj.dati)) + "\n")

print("OUT_CMDB_ESX finalizat \n")


# ===============================================================================================

# ------------      PROCESAREA DISS(din Asset Server Dismessi) SI PDL (din Asset Client)

# ================================================================================================

# --------------------------------------------------------------------
# elaborazione dati server dismessi
# prelucrare servere dismise
# --------------------------------------------------------------------
DISS_data = process_asset("DISS", DISS_field, cm.pr["DISMESSI_Pattern"], "server", cm.pr["OUT_DISMESSI"])


# --------------------------------------------------------------------
# elaborazione dati PDL
# prelucrare date PDL
# --------------------------------------------------------------------
PDL_data = process_asset("PDL", PDL_field, cm.pr["PDL_Pattern"], "Nome CI", cm.pr["OUT_PDL"])