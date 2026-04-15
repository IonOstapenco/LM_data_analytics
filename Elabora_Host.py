# Python Classi dati server Host
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class c_HOST:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

HOST = []
HOST_field = { "Host": 0,                   # 0
               "Datacenter": 0,             # 1
               "Cluster": 0,                # 2
               "Config status": 0,          # 3
               "in Maintenance Mode": 0,    # 4  
               "in Quarantine Mode": 0,     # 5
               "CPU Model": 0,              # 6
               "HT Available": 0,           # 7
               "HT Active": 0,              # 8
               "# CPU": 0,                  # 9  in CMDB
               "Cores per CPU": 0,          # 10
               "# Cores": 0,                # 11 in CMDB
               "# VMs total": 0,            # 12
               "# VMs": 0,                  # 13
               "VMs per Core": 0,           # 14
               "# vCPUs": 0,                # 15
               "vCPUs per Core": 0,         # 16
               "VMotion support": 0,        # 17
               "Storage VMotion support": 0,# 18
               "ESX Version": 0,            # 19
               "Vendor": 0,                 # 20
               "Model": 0,                  # 21
               "VI SDK Server": 0,          # 22 in CMDB
               "Dominio_ESX": 0             # 23
              }
n_HOST = 23

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_CMDB:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo
CMDB_esx = []
CMDB_field = {  "Nome CI"     : 0, 
                "OS"          : 1, 
                "DNS"         : 2, 
                "Domain Name" : 3, 
                "Is Virtual"  : 4, 
                "Numero CPU" : 5,   
                "Numero Socket" : 6, 
                "Processore" : 7, 
                "Modello" : 8, 
                "VM_Cluster" : 9, 
                "VM_Virtualcenter": 10, 
                "VM_Host" : 11,
                "VMWare_LastReportDate" : 12,
                "Bigfix_LastReportDate" : 13,
                "Applicazione (lista)" : 14,
                "Ruolo" : 15,
                "Category" : 16,
                "Type" : 17,
                "Ambiente" : 18,
                "Responsabile" : 19,
                "Used By": 20,
                "Contratto" : 21,
                "server_iscloud" : 22,
                "ESX Version" : 23
            }


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


print("Procedura per la elaborazione dei dati da RVTools - tabvHost.")

#
# Cerco il file più recente in base al pattern indicato in Parametri.json


# ----------------------------------------------------------------------------------------------
# ==============================================================================================
# --                         PROCESAREA RVTOOLS (HOST)
# =================================================================================================
# =-=-=-=-=-=-=-----------------=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=--=-=-=-==-=-=--
    #       cautare fisiere 
    # ------------=-=-=-=-===================================
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Host_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
    fc = open(w, "r")
    Linee = fc.readlines()
    separa = cm.trova_separa(Linee[0])

    # Citire header + mapping la pozitii 

    tmp = cm.togli_apici(Linee[0], separa)  # --- Linee[0] contiene l'intestazione delle colonne.
    y = tmp.split(cm.cs)   # ----------- Separo i campi dell'intestazione
    n = len(y)
    i = 0
    for c in y:
        if ( c in HOST_field ):
            HOST_field[c] = i    # ---- Memorizzo la posizione del campo che mi interessa per questo file.
        i += 1
    del Linee[0]    # ------------------ Elimino la prima riga in quanto già elaborata
    i = 0

    # -------------------------------------------------------------------------------------
    # ---    procesare randuri
    # ---
    # --------------------------------------------------------------
    for linea in Linee:
        print('\r', mesg.format(i), end='', flush=True)

#
# Preparo la riga con tutti gli attributi/caratteristiche del server. Quelle che interessano
#
        tmp = cm.togli_apici(linea, separa)
        y = tmp.split(cm.cs) # --> extragere date
        nome = str(y[HOST_field["Host"]]).lower() # --> nume server (pe ce masina sta)
        l = cm.togli_dominio(nome) # --> sterge domeniu / domain
        nome = l[0]
        if ( l[1] == '' ):
            dominio = '-'
        else:
            dominio = l[1]
        l = list(HOST_field.keys())
        t = [nome] # -- construieste lista de date
        for c in range(1, n_HOST):
            t.append(y[HOST_field[l[c]]])
        t.append(dominio)       # 23esimo elemento : il dominio dell'ESX
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CMDB_field
#
        z = c_HOST(nome, t)
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CMDB e che
# viene memorizzato nella lista di oggetti 'CMDB'
#
        HOST.append(z)
        i += 1

# -----------------------------------------  FINE ciclo sulle righe

#
# Scrittura file intermedio: Host_list.csv
#
# ---=====================================----------------------------------------------------
# OUTPUT INTERMEDIAR -- Host_list.csv
# -------=================================---------------------------------=====================
cm.scrivi_dati("OUT_Host", HOST_field, HOST) # ---> output intermediar

#y = [cm.out_path, cm.pr["OUT_Host"]]
#
#output_file = cm.dr.join(y)
#
#f = open(output_file, "w")
#
#f.write("sep=" + cm.cs + "\n")
#
#print("\n\nScrittura file " + output_file)
#
#riga = cm.cs.join(list(HOST_field.keys()))
#
#f.write(riga + "\n")
#
#n = len(HOST)
#for j in range(0, n):
#    print('\r', mesg.format(j), end='', flush=True)
#    riga = cm.cs.join(map(str, HOST[j].dati))
#    f.write(riga + "\n")
#f.close()


#
# Deve essere fatto il merge con i dati del CMDB relativi agli ESX.
#


y = [cm.out_path, cm.pr["OUT_CMDB_ESX"]]

s_file = cm.dr.join(y)
# -------------------------------------------------------------------------------
# citire CMDB ESX
# ----------------------------------------------------------------------------------------
f = open(s_file, "r")




Linee = f.readlines()

del Linee[0]
del Linee[0]
# -------------------------------------------------------------------------------------
# procesare fiecare server CMDB
# --------------------------------------------------------------------------------------------
for linea in Linee:
    a = str(linea).rstrip('\n')
    y = a.split(cm.cs)
    # --- aici extragem nume ----- 
    nome = str(y[CMDB_field["Nome CI"]]).lower()
    l = cm.togli_dominio(nome)
    nome = l[0]
    dnsname = str(y[CMDB_field["DNS"]]).lower()
    l = cm.togli_dominio(dnsname)
    if ( l[1] == '' ):
        dominio = '-'
    else:
        dominio = l[1]
    z = c_CMDB(nome, y)

    # ----- gaseste host corespunzator -----------------------------------------------------------
    # un fel de join intre cmdb si host
    trovato = next(
        (o_g for o_g in HOST if o_g.nome == nome),
        None
    )

    # ----------------  Actualizare date CMDB ------------------------------------------------
    try:
        z.dati[CMDB_field["Numero Socket"]] = trovato.dati[9]                   # # CPU
        z.dati[CMDB_field["Numero CPU"]] = trovato.dati[11]                     # # Cores
        z.dati[CMDB_field["VM_Virtualcenter"]] = trovato.dati[22]               # VI SDK Server
        z.dati.append(trovato.dati[19])                                         # ESX Version
    except:
        z.dati.append(0)
    finally:
        z.dati[CMDB_field["Domain Name"]] = dominio                             # Dominio ESX
        CMDB_esx.append(z)

# -----------------------------------------  FINE ciclo sulle righe

#
# Scrittura del file AssetCMDB_Esx.csv
#

cm.scrivi_dati("OUT_CMDB_ESX", CMDB_field, CMDB_esx)

#y = [cm.out_path, cm.pr["OUT_CMDB_ESX"]]
#
#output_file = cm.dr.join(y)
#
#f = open(output_file, "w")
#
#f.write("sep=" + cm.cs + "\n")
#
#print("\n\nScrittura file " + output_file)
#
#riga = cm.cs.join(list(CMDB_field.keys()))
#
#f.write(riga + "\n")
#
#n = len(CMDB_esx)
#for j in range(0, n):
#    print('\r', mesg.format(j), end='', flush=True)
#    riga = cm.cs.join(map(str, CMDB_esx[j].dati))
#    f.write(riga + "\n")
#f.close()

print("\nFine procedura!\n")