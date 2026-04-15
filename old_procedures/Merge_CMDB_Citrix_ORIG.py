# Python classi dati Asset Server CMDB, Citrix

import csv
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_CMDB:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo



CMDB_Citrix = []
CMDB_field = {  "Nome CI"     : 0, 
                "OS"          : 1, 
                "DNS"         : 2, 
                "Domain Name" : 3, 
                "Is Virtual" : 4,
                "Numero CPU" : 5,
                "Numero Socket" : 6,
                "Processore" : 7,
                "Modello" : 8,
                "VM_Cluster" : 9,
                "VM_Virtualcenter" : 10,
                "VM_Host" : 11,
                "VMWare_LastReportDate" : 12,
                "Bigfix_LastReportDate" : 13,
                "Applicazione (lista)" : 14,
                "Ruolo" : 15,
                "Category" : 16,
                "Type" : 17,
                "Ambiente" : 18,
                "Responsabile" : 19,
                "Used By" : 20,
                "Contratto" : 21,
                "server_iscloud" : 22
}

class c_Server:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

Server = []
Server_field = [
             "name",         # colonna A 1         
             "address",      # address colonna K 11      
             "cpus",         # CPUS colonna O 15  
             "description",  # descriptions AO 41  
             "funzione",     # Riepilogo pool       
             "pool"          # Riepilogo pool            
            ]

class c_Vms:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

Vms = []
Vms_field = [
            "name",           # colonna A 1               
             "address",       # colonna G 7             
             "cpus",          # colonna AF 32               
             "funzione",      # Riepilogo pool                           
             "operating_system",   # colonna U 21  
             "pool",          # Riepilogo pool               
             "power_state",   # colonna B 2        
             "running_on"     # colonna D 4                          
            ]


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Lettura dati dal CMDB - AssetServer_CMDB.csv

cm.check_outdir(cm.out_path)

y = [cm.out_path, cm.pr["OUT_CMDB"]] 

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

output_file = cm.dr.join(y)

f = open((output_file), "r")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(output_file))
print("----------------------------------------------------------------\n")

Linee = f.readlines() 

del Linee[0]
del Linee[0]
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    a = str(linea).rstrip('\n')
    y = a.split(cm.cs)
    nome = y[0]

    z = c_CMDB(nome, y)

    CMDB_Citrix.append(z)
    i += 1

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Lettura dati relativi ai server Citrix. - Server_Citrix_list.csv

y = [cm.out_path, cm.pr["OUT_Server_Citrix"]] 

output_file = cm.dr.join(y)

f = open((output_file), "r")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(output_file))
print("----------------------------------------------------------------\n")

Linee = f.readlines() 

del Linee[0]
del Linee[0]
l = list(CMDB_field.keys())
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    a = str(linea).rstrip('\n')
    y = a.split(cm.cs)
    nome = y[0]

    trovato = next(
        (o_g for o_g in CMDB_Citrix if o_g.nome == nome),
        None
    )
    try:
        trovato.dati[CMDB_field["Numero CPU"]] = y[2]
        trovato.dati[CMDB_field["Ambiente"]] = y[4]
        trovato.dati[CMDB_field["VM_Cluster"]] = y[5]
    except:
        
        t = []
#        t.append(nome)
        for k in l:
            t.append('-')
        z = c_CMDB(nome, t)
        z.dati[CMDB_field["Nome CI"]] = y[0]
        z.dati[CMDB_field["Numero CPU"]] = y[2]
        z.dati[CMDB_field["Ambiente"]] = y[4]
        z.dati[CMDB_field["VM_Cluster"]] = y[5]
        z.dati[CMDB_field["Used By"]] = 'CEDACRI'
        z.dati[CMDB_field["server_iscloud"]] = 0
        z.dati[CMDB_field["Is Virtual"]] = 'NO'
        z.dati[CMDB_field["OS"]] = 'XenServer Type'
        z.dati[CMDB_field["Type"]] = 'Server'
        z.dati[CMDB_field["Category"]] = 'Server'
        z.dati[CMDB_field["Ruolo"]] = 'CITRIX'
        z.dati[CMDB_field["Contratto"]] = 'MS SPLA'
        
        CMDB_Citrix.append(z)
    i += 1
# -----------------------------------------  FINE ciclo sulle righe

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Lettura dati relativi alle VM Citrix. - Vms_Citrix_list.csv

y = [cm.out_path, cm.pr["OUT_Vms_Citrix"]] 

output_file = cm.dr.join(y)

f = open((output_file), "r")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(output_file))
print("----------------------------------------------------------------\n")

Linee = f.readlines() 

del Linee[0]
del Linee[0]
l = list(CMDB_field.keys())
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    a = str(linea).rstrip('\n')
    y = a.split(cm.cs)
    nome = y[0]

    trovato = next(
        (o_g for o_g in CMDB_Citrix if o_g.nome == nome),
        None
    )
    try:
        trovato.dati[CMDB_field["Numero CPU"]] = y[2]
        trovato.dati[CMDB_field["Ambiente"]] = y[3]
        trovato.dati[CMDB_field["OS"]] = y[4]
        trovato.dati[CMDB_field["VM_Cluster"]] = y[5]
        trovato.dati[CMDB_field["VM_Host"]] = y[7]
    except:
       
        t = []
        for k in l:
            t.append('-')
        z = c_CMDB(nome, t)
        z.dati[CMDB_field["Nome CI"]] = y[0]
        z.dati[CMDB_field["Numero CPU"]] = y[2]
        z.dati[CMDB_field["Ambiente"]] = y[3]
        z.dati[CMDB_field["OS"]] = y[4]
        z.dati[CMDB_field["VM_Cluster"]] = y[5]
        z.dati[CMDB_field["VM_Host"]] = y[7]
        z.dati[CMDB_field["Used By"]] = 'CEDACRI'
        z.dati[CMDB_field["server_iscloud"]] = 0
        z.dati[CMDB_field["Is Virtual"]] = 'SI'
        z.dati[CMDB_field["Type"]] = 'Server'
        z.dati[CMDB_field["Category"]] = 'Server'
        z.dati[CMDB_field["Ruolo"]] = 'CITRIX'
        z.dati[CMDB_field["Contratto"]] = 'MS SPLA'

        CMDB_Citrix.append(z)
    i += 1

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Lettura dati di CMDB_ESX - AssetCMDB_Esx.csv

y = [cm.out_path, cm.pr["OUT_CMDB_ESX"]] 

output_file = cm.dr.join(y)

f = open((output_file), "r")

print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(output_file))
print("----------------------------------------------------------------\n")

Linee = f.readlines() 

del Linee[0]
del Linee[0]
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    a = str(linea).rstrip('\n')
    y = a.split(cm.cs)
    nome = y[0]
    
    trovato = next(
        (o_g for o_g in CMDB_Citrix if o_g.nome == nome),
        None
    )



#
# Scrittura del file Server_CMDB_Citrix.csv
#

y = [cm.out_path, cm.pr["OUT_CMDB_Citrix"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(CMDB_field)

f.write(riga + "\n")

n = len(CMDB_Citrix)
for j in range(0, n):
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, CMDB_Citrix[j].dati))
    f.write(riga + "\n")
f.close()

