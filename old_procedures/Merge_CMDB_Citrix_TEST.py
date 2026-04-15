# -*- coding: utf-8 -*-
import Common as cm
import csv
import os


# !! nu se citesc coloanele VM_Cluster	VM_Virtualcenter	VM_Host	VMWare_LastReportDate


# ==============================================================-------------------------
class c_CMDB:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo  # listă cu 23 de elemente
        # lista con 23 elementi

# ==================================================================-----------
# CÂMPURI — 23 de câmpuri
# CAMPI — 23 campi
CMDB_field = {
    "Nome CI": 0, "OS": 1, "DNS": 2, "Domain Name": 3, "Is Virtual": 4,
    "Numero CPU": 5, "Numero Socket": 6, "Processore": 7, "Modello": 8,
    "VM_Cluster": 9, "VM_Virtualcenter": 10, "VM_Host": 11,
    "VMWare_LastReportDate": 12, "Bigfix_LastReportDate": 13,
    "Applicazione (lista)": 14, "Ruolo": 15, "Category": 16, "Type": 17,
    "Ambiente": 18, "Responsabile (Server)": 19, "Used By": 20, "Contratto": 21,
    "server_iscloud": 22
}

# ==============================================================
cm.check_outdir(cm.out_path)

# ==============================================================
# FUNCTIE PENTRU CITIRE SIGURĂ (SĂRIM PESTE sep=|)
# FUNZIONE PER LETTURA SICURA (SALTA "sep=|")
def load_csv_dict_safe(filepath, key_field):
    data = {}
    if not os.path.exists(filepath):
        print(f"File non trovato: {filepath}")
        return data

    print(f"\nCaricamento {os.path.basename(filepath)}...")
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("File vuoto.")
        return data

    # 1. Elimină sep=|
    # 1. Elimina "sep=|"
    if lines[0].strip().startswith("sep="):
        lines = lines[1:]

    # 2. Header
    # 2. Intestazione
    if not lines:
        print("Nessun header.")
        return data

    header_line = lines[0].strip()
    sep = ";" if ";" in header_line else "|" # --> era asa sep = "|" if "|" in header_line else ","
    fieldnames = [col.strip() for col in header_line.split(sep)]
    lines = lines[1:]  # sare peste header
    # salta l'intestazione

    # 3. Citește datele
    # 3. Legge i dati
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        values = [val.strip() for val in line.split(sep)]
        if len(values) < len(fieldnames):
            values += [""] * (len(fieldnames) - len(values))

        row = dict(zip(fieldnames, values))
        key = row.get(key_field, "").strip()
        if key:
            data[key.lower()] = row
        else:
            print(f"  Riga {i+2}: chiave mancante per {key_field}")

    print(f"Caricati {len(data)} record da {os.path.basename(filepath)}")
    return data

# ==============================================================
# 1. CITIRE AssetServer_CMDB.csv
# 1. LETTURA AssetServer_CMDB.csv
cmdb_path = cm.dr.join([cm.out_path, cm.pr["OUT_CMDB"]])
CMDB_Citrix = {}

cmdb_data = load_csv_dict_safe(cmdb_path, "Nome CI")
for nome, row in cmdb_data.items():
    dati = [""] * len(CMDB_field)
    for field, idx in CMDB_field.items():
        dati[idx] = row.get(field, "")
    CMDB_Citrix[nome] = c_CMDB(nome, dati)

# 2. CITIRE Server_Citrix_list.csv
# 2. LETTURA Server_Citrix_list.csv
server_path = cm.dr.join([cm.out_path, cm.pr["OUT_Server_Citrix"]])
if os.path.exists(server_path):
    server_data = load_csv_dict_safe(server_path, "name")  # PRESUPUNEM că prima coloană este "Name"
    # SI PRESUME che la prima colonna sia "Name"
    for nome_raw, row in server_data.items():
        nome = nome_raw.lower()
        if nome not in CMDB_Citrix:
            dati = [""] * len(CMDB_field)
            obj = c_CMDB(nome, dati)
            CMDB_Citrix[nome] = obj
        else:
            obj = CMDB_Citrix[nome]

        obj.dati[0] = nome_raw
        obj.dati[CMDB_field["Numero CPU"]] = row.get("cpus", "")
        obj.dati[CMDB_field["Ambiente"]] = row.get("pool", "")
        obj.dati[CMDB_field["VM_Cluster"]] = row.get("pool", "") 

        # Valori implicite
        # Valori predefiniti
        obj.dati[CMDB_field["Used By"]] = "CEDACRI"
        obj.dati[CMDB_field["server_iscloud"]] = "0"
        obj.dati[CMDB_field["Is Virtual"]] = "NO"
        obj.dati[CMDB_field["OS"]] = "XenServer Type"
        obj.dati[CMDB_field["Type"]] = "Server"
        obj.dati[CMDB_field["Category"]] = "Server"
        obj.dati[CMDB_field["Ruolo"]] = "CITRIX"
        obj.dati[CMDB_field["Contratto"]] = "MS SPLA"

# 3. CITIRE Vms_Citrix_list.csv
# 3. LETTURA Vms_Citrix_list.csv
vms_path = cm.dr.join([cm.out_path, cm.pr["OUT_Vms_Citrix"]])
if os.path.exists(vms_path):
    vms_data = load_csv_dict_safe(vms_path, "name")  # PRESUPUNEM că prima coloană este "Name"
    # SI PRESUME che la prima colonna sia "Name"
    for nome_raw, row in vms_data.items():
        nome = nome_raw.lower()
        if nome not in CMDB_Citrix:
            dati = [""] * len(CMDB_field)
            obj = c_CMDB(nome, dati)
            CMDB_Citrix[nome] = obj
        else:
            obj = CMDB_Citrix[nome]

        obj.dati[0] = nome_raw
        obj.dati[CMDB_field["Numero CPU"]] = row.get("cpus", "")
        obj.dati[CMDB_field["Ambiente"]] = row.get("pool", "")
        obj.dati[CMDB_field["OS"]] = row.get("operating_system", "") # -- era OS
        obj.dati[CMDB_field["VM_Cluster"]] = row.get("pool", "")
        obj.dati[CMDB_field["VM_Host"]] = row.get("running_on", "")

        # Valori implicite
        # Valori predefiniti
        obj.dati[CMDB_field["Used By"]] = "CEDACRI"
        obj.dati[CMDB_field["server_iscloud"]] = "0"
        obj.dati[CMDB_field["Is Virtual"]] = "SI"
        obj.dati[CMDB_field["Type"]] = "Server"
        obj.dati[CMDB_field["Category"]] = "Server"
        obj.dati[CMDB_field["Ruolo"]] = "CITRIX"
        obj.dati[CMDB_field["Contratto"]] = "MS SPLA"

# ==============================================================
# SCRIERE
# SCRITTURA
output_path = cm.dr.join([cm.out_path, cm.pr["OUT_CMDB_Citrix"]])
print(f"\nScrittura file {output_path} ({len(CMDB_Citrix)} righe)")
# Stampa del file di output

with open(output_path, "w", encoding="utf-8", newline='') as f:
    f.write("sep=|\n")
    f.write("|".join(CMDB_field.keys()) + "\n")
    j = 0
    for nome in sorted(CMDB_Citrix.keys()):
        obj = CMDB_Citrix[nome]
        print('\r', f"Scrittura [{j}]", end='', flush=True)
        row = [obj.dati[i] if i < len(obj.dati) else "" for i in range(len(CMDB_field))]
        f.write("|".join(map(str, row)) + "\n")
        j += 1

print(f"\nCompletato: {output_path}")
print(f"Totale server: {len(CMDB_Citrix)}")
# Completato e conteggio finale dei server
