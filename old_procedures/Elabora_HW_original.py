 # Python Classi dati della tabella HW 

#from sys import exit
import csv
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


Hardware = {}
Hardware_field = {
    "nome": {"CMDB_Citrix": 0, "BGFX": 1},                                            
    "operating_system": {"CMDB_Citrix": 1, "BGFX": 2, "CMDB_esx": 1, "VM": 14},     
    "dominio": {"BGFX": 26, "CMDB_Citrix": 3, "HOST": 23},                       
    "dns_name": {"CMDB_Citrix": 2, "BGFX": 3, "VM": 4},
    "virtuale": {"CMDB_Citrix": 4, "BGFX": 14},             
    "tipo": {"CMDB_Citrix": 17},                                          
    "cluster_name": {"Cluster": 0, "CMDB_Citrix": 9},           
    "cluster_ambiente": {"Cluster": 10},      
    "cluster_cliente": {"Cluster": 11},          
    "cluster_destinazione": {"Cluster": 12},     
    "cluster_cores": {"Cluster": 4, "BGFX": 28},       
    "cluster_numhosts": {"Cluster": 1},       
    "cluster_n_vms_total": {"Cluster": 16},
    "cluster_n_vms": {"Cluster": 17},  
    "cluster_n_vms_win": {"Cluster": 18},
    "hyperthreadactive": {"HOST": 8},              
    "ha_enabled": {"Cluster": 6},               
    "drs_enabled": {"Cluster": 7},               
    "host": {"VM": 12, "CMDB_Citrix": 11, "BGFX": 31},
    "vm_hw_version": {"VM": 8},         
    "n_cpu": {"BGFX": 7, "CMDB_Citrix": 6},                  
    "n_core": {"VM": 5, "BGFX": 6, "CMDB_Citrix": 6},                             
    "pvu_per_core": {"BGFX": 21},             
    "valore_pvu_modificato": {"BGFX": 22},      
    "valore_pvu_predefinito": {"BGFX": 23},     
    "fattore_core_oracle": {"BGFX": 24},       
    "powerstate": {"VM": 1},                
    "vcenter": { "CMDB_Citrix": 11, "VM": 16, "Cluster": 13},                 
    "vcenter_cores":{"VCenter": 2},        
    "vcenter_hosts":{"VCenter": 3},        
    "vcenter_dominio":{"VCenter": 4},      
    "vcenter_cluster":{"VCenter": 1},      
    "cpu_model": {"BGFX": 17, "CMDB_Citrix": 8},              
    "applicazione": {"CMDB_Citrix": 14},            
    "ruolo": {"CMDB_Citrix": 15},                   
    "ambiente": {"CMDB_Citrix": 18 },                                 
    "responsabile": {"CMDB_Citrix": 19},                              
    "cliente":{"CMDB_Citrix": 20},                 
    "contratto": {"CMDB_Citrix": 21},                     
    "sito": {"HOST": 1, "VM": 10}
}


BGFX = {}
BGFX_field = {"Stato": 0,
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

CMDB_Citrix = {}
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
                "Bigfix_LastReportDate": 13,
                "Applicazione (lista)" : 14,
                "Ruolo" : 15,
                "Category" : 16,
                "Type" : 17,
                "Ambiente" : 18,
                "Responsabile": 19,
                "Used By": 20,
                "Contratto" : 21,
                "server_iscloud" : 22
            }

VM = {}
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

HOST = {}
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

Cluster = {}
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
 
VCenter = {}
VCenter_field = {"Nome": 0,
           "Cluster": 1,
           "Core Totali": 2,
           "Host": 3,
           "Dominio": 4
           }

DISS = {}
DISS_field = {"server": 0,
              "datadismissione": 2
           }

PDL = {}
PDL_field = {"Nome CI": 0,
             "Category": 1,
             "Type": 2,
             "Domain Name": 3,
             "Used By": 4
            }


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Caricamento dati elaborati in precedenza

cm.check_outdir(cm.out_path)

mesg = "Elemento [{}]"
mes1 = "File in caricamento: [{}]"

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

lnome = list(CMDB_Citrix.keys())        # Questi sono i nomi del server elencati nella lista unita tra CMDB e Citrix

lfield= list(Hardware_field.keys())     # Questi sono i nomi dei campi che dobbiamo compilare per Tabella HW.
i = 0
for k in lnome:                         # 'k' contiene il nome del server, dall'elenco CMDB_Citrix, in fase di elaborazione.
    print('\r', mesg.format(i), end='', flush=True)
    Hardware[k] = {}
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
                    if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "SI":
                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = HOST[k][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"
                case "VM":
                    if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "NO":
                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = VM[k][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"
                case "Cluster":
                    if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "NO":
                        Hardware[k][f] = "-"
                    else:
                        try:
                            Hardware[k][f] = Cluster[CMDB_Citrix[k][CMDB_field["VM_Cluster"]]][Hardware_field[f][a]]
                            break
                        except:
                            Hardware[k][f] = "-"
                case "VCenter":
                    if CMDB_Citrix[k][CMDB_field ["Is Virtual"]] == "NO":
                        Hardware[k][f] = "-"   
                    else:
                        l = cm.togli_dominio(CMDB_Citrix[k][CMDB_field["VM_Virtualcenter"]])
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