# Python - Elabora_SW - varianta cu DictReader (2025/2026 compatibilă)

import csv
import Common as cm


# s-a luat din elabora_HW mai nou, care elimina spatiile invizibile + schimbarea standadtrelor
# logica tratta dalla più recente procedura elabora_HW,
# che rimuove gli spazi invisibili e normalizza i formati
# tratta dalla più recente elabora_HW, che rimuove gli spazi invisibili e modifica gli standard

# ───────────────────────────────────────────────
# Normalizare texte (fără BOM, spații inutile)
# ───────────────────────────────────────────────
def norm(s, lower=False):
    if s is None:
        return ""
    s = s.replace("\ufeff", "").strip()
    return s.lower() if lower else s

# ───────────────────────────────────────────────
# Clase (neschimbate)
# ───────────────────────────────────────────────
class AssetSW:
    def __init__(self, dati):
        self.datisw = dati

class c_TABSW:
    def __init__(self, nume, dati):
        self.nome = nume
        self.datihw = dati
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))

class c_BGFXSW:
    def __init__(self, nume):
        self.nome = nume
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))

class c_CMDBSW:
    def __init__(self, nume):
        self.nome = nume
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))

# ───────────────────────────────────────────────
# calcolo edition --non cambiato
# Calcul ediție (neschimbat)
# ───────────────────────────────────────────────
def calcola_edizione(dati_sw):
    nome_componente = dati_sw[1]
    y = nome_componente.split(" ")

    # SQL Server
    if 'sql server' in nome_componente.lower() and 'edition' in nome_componente.lower():
        z = cm.cerca_elemento(y, 'edition', 0, 1, -1)
        if z >= 0:
            ediz_nome = y[z - 1]
            if z - 2 >= 0 and y[z - 2].lower() == 'r2':
                ediz_vers = y[z - 3] + ' ' + y[z - 2] if z - 3 >= 0 else y[z - 2]
            else:
                ediz_vers = y[z - 2] if z - 2 >= 0 else '-'
            return ediz_nome.strip(), ediz_vers.strip()

    # Office / 365
    if 'office' in nome_componente.lower():
        ultimo = len(y) - 1
        if cm.cerca_elemento(y, '365', 0, 1, -1) > -1:
            if cm.cerca_elemento(y, 'proplus', 0, 1, -1) > -1:
                return "Professional Plus", "365"
            else:
                return y[ultimo], "365"
        elif cm.cerca_elemento(y, 'professional plus', 0, 1, -1) > -1:
            return "Professional Plus", y[ultimo]
        elif cm.cerca_elemento(y, '2003', 0, 1, -1) > -1:
            return y[ultimo], "2003"
        else:
            return y[ultimo-1] if ultimo-1 >= 0 else '-', y[ultimo] if ultimo >= 0 else '-'

    return '-', '-'

# ───────────────────────────────────────────────
# dtruttura finala SW (50 colonne)
# Structura finală SW (50 coloane)
# ───────────────────────────────────────────────
SW_field = [
    "nome", "operating_system", "dominio", "dns_name", "virtuale", "tipo",
    "cluster_name", "cluster_ambiente", "cluster_cliente", "cluster_destinazione",
    "cluster_cores", "cluster_numhosts", "cluster_n_vms_total", "cluster_n_vms", 
    "cluster_n_vms_win", "hyperthreadactive", "ha_enabled", "drs_enabled", "host",
    "vm_hw_version", "n_cpu", "n_core", "pvu_per_core", "valore_pvu_modificato",
    "valore_pvu_predefinito", "fattore_core_oracle", "powerstate", "vcenter",
    "vcenter_cores", "vcenter_hosts", "vcenter_dominio", "vcenter_cluster",
    "cpu_model", "applicazione", "ruolo", "ambiente", "responsabile", "cliente",
    "contratto", "sito",
    "nome publisher", "nome componente", "versione_componente", 
    "versione dettagliata componente", "percorso_di_installazione", 
    "nome prodotto", "versione_prodotto", "metrica", "nome_edizione", 
    "versione_edizione"
]

#v  ordine fisso per i 10 campi software (usato ovunque nel codice)
# Ordine fixă pentru cele 10 câmpuri SW (folosim această ordine peste tot)
SW_ORDER = [
    "nome publisher",
    "nome componente",
    "versione_componente",
    "versione dettagliata componente",
    "percorso_di_installazione",
    "nome prodotto",
    "versione_prodotto",
    "metrica",
    "nome_edizione",       # calculat mai târziu
    "versione_edizione"    # calculat mai târziu
]

# ───────────────────────────────────────────────
# inizializzazione dei dizionari principali
# Inițializare dicționare
# ───────────────────────────────────────────────
Software = {}
BGFXSW   = {}
CMDBSW   = {}

# ───────────────────────────────────────────────
# 1. Încărcare Hardware (neschimbat)
# ───────────────────────────────────────────────
print("Caricare date Hardware...")
cm.check_outdir(cm.out_path)
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_Hardware_TAB"]])
Hardware = {}
cm.carica_dati(input_file, Hardware, 0)

# ───────────────────────────────────────────────
# 2. Listări excludere (neschimbat)
# ───────────────────────────────────────────────
mcrsft_kywrd_2_xcld = []; mcrsft_nomi_2_xcld = []
ibm_kywrd_2_xcld    = []; ibm_nomi_2_xcld    = []
vmwr_kywrd_2_xcld   = []; vmwr_nomi_2_xcld   = []
orcl_nomi_2_xcld    = []
rdht_nomi_2_xcld    = []

def carica_lista(file_name, lista):
    try:
        input_file = cm.dr.join([cm.exc_path, file_name])
        with open(input_file, 'r', encoding='utf-8') as fc:
            for line in fc:
                lista.append(line.strip())
    except FileNotFoundError:
        print(f"  Fișier {file_name} nu există - continuă...")
        print(f"  File {file_name} non esista - continua...")

carica_lista("Microsoft_keyword.csv", mcrsft_kywrd_2_xcld)
carica_lista("Microsoft_nomi.csv",     mcrsft_nomi_2_xcld)
carica_lista("IBM_keyword.csv",        ibm_kywrd_2_xcld)
carica_lista("IBM_nomi.csv",           ibm_nomi_2_xcld)
carica_lista("VMware_keyword.csv",     vmwr_kywrd_2_xcld)
carica_lista("VMware_nomi.csv",        vmwr_nomi_2_xcld)
carica_lista("Oracle_nomi.csv",        orcl_nomi_2_xcld)
carica_lista("RedHat_nomi.csv",        rdht_nomi_2_xcld)

# ───────────────────────────────────────────────
# 3. Procesare BGFX SW cu DictReader
# ───────────────────────────────────────────────
print("\nElaborare BGFXSW...")
file_pattern = cm.pr["BFGX_SW_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)

if not temp:
    print("→ Niciun fișier BGFX_SW găsit -- Nessun file BGFX_SW non ha trovato!")
else:
    file_path = temp[0]
    print(f"→ Procesez: {file_path}")

    with open(file_path, "r", encoding="utf-8-sig", errors="replace") as f:
        pos = f.tell()
        first = f.readline().rstrip("\n")
        delimiter = "|"
        if first.lower().startswith("sep="):
            delimiter = first.split("=", 1)[1].strip("'\"")
            print(f"   Separator detectat: '{delimiter}'")
        else:
            f.seek(pos)

        reader = csv.DictReader(f, delimiter=delimiter)
        # Normalizăm header-ele
        reader.fieldnames = [norm(h) for h in reader.fieldnames if h is not None]

        print("Header BGFX_SW:", ", ".join(reader.fieldnames[:10]) + "...")

        row_count = 0
        kept_count = 0

        for row in reader:
            row_count += 1
            # row curat cu chei normalizate
            clean = {norm(k): (v.strip() if v else "") for k, v in row.items() if k is not None}
           
            # un fel de debug
            #print("CHEI REALE BGFX:", list(clean.keys()))
            #break

            publisher = norm(clean.get("nome publisher", ""), lower=True)
            prodotto  = clean.get("nome prodotto", "").strip()

            if not publisher or cm.cerca_elemento(cm.pr["Vendor"], publisher, -1, 1, -1) < 0:
                continue

            # Excluderi cunoscute
            exclude = False
            if publisher == "microsoft":
                if (cm.cerca_elemento(mcrsft_kywrd_2_xcld, prodotto, -1,1,-1) > -1 or
                    cm.cerca_elemento(mcrsft_nomi_2_xcld,   prodotto, -1,1,-1) > -1):
                    exclude = True
            elif publisher in ("ibm", "oracle", "vmware", "red hat"):
                # adaugă logica similară pentru ceilalți vendor dacă există liste
                pass

            if exclude:
                continue

            # Construim lista în ordine fixă
            sw_line = []

            # debug ca sa vedem metrica
            # print("METRICA:", sw_line[7])



            for col in SW_ORDER[:8]:  # primele 8 vin din fișier
                val = clean.get(col, "")
                sw_line.append(norm(val, lower=True) if col != "nome prodotto" else val.lower())

  

            sw_line.extend(["-", "-"])  # edițiile se calculează mai târziu
            
            # DEBUG metrica
            if kept_count < 20:
                print("PRODOTTO:", sw_line[5], "| METRICA:", sw_line[7])

                
            computer = norm(clean.get("nome computer", ""), lower=True)
            if not computer:
                continue

            if computer not in BGFXSW:
                BGFXSW[computer] = c_BGFXSW(computer)

            BGFXSW[computer].software(sw_line)
            kept_count += 1

        print(f"   Total rânduri: {row_count:,} → păstrate după filtre: {kept_count:,}")

# ───────────────────────────────────────────────
# 4. Procesare CMDB SW cu DictReader
# ───────────────────────────────────────────────
print("\nElaborare CMDBSW...")
cm.files = []
file_pattern = cm.pr["CMDB_SW_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

if not cm.files:
    print("→ Niciun fișier CMDB_SW găsit")
else:
    file_path = sorted(cm.files, reverse=True)[0]
    print(f"→ Procesez: {file_path}")

    with open(file_path, "r", encoding="utf-8-sig", errors="replace") as f:
        pos = f.tell()
        first = f.readline().rstrip("\n")
        delimiter = ","
        if first.lower().startswith("sep="):
            delimiter = first.split("=", 1)[1].strip("'\"")
        else:
            f.seek(pos)

        reader = csv.DictReader(f, delimiter=delimiter)
        reader.fieldnames = [norm(h) for h in reader.fieldnames if h is not None]

        print("Header CMDB_SW:", ", ".join(reader.fieldnames[:8]) + "...")

        row_count = 0
        kept_count = 0

        for row in reader:
            row_count += 1
            clean = {norm(k): (v.strip() if v else "") for k, v in row.items() if k is not None}

            publisher = norm(clean.get("manufacturer_name_", ""), lower=True)
            if not publisher or cm.cerca_elemento(cm.pr["Vendor"], publisher, -1, 1, -1) < 0:
                continue

            software_name = clean.get("software", "").strip()

            sw_line = [
                publisher,
                norm(software_name, True),
                norm(clean.get("version_number", ""), True),
                "-", "-",                        # detaliat + path
                norm(software_name, True),
                norm(clean.get("version_number", ""), True),
                "-",                             # metrica
                "-", "-"                         # ediții
            ]

            server = norm(clean.get("server", ""), lower=True)
            if not server:
                continue

            if server not in CMDBSW:
                CMDBSW[server] = c_CMDBSW(server)

            CMDBSW[server].software(sw_line)
            kept_count += 1

        print(f"   Total rânduri: {row_count:,} → păstrate după filtre: {kept_count:,}")

# ───────────────────────────────────────────────
# 5. Combinare HW + SW + calcul ediții
# ───────────────────────────────────────────────
print("\nCombinare HW + SW...")

for nume in Hardware:
    Software[nume] = c_TABSW(nume, Hardware[nume])

for nume in list(Software.keys()):
    if nume in BGFXSW:
        for asset in BGFXSW[nume].sw:
            ed_n, ed_v = calcola_edizione(asset.datisw)
            asset.datisw[8]  = ed_n
            asset.datisw[9]  = ed_v
            Software[nume].software(asset.datisw[:])

    if nume in CMDBSW:
        for asset in CMDBSW[nume].sw:
            ed_n, ed_v = calcola_edizione(asset.datisw)
            asset.datisw[8]  = ed_n
            asset.datisw[9]  = ed_v
            Software[nume].software(asset.datisw[:])

# ───────────────────────────────────────────────
# 6. Scriere finală
# ───────────────────────────────────────────────
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_Software_TAB"]])
print("\n=== DIAGNOSTIC ===")
print(f"Servere în Hardware   : {len(Hardware):>6}")
print(f"Servere cu BGFX SW    : {len(BGFXSW):>6}")
print(f"Servere cu CMDB SW    : {len(CMDBSW):>6}")

comune_bgfx = set(Hardware.keys()) & set(BGFXSW.keys())
comune_cmdb = set(Hardware.keys()) & set(CMDBSW.keys())

print(f"Servere comune Hardware ↔ BGFX : {len(comune_bgfx):>6}")
print(f"Servere comune Hardware ↔ CMDB : {len(comune_cmdb):>6}")

if comune_bgfx:
    print("Exemple comune BGFX:", list(comune_bgfx)[:3])
if comune_cmdb:
    print("Exemple comune CMDB:", list(comune_cmdb)[:3])

total_sw = sum(len(s.sw) for s in Software.values())
print(f"Total intrări software scrise : {total_sw:>6}")
print("===================\n")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("sep=|\n")
    f.write("|".join(SW_field) + "\n")

    for nume in Software:
        hw = Software[nume].datihw
        for sw_asset in Software[nume].sw:
            line = hw + sw_asset.datisw
            f.write("|".join(map(str, line)) + "\n")

print("\n+───────────────────────────────────────────────+")
print(f"  Procedura Elabora_SW → {output_file}")
print(f"  Servere: {len(Software):,}   Software total: {sum(len(s.sw) for s in Software.values()):,}")
print("+───────────────────────────────────────────────+")