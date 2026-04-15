# -*- coding: utf-8 -*- 
import Common as cm
import csv
import os

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Classi per i dati
class c_CMDB:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

class c_DISS:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

class c_PDL:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Definizione dizionari campi
CMDB_field = {
    "Nome CI": 0,
    "OS": 7,
    "DNS": 30,
    "Domain Name": 12,
    "Is Virtual": 27,
    "Numero CPU": 15,
    "Numero Socket": 14,
    "Processore": 16,
    "Modello": 26,
    "VM_Cluster": 19,
    "VM_Virtualcenter": 24,
    "VM_Host": 21,
    "VMWare_LastReportDate": 20,
    "Bigfix_LastReportDate": 31,
    "Applicazione (lista)": 8,
    "Ruolo": 5,
    "Category": 2,
    "Type": 3,
    "Ambiente": 6,
    "Responsabile": 9,
    "Used By": 38,
    "Contratto": 39,
    "server_iscloud": 33,
    "Ip_primary": 40
}

DISS_field = {"server": 0, "datadismissione": 2}

# PDL_field sarà impostato dinamicamente dall’header
PDL_field = {"Nome CI": 0, "Category": 2, "Type": 3, "Domain Name": 7, "Used By": 19}

# Liste oggetti
CMDB = []
CMDB_esx = []
DISS = []
PDL = []

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Creazione cartella di output
cm.check_outdir(cm.out_path)

# --- Ricerca del file CMDB
cm.files.clear()
file_pattern = cm.pr["CMDB_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)
input_file = temp[0]
print("Elaborazione file " + input_file)

nomi = []
i = 0
mesg = "Elemento [{}]"

# --- File speciale / standard
special_file = "Asset Client (ALL)-data-2025-10-20 10_08_21.csv"

# Se il file è speciale, utilizziamo DictReader
if os.path.basename(input_file) == special_file:
    print("⚙️ File speciale rilevato – si applica il metodo DictReader")
    with open(input_file, "r", encoding="utf-8") as fc:
        reader = csv.DictReader(fc, delimiter=",")
        for row in reader:
            print('\r', mesg.format(i), end='', flush=True)
            nome = str(row.get("Nome CI", "")).lower()
            if not nome or nome in nomi:
                continue
            nomi.append(nome)
            
            s_ruolo = str(row.get("Ruolo", "")).lower()
            if s_ruolo.startswith("appliance"):
                continue
            
            is_esx = 1 if s_ruolo.startswith("esx") else 0
            
            # Costruzione lista nell’ordine dei campi
            t = []
            for c in CMDB_field:
                if c == "Nome CI":
                    t.append(nome)
                else:
                    t.append(row.get(c, ""))
            
            z = c_CMDB(nome, t)
            
            if is_esx:
                if len(z.dati) > 6:
                    z.dati[6] = z.dati[5]
                if "server_numerocore" in row and len(z.dati) > 5:
                    z.dati[5] = row.get("server_numerocore", "")
                CMDB_esx.append(z)
            
            CMDB.append(z)
            i += 1

# Per i file standard
else:
    print("📄 File standard – si applica il metodo originale")
    with open(input_file, "r", encoding="utf-8") as fc:
        for x in fc:
            print('\r', mesg.format(i), end='', flush=True)
            if i < 2:
                i += 1
                continue
            
            separa = cm.trova_separa(x)
            tmp = cm.togli_apici(x, separa)
            y = tmp.split(cm.cs)
            
            s_ruolo = str(y[CMDB_field["Ruolo"]]).lower() if len(y) > CMDB_field["Ruolo"] else ""
            if s_ruolo.startswith("appliance"):
                i += 1
                continue
            
            is_esx = 1 if s_ruolo.startswith("esx") else 0
            nome = str(y[CMDB_field["Nome CI"]]).lower() if len(y) > CMDB_field["Nome CI"] else ""
            
            if not nome or nome in nomi:
                i += 1
                continue
            nomi.append(nome)
            
            # Costruzione lista nell’ordine dei campi
            t = []
            for c in CMDB_field:
                idx = CMDB_field[c]
                if c == "Nome CI":
                    t.append(nome)
                elif idx < len(y):
                    t.append(y[idx])
                else:
                    t.append("")
            
            z = c_CMDB(nome, t)
            
            if is_esx:
                if len(z.dati) > 6:
                    z.dati[6] = z.dati[5]
                z.dati[5] = y[32] if len(y) > 32 else ""
                CMDB_esx.append(z)
            
            CMDB.append(z)
            i += 1

# --- Caricamento server DISMESSI
cm.files.clear()
file_pattern = cm.pr["DISMESSI_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)
input_file = temp[0]
print("\nElaborazione file " + input_file)

i = 0
with open(input_file, "r", encoding="utf-8") as fc:
    for x in fc:
        print('\r', mesg.format(i), end='', flush=True)
        if i < 2:
            i += 1
            continue
        
        separa = cm.trova_separa(x)
        tmp = cm.togli_apici(x, separa)
        y = tmp.split(cm.cs)
        nome = str(y[DISS_field["server"]]).lower() if len(y) > DISS_field["server"] else ""
        
        t = []
        for c in DISS_field:
            idx = DISS_field[c]
            if c == "server":
                t.append(nome)
            else:
                t.append(y[idx] if idx < len(y) else "")
        
        DISS.append(c_DISS(nome, t))
        i += 1

# --- Caricamento PDL
cm.files.clear()
file_pattern = cm.pr["PDL_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)
input_file = temp[0]
print("\nElaborazione file " + input_file)

i = 0
header_line = None

with open(input_file, "r", encoding="utf-8") as fc:
    for x in fc:
        print('\r', mesg.format(i), end='', flush=True)
        
        # Lettura header per identificare gli indici corretti
        if i == 1:
            separa = cm.trova_separa(x)
            tmp = cm.togli_apici(x, separa)
            header_cols = tmp.split(cm.cs)
            
            # Ricerca index delle colonne
            PDL_field_new = {}
            for col_name in ["Nome CI", "Category", "Type", "Domain Name", "Used By"]:
                try:
                    idx = header_cols.index(col_name)
                    PDL_field_new[col_name] = idx
                except ValueError:
                    PDL_field_new[col_name] = PDL_field.get(col_name, 0)
            
            PDL_field = PDL_field_new
            print(f"\n🔍 Indici PDL rilevati: {PDL_field}")
            i += 1
            continue
        
        if i < 2:
            i += 1
            continue
        
        separa = cm.trova_separa(x)
        tmp = cm.togli_apici(x, separa)
        y = tmp.split(cm.cs)
        nome = str(y[PDL_field["Nome CI"]]).lower() if len(y) > PDL_field["Nome CI"] else ""
        
        t = []
        for c in PDL_field:
            idx = PDL_field[c]
            if c == "Nome CI":
                t.append(nome)
            else:
                t.append(y[idx] if idx < len(y) else "")
        
        if not any(p.nome == nome for p in PDL):
            PDL.append(c_PDL(nome, t))
        i += 1

# --- Scrittura file di output
def write_output_file(filename, field_dict, data_list):
    y = [cm.out_path, cm.pr[filename]]
    output_file = cm.dr.join(y)
    print("\n\nScrittura file " + output_file)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("sep=" + cm.cs + "\n")
        f.write(cm.cs.join(field_dict) + "\n")
        
        for j, item in enumerate(data_list):
            print('\r', mesg.format(j), end='', flush=True)
            f.write(cm.cs.join(map(str, item.dati)) + "\n")

write_output_file("OUT_CMDB", CMDB_field, CMDB)
write_output_file("OUT_CMDB_ESX", CMDB_field, CMDB_esx)
write_output_file("OUT_DISMESSI", DISS_field, DISS)
write_output_file("OUT_PDL", PDL_field, PDL)
