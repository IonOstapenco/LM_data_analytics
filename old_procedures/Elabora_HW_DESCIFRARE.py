# =========================
# Construire Tabella HW
# =========================

# import csv  # momentan nu este folosit direct aici
import Common as cm   # modul comun unde sunt definite funcțiile și parametrii generali

# -------------------------------------------------------------------------------------------------
# DICTIONARUL FINAL - va conține rezultatul consolidat (Tabella_HW)
# Cheia = numele serverului
# Valoarea = dicționar cu toate câmpurile hardware
# -------------------------------------------------------------------------------------------------

Hardware = {}

# Hardware_field definește:
# - ce câmpuri vor exista în tabela finală
# - din ce sursă se ia fiecare câmp
# - ce poziție (coloană) din sursă trebuie folosită
# Ordinea surselor reprezintă prioritatea

Hardware_field = {

    # Exemplu:
    # "nome": {"CMDB_Citrix": 0, "BGFX": 1}
    # Înseamnă:
    # 1. încearcă să ia valoarea din CMDB_Citrix coloana 0
    # 2. dacă nu există, ia din BGFX coloana 1

    "nome": {"CMDB_Citrix": 0, "BGFX": 1},
    "operating_system": {"CMDB_Citrix": 1, "BGFX": 2, "CMDB_esx": 1, "VM": 14},
    "dominio": {"BGFX": 26, "CMDB_Citrix": 3, "HOST": 23},
    "dns_name": {"CMDB_Citrix": 2, "BGFX": 3, "VM": 4},
    "virtuale": {"CMDB_Citrix": 4, "BGFX": 14},
    "tipo": {"CMDB_Citrix": 17},

    # Date legate de cluster (doar pentru mașini virtuale)
    "cluster_name": {"Cluster": 0, "CMDB_Citrix": 9},
    "cluster_ambiente": {"Cluster": 10},
    "cluster_cliente": {"Cluster": 11},
    "cluster_destinazione": {"Cluster": 12},
    "cluster_cores": {"Cluster": 4, "BGFX": 28},
    "cluster_numhosts": {"Cluster": 1},
    "cluster_n_vms_total": {"Cluster": 16},
    "cluster_n_vms": {"Cluster": 17},
    "cluster_n_vms_win": {"Cluster": 18},

    # Informații host
    "hyperthreadactive": {"HOST": 8},
    "ha_enabled": {"Cluster": 6},
    "drs_enabled": {"Cluster": 7},
    "host": {"VM": 12, "CMDB_Citrix": 11, "BGFX": 31},

    # Informații VM
    "vm_hw_version": {"VM": 8},
    "n_cpu": {"BGFX": 7, "CMDB_Citrix": 6},
    "n_core": {"VM": 5, "BGFX": 6, "CMDB_Citrix": 5},

    # Informații licențiere
    "pvu_per_core": {"BGFX": 21},
    "valore_pvu_modificato": {"BGFX": 22},
    "valore_pvu_predefinito": {"BGFX": 23},
    "fattore_core_oracle": {"BGFX": 24},

    "powerstate": {"VM": 1},

    # Informații VCenter
    "vcenter": {"CMDB_Citrix": 11, "VM": 16, "Cluster": 13},
    "vcenter_cores": {"VCenter": 2},
    "vcenter_hosts": {"VCenter": 3},
    "vcenter_dominio": {"VCenter": 4},
    "vcenter_cluster": {"VCenter": 1},

    # Alte informații
    "cpu_model": {"BGFX": 17, "CMDB_Citrix": 8},
    "applicazione": {"CMDB_Citrix": 14},
    "ruolo": {"CMDB_Citrix": 15},
    "ambiente": {"CMDB_Citrix": 18},
    "responsabile": {"CMDB_Citrix": 19},
    "cliente": {"CMDB_Citrix": 20},
    "contratto": {"CMDB_Citrix": 21},
    "sito": {"HOST": 1, "VM": 10}
}

# -------------------------------------------------------------------------------------------------
# DICTIONARELE SURSA
# Fiecare reprezintă un fișier CSV încărcat anterior
# Cheia = nume server
# Valoare = lista valorilor de pe linia respectivă
# -------------------------------------------------------------------------------------------------

BGFX = {}           # ICTG-HW
CMDB_Citrix = {}    # Server_CMDB_Citrix
VM = {}             # VM_list.csv
HOST = {}           # Host_list.csv
Cluster = {}        # Cluster_list.csv
VCenter = {}        # Vcenter_list.csv
DISS = {}           # ServerDismessi
PDL = {}            # AssetClient

# -------------------------------------------------------------------------------------------------
# ÎNCĂRCARE DATE DIN FIȘIERE (folosind funcția din Common.py)
# -------------------------------------------------------------------------------------------------

cm.check_outdir(cm.out_path)   # verifică / creează directorul de output

# Pentru fiecare fișier se:
# 1. construiește path-ul
# 2. se încarcă datele în dicționar

y = [cm.out_path, cm.pr["OUT_CLUSTER"]]
cm.carica_dati(cm.dr.join(y), Cluster, 0)

y = [cm.out_path, cm.pr["OUT_VM"]]
cm.carica_dati(cm.dr.join(y), VM, 0)

y = [cm.out_path, cm.pr["OUT_Host"]]
cm.carica_dati(cm.dr.join(y), HOST, 0)

y = [cm.out_path, cm.pr["OUT_BGFX"]]
cm.carica_dati(cm.dr.join(y), BGFX, 1)  # cheia este pe poziția 1

y = [cm.out_path, cm.pr["OUT_CMDB_Citrix"]]
cm.carica_dati(cm.dr.join(y), CMDB_Citrix, 0)

y = [cm.out_path, cm.pr["OUT_VCENTER"]]
cm.carica_dati(cm.dr.join(y), VCenter, 0)

y = [cm.out_path, cm.pr["OUT_DISMESSI"]]
cm.carica_dati(cm.dr.join(y), DISS, 0)

y = [cm.out_path, cm.pr["OUT_PDL"]]
cm.carica_dati(cm.dr.join(y), PDL, 0)

# -------------------------------------------------------------------------------------------------
# CONSTRUIREA TABELEI HARDWARE
# -------------------------------------------------------------------------------------------------

# Lista serverelor din CMDB (baza principală)
lnome = list(CMDB_Citrix.keys())

# Lista câmpurilor care trebuie populate
lfield = list(Hardware_field.keys())

i = 0

# Pentru fiecare server din CMDB
for k in lnome:

    print('\r', f"Elemento [{i}]", end='', flush=True)

    Hardware[k] = {}

    # Pentru fiecare câmp din tabela finală
    for f in lfield:

        # Lista surselor în ordinea priorității
        p = list(Hardware_field[f].keys())

        for a in p:

            match a:

                # 1️⃣ Sursa CMDB
                case "CMDB_Citrix":
                    Hardware[k][f] = CMDB_Citrix[k][Hardware_field[f][a]]
                    break

                # 2️⃣ Sursa BigFix
                case "BGFX":
                    try:
                        Hardware[k][f] = BGFX[k][Hardware_field[f][a]]
                        break
                    except:
                        Hardware[k][f] = "-"

                # 3️⃣ HOST (doar dacă serverul NU este virtual)
                case "HOST":
                    if CMDB_Citrix[k][4] == "SI":
                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = HOST[k][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"

                # 4️⃣ VM (doar dacă serverul ESTE virtual)
                case "VM":
                    if CMDB_Citrix[k][4] == "NO":
                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = VM[k][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"

                # 5️⃣ Cluster (doar pentru VM)
                case "Cluster":
                    if CMDB_Citrix[k][4] == "NO":
                        Hardware[k][f] = "-"
                    else:
                        try:
                            cluster_name = CMDB_Citrix[k][9]
                            Hardware[k][f] = Cluster[cluster_name][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"

                # 6️⃣ VCenter (doar pentru VM)
                case "VCenter":
                    if CMDB_Citrix[k][4] == "NO":
                        Hardware[k][f] = "-"
                    else:
                        l = cm.togli_dominio(CMDB_Citrix[k][10])
                        try:
                            Hardware[k][f] = VCenter[l[0]][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"

    i += 1

# -------------------------------------------------------------------------------------------------
# ADAUGARE PDL (Desktop-uri)
# -------------------------------------------------------------------------------------------------

for k in PDL.keys():

    Hardware[k] = {}

    # Inițializare toate câmpurile cu "-"
    for f in lfield:
        Hardware[k][f] = '-'

    # Setare câmpuri specifice PDL
    Hardware[k]["nome"] = PDL[k][0]
    Hardware[k]["tipo"] = "PDL"
    Hardware[k]["dominio"] = PDL[k][3]
    Hardware[k]["cliente"] = PDL[k][4]
    Hardware[k]["ruolo"] = "Desktop"
    Hardware[k]["ambiente"] = "Produzione"
    Hardware[k]["virtuale"] = "NO"

# -------------------------------------------------------------------------------------------------
# SCRIERE FIȘIER FINAL Tabella_HW.csv
# -------------------------------------------------------------------------------------------------

y = [cm.out_path, cm.pr["OUT_Hardware_TAB"]]
output_file = cm.dr.join(y)

f = open(output_file, "w")

# Scriere separator
f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

# Scriere header
riga = cm.cs.join(lfield)
f.write(riga + "\n")

# Scriere date
for j, c in enumerate(Hardware.keys()):
    print('\r', f"Elemento [{j}]", end='', flush=True)
    riga = cm.cs.join(map(str, list(Hardware[c].values())))
    f.write(riga + "\n")

f.close()

print("\n>-----------------------------------------------------------<\n")
