 # Python Classi dati della tabella HW 

#from sys import exit
import csv # --> voi folosi pentru dictreader
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# f-tie de stergere BOM
# funzione per rimuovere il BOM (Byte Order Mark) e pulire la stringa
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()


# #!! cream functie pentru convertire // incarcare 
# creiamo una funzione per la conversione e il caricamento dei dati 
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()


def carica_dati_dict(input_file, dati, key_field):
    print(f"\nCaricamento: {input_file}")

    with open(input_file, "r", encoding="cp1252") as f: # --> am shicmbat din utf-8
                                                        # ho cambiatoa da utf-8
        # fiindca facea probleme la dictreader
        #perché con utf-8 dava problemi con DictReader

        delimiter = cm.cs

        #  detectare si sarire linie sep=
        # rilevamento e salto della riga sep=
        pos = f.tell()
        first_line = f.readline()

        if first_line.lower().startswith("sep="):
            delimiter = first_line.strip().split("=")[1]
        else:
            f.seek(pos)

        reader = csv.DictReader(f, delimiter=delimiter)

        #  normalizare header
        # normalizzazione dell'header del file
        reader.fieldnames = [norm(h) for h in reader.fieldnames]

        # pentru debug
        # per debug
        print("Header detectat:", reader.fieldnames)


        for row in reader:

            row = {norm(k): v for k, v in row.items() if k is not None}

            key = row.get(key_field)

            if key:
                dati[key.strip()] = row



# ----- ASTA PENTRU OUTPUT! se ia din fiecare colectie, si se inscrie in tabella_HW
#asta defineste cimpuri din tabella.hw
# questo è per l'OUTPUT: prende i dati da ogni collezione e li scrive nella tabella_HW
# asta defineste cimpuri din tabella.hw
# questo definisce i campi della tabella HW
Hardware = {}  

# modificam cum ne trebuieste!!
# modifichiamo secondo le nostre necessità

#!!! probabil un fel de LEFT join pe CMDB
# probabilmente una specie di LEFT JOIN sulla CMDB

Hardware_field = { # !! hz poate sa iau exemplu de la inner join sau un exercitiu de suprapunere
    # era asa --> "nome": {"CMDB_Citrix": 0, "BGFX": 1},
    "nome": {"CMDB_Citrix": "Nome CI", "BGFX": "Nome computer"},  # -- > combina/ia din Server_CMDB_Citrix , ICTG-HW                                         
    
    #"operating_system": {"CMDB_Citrix": 1, "BGFX": 2, "CMDB_esx": 1, "VM": 14},     
    "operating_system": {"CMDB_Citrix": "OS", "BGFX": "Sistema operativo", "CMDB_esx": "OS", "VM": "OS according to the VMware Tools"}, 
    
    #"dominio": {"BGFX": 26, "CMDB_Citrix": 3, "HOST": 23}, 
    "dominio": {"BGFX": "Domain", "CMDB_Citrix": "Domain Name", "HOST": "Dominio_ESX"},  

    #"dns_name": {"CMDB_Citrix": 2, "BGFX": 3, "VM": 4},
    "dns_name": {"CMDB_Citrix": "DNS", "BGFX": "Nome DNS", "VM": "DNS Name"},
    
    #!!!! nu inteleg daca trebuieste aici BGFX???
    #"virtuale": {"CMDB_Citrix": "Is Virtual", "BGFX": 14}, 
    "virtuale": {"CMDB_Citrix": "Is Virtual"},             
    
    #"tipo": {"CMDB_Citrix": 17}, 
    "tipo": {"CMDB_Citrix": "Type"},     
# -----------------------------------------------------------------------------
# zona cu CLUSTER!!!
# area relativa ai CLUSTER
# --------------------------------------------------------------------------
    #"cluster_name": {"Cluster": 0, "CMDB_Citrix": 9},  
    "cluster_name": {"Cluster": "Name", "CMDB_Citrix": "VM_Cluster"},           
    
    #"cluster_ambiente": {"Cluster": 10},
    "cluster_ambiente": {"Cluster": "Ambiente"}, 

    #"cluster_cliente": {"Cluster": 11},      
    
    "cluster_cliente": {"Cluster": "Cliente"},          
    
    #"cluster_destinazione": {"Cluster": 12}, 
    "cluster_destinazione": {"Cluster": "Destinazione"}, 

    #"cluster_cores": {"Cluster": 4, "BGFX": 28},
    "cluster_cores": {"Cluster": "NumCpuCores"},       
    
    #"cluster_numhosts": {"Cluster": 1},
    "cluster_numhosts": {"Cluster": "NumHosts"},       
    
    #"cluster_n_vms_total": {"Cluster": 16},
    "cluster_n_vms_total": {"Cluster": "# VMS Total"},
    
    #"cluster_n_vms": {"Cluster": 17}, 
    "cluster_n_vms": {"Cluster": "# VMS"},  
    
    #"cluster_n_vms_win": {"Cluster": 18},
    "cluster_n_vms_win": {"Cluster": "# VMS WIN"},
    # -----------------------------------------------------------------------------
    ### Zona cu HOST
    #area relativa ai CLUSTER
    # -----------------------------------------------------------------------------
    #"hyperthreadactive": {"HOST": 8},
    "hyperthreadactive": {"HOST": "HT Active"},              
    
    #"ha_enabled": {"Cluster": 6}, 
    "ha_enabled": {"Cluster": "HA enabled"},               
    
    #"drs_enabled": {"Cluster": 7},
    "drs_enabled": {"Cluster": "DRS enabled"},               
    
    #"host": {"VM": 12, "CMDB_Citrix": 11, "BGFX": 31},
    "host": {"VM": "Host", "CMDB_Citrix": "VM_Host"}, # 31, "Last Report Time" nu este! non esista Last Report Time
    
    # -------------------------------------------------------------------------------- 
    ## !! VM zone

    # --------------------------------------------------------------------------------
    #"vm_hw_version": {"VM": 8},
    "vm_hw_version": {"VM": "HW version"},         
    
    #"n_cpu": { "CMDB_Citrix": 6}, 
    "n_cpu": { "CMDB_Citrix": "Numero Socket"},    #--> am pus Socket attivi del server in clod de numero cpu              
    
    #"n_core": {"VM": 5, "BGFX": 6, "CMDB_Citrix": 5}, #--> nr cpu nu este deja in itcg-hw
    "n_core": {"VM": "CPUs", "CMDB_Citrix": "Numero CPU"},                           
    
    #"pvu_per_core": {"BGFX": 21},  
    "pvu_per_core": {"BGFX": "PVU per core"},             
    
    #"valore_pvu_modificato": {"BGFX": 22}, 
    "valore_pvu_modificato": {"BGFX": "Valore PVU modificato"},      
    
    #"valore_pvu_predefinito": {"BGFX": 23}, 
    "valore_pvu_predefinito": {"BGFX": "Valore PVU predefinito"},     
    
    #"fattore_core_oracle": {"BGFX": 24},
    "fattore_core_oracle": {"BGFX": "Fattore core Oracle"},       
    
    #"powerstate": {"VM": 1}, 
    "powerstate": {"VM": "Powerstate"},                
    
    #"vcenter": { "CMDB_Citrix": 11, "VM": 16, "Cluster": 13},
    "vcenter": { "CMDB_Citrix": "VM_Host", "VM": "Category", "Cluster": "VI SDK Server"},                 
    
    #"vcenter_cores":{"VCenter": 2},
    "vcenter_cores":{"VCenter": "Core Totali"},        
    
    #"vcenter_hosts":{"VCenter": 3},
    "vcenter_hosts":{"VCenter": "Host"},        
    
    #"vcenter_dominio":{"VCenter": 4},
    "vcenter_dominio":{"VCenter": "Dominio"},      
    
    #"vcenter_cluster":{"VCenter": 1},
    "vcenter_cluster":{"VCenter": "Cluster"},      
    
    #"cpu_model": {"BGFX": 17, "CMDB_Citrix": 8},
    "cpu_model": {"BGFX": "Vendor", "CMDB_Citrix": "Modello"},              
    
    #"applicazione": {"CMDB_Citrix": 14},
    "applicazione": {"CMDB_Citrix": "Applicazione (lista)"},            
    
    #"ruolo": {"CMDB_Citrix": 15}, 
    "ruolo": {"CMDB_Citrix": "Ruolo"},                   
    
    #"ambiente": {"CMDB_Citrix": 18 }, 
    "ambiente": {"CMDB_Citrix": "Ambiente" },                                 
    
    #"responsabile": {"CMDB_Citrix": 19},
    "responsabile": {"CMDB_Citrix": "Responsabile (Server)"}, # --> modificato a 11/03/26, a cauza di input                              
    
    #"cliente":{"CMDB_Citrix": 20}, 
    "cliente":{"CMDB_Citrix": "Used By"},                 
    
    #"contratto": {"CMDB_Citrix": 21},
    "contratto": {"CMDB_Citrix": "Contratto"},                     
    
    #"sito": {"HOST": 1, "VM": 10}
    "sito": {"HOST": "Datacenter", "VM": "Datacenter"}
}


## de unde se ia info, colectii cu campuri

# trebuie sa modificam colectia, fiindca din 2026 are alta structura
#ICTG-HW.csv (februarie)

# dobbiamo modificare la collezione perché dal 2026 ha una structura diversa

#Stato|
# Nome computer|
# Sistema operativo|
# Nome DNS|
# Tipo di computer|
# Core partizione|
# Core server|
# Stringa marchio processore|
# Vendor
# |PVU per core|
# Valore PVU modificato|
# Valore PVU predefinito|
# Fattore core Oracle|
# Socket attivi del server
# |Nome cluster
# |Core cluster
BGFX = {} # ---> ICTG_HW clasic

BGFX_field ={"Stato", # --> ICTG_HW nou
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

}
"""
BGFX_field = {"Stato": 0, # ---> ICTG-HW clasic
              "Nome computer": 1,
              "Sistema operativo": 2,
              "Nome DNS": 3,
              "AIX Full OS Level": 4,
              "Technology Level": 5,
              "NumeroCPU": 6,
              "NumeroSocket": 7,
              "License Type": 8,
              "Computer Type": 9,
              "Java Output": 10,
              "JavaPath": 11,
              "JavaVersion": 12,
              "Tipo di computer": 13,
              "Core partizione": 14,
              "Core server": 15,
              "Stringa marchio processore": 16,
              "Vendor": 17,
              "Marchio": 18,
              "Tipo": 19,
              "Modello": 20,
              "PVU per core": 21,
              "Valore PVU modificato": 22,
              "Valore PVU predefinito": 23,
              "Fattore core Oracle": 24,
              "Socket attivi del server": 25,
              "Domain": 26,
              "Nome cluster": 27,
              "Core cluster": 28,
              "CPU": 29,
              "Nome host padre": 30,
              "Last Report Time": 31,
              "Tipo di server": 32
             }
"""


CMDB_Citrix = {} # ---> Server_CMDB_Citrix.csv
CMDB_field = {  "Nome CI": "Nome CI" , 
                "OS": "OS", 
                "DNS": "DNS"        , 
                "Domain Name":"Domain Name" , 
                "Is Virtual" :  "Is Virtual", 
                "Numero CPU":"Numero CPU" ,   
                "Numero Socket":"Numero Socket" , 
                "Processore" :"Processore" , 
                "Modello" :"Modello", 
                "VM_Cluster" :"VM_Cluster" , 
                "VM_Virtualcenter":"VM_Virtualcenter", 
                "VM_Host" :"VM_Host" ,
                "VMWare_LastReportDate":"VMWare_LastReportDate",
                "Bigfix_LastReportDate":"Bigfix_LastReportDate",
                "Applicazione (lista)":"Applicazione (lista)",
                "Ruolo":"Ruolo",
                "Category":"Category",
                "Type":"Type" ,
                "Ambiente": "Ambiente",
                "Responsabile":"Responsabile",
                "Used By":"Used By",
                "Contratto" :"Contratto",
                "server_iscloud":"server_iscloud"
            }

VM = {} # ---> din VM_list.csv se iau campuri
VM_field = {
    "VM": 0,
    "Powerstate": 0,
    "Template": 0,
    "SRM Placeholder": 0,
    "DNS Name": 0,
    "CPUs": 0,
    "Memory": 0,
    "Primary IP Address": 0,
    "HW version": 0,
    "Annotation": 0,
    "Datacenter": 0,
    "Cluster": 0,
    "Host": 0,
    "OS according to the configuration file": 0,
    "OS according to the VMware Tools": 0,
    "VM ID": 0,
    "VI SDK Server type": 0,
    "VI SDK API Version": 0,
    "VI SDK Server": 0,
    "Sockets": 0,
    "Cores p/s": 0,
    "Tools": 0,
    "Tools Version": 0,
    "Required Version": 0,
    "Upgradeable": 0,
    "Upgrade Policy": 0
    }

HOST = {} # ---> Host_list.csv
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

Cluster = {} # ---> din fisier Cluster_list.csv
Cluster_field = { "Name": 0,
                  "NumHosts": 0,
                  "numEffectiveHosts": 0,
                  "TotalCpu": 0,
                  "NumCpuCores": 0,
                  "NumCpuThreads": 0,
                  "HA enabled": 0,
                  "DRS enabled": 0,
                  "DRS default VM behavior": 0,
                  "DRS vmotion rate": 0,
                  "Ambiente": 0,
                  "Cliente": 0,
                  "Destinazione": 0,
                  "VI SDK Server": 0,
                  "Vcenter": 0,
                  "Vcenter dominio": 0,
                  "# VMS Total": 0,  # in VM_list
                  "# VMS": 0,        # in VM_list
                  "# VMS WIN" : 0    # in VM_list
                }
 
VCenter = {} # --> Vcenter_list
VCenter_field = {"Nome": 0,
           "Cluster": 1,
           "Core Totali": 2,
           "Host": 3,
           "Dominio": 4
           }

DISS = {}  # ---> ServerDismessi
DISS_field = {"server": 0,
              "datadismissione": 2
           }

PDL = {} # -----> AssetClient
PDL_field = {"Nome CI": "Nome CI",
             "Category": "Category",
             "Type": "Type",
             "Domain Name": "Domain Name",
             "Used By": "Used By"
            }


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Caricamento dati elaborati in precedenza
# Încărcarea datelor procesate anterior

cm.check_outdir(cm.out_path)

mesg = "Elemento [{}]"
mes1 = "File in caricamento: [{}]"
""""
y = [cm.out_path, cm.pr["OUT_CLUSTER"]]
input_file = cm.dr.join(y)

cm.carica_dati(input_file, Cluster, 0)

y = [cm.out_path, cm.pr["OUT_VM"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, VM, 0)

y = [cm.out_path, cm.pr["OUT_Host"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, HOST, 0)

y = [cm.out_path, cm.pr["OUT_BGFX"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, BGFX, 1)

y = [cm.out_path, cm.pr["OUT_CMDB_Citrix"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, CMDB_Citrix, 0)

y = [cm.out_path, cm.pr["OUT_VCENTER"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, VCenter, 0)

y = [cm.out_path, cm.pr["OUT_DISMESSI"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, DISS, 0)

y = [cm.out_path, cm.pr["OUT_PDL"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, PDL, 0)


"""


cm.check_outdir(cm.out_path)

# CLUSTER
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_CLUSTER"]])
carica_dati_dict(input_file, Cluster, "Name")

# VM
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_VM"]])
carica_dati_dict(input_file, VM, "VM")

# HOST
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_Host"]])
carica_dati_dict(input_file, HOST, "Host")

# BGFX
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_BGFX"]])
carica_dati_dict(input_file, BGFX, "Nome computer")

# CMDB
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_CMDB_Citrix"]])
carica_dati_dict(input_file, CMDB_Citrix, "Nome CI")

# VCENTER
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_VCENTER"]])
carica_dati_dict(input_file, VCenter, "Nome")

# DISMESSI
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_DISMESSI"]])
carica_dati_dict(input_file, DISS, "server")

# PDL
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_PDL"]])
carica_dati_dict(input_file, PDL, "Nome CI")
# chestia asta trebuie de simplificat cred ca
# # questa parte probabilmente deve essere semplificata

# Acestea sunt numele serverelor listate în lista îmbinată între CMDB și Citrix
lnome = list(CMDB_Citrix.keys())        # Questi sono i nomi del server elencati nella lista unita tra CMDB e Citrix

# Acestea sunt numele câmpurilor pe care trebuie să le completăm pentru tabelul HW.
lfield= list(Hardware_field.keys())     # Questi sono i nomi dei campi che dobbiamo compilare per Tabella HW.


i = 0
# 'k' conține numele serverului, din lista CMDB_Citrix, care este procesat.
for k in lnome:                         # 'k' contiene il nome del server, dall'elenco CMDB_Citrix, in fase di elaborazione.
    print('\r', mesg.format(i), end='', flush=True)
    Hardware[k] = {}
    # # 'f' conține numele câmpului care va fi populat în tabelul HW
    for f in lfield:                        # 'f' contiene il nome del campo da compilare in Tabella HW
        p = list(Hardware_field[f].keys())  # Questo è l'elenco delle priorità: da quale origine prendere il valore per primo.
        for a in p:                         # 'a' contiene il nome dell'origine da cui prendere il valore da inserire in Tabella HW
            match a:
                case "CMDB_Citrix":
                    Hardware[k][f] = CMDB_Citrix[k][Hardware_field[f][a]]
                    break
                case "BGFX":
                    try:
                        Hardware[k][f] = BGFX[k][Hardware_field[f][a]]
                        break
                    except:
                        Hardware[k][f] = "-"
                case "HOST":
                  #  if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "SI":
                    if CMDB_Citrix[k]["Is Virtual"] == "SI":
    
                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = HOST[k][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"
                case "VM":
                    #if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "NO":
                    if CMDB_Citrix[k]["Is Virtual"] == "NO":

                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = VM[k][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"
                case "Cluster":
                    
                    if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "NO":
                    #if Cluster[CMDB_Citrix[k]["Is Virtual"]] == "NO":
                        Hardware[k][f] = "-"
                    else:
                        cluster_name = CMDB_Citrix[k][CMDB_field["VM_Cluster"]].strip()
                        if cluster_name in Cluster:
                            Hardware[k][f] = Cluster[cluster_name][Hardware_field[f][a]] 
                        else:
                           Hardware[k][f] = "-"     
                        #try:
                            #Hardware[k][f] = Cluster[CMDB_Citrix[k][CMDB_field["VM_Cluster"]]][Hardware_field[f][a]]
                           # Hardware[k][f] = Cluster[CMDB_Citrix[k]["VM_Cluster"]][Hardware_field[f][a]]
                            #break
                        #except:
                        #    Hardware[k][f] = "-"
                case "VCenter":
                    if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "NO":
                        Hardware[k][f] = "-"   
                    else:
                        #l = cm.togli_dominio(CMDB_Citrix[k][CMDB_field["VM_Virtualcenter"]])
                        l = cm.togli_dominio(CMDB_Citrix[k]["VM_Virtualcenter"])

                        try:
                            Hardware[k][f] = VCenter[l[0]][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"               
    i += 1

lnome = list(PDL.keys())

for k in lnome:
    Hardware[k] = {}
    for f in lfield:
        Hardware[k][f] = '-'
    Hardware[k]["nome"] = PDL[k][PDL_field["Nome CI"]]
    Hardware[k]["tipo"] = "PDL"
    Hardware[k]["dominio"] = PDL[k][PDL_field["Domain Name"]]
    Hardware[k]["cliente"] = PDL[k][PDL_field["Used By"]]
    Hardware[k]["ruolo"] = "Desktop"
    Hardware[k]["ambiente"] = "Produzione"
    Hardware[k]["virtuale"] = "NO"

#
# Scrittura file: Tabella Hardware.csv
#

y = [cm.out_path, cm.pr["OUT_Hardware_TAB"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(lfield)

f.write(riga + "\n")

lnome = list(Hardware.keys())

n = len(Hardware)
j = 0
for c in lnome:
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, list(Hardware[c].values())))

    f.write(riga + "\n")
    j += 1
f.close()
print ("\n>-----------------------------------------------------------<\n")