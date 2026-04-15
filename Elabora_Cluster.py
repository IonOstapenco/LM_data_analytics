# Python Classi dati dei Cluster 

"""
 Citește VM_list.csv
 calculează statistici VM pe cluster
 citește RVTools (tabvCluster)
 face JOIN între Cluster și VM
 calculează statistici pe vCenter
 generează:
•	Cluster_list.csv
•	Vcenter_list.csv

"""
#from sys import exit
import csv
import Common as cm


# funzione per rimuovere il BOM dalle stringhe
# f-tie de stergere BOM
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()

# funzione per la normalizzazione / caricamento dei valori
#!! cream functie pentru convertire // incarcare 
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# classe che rappresenta un oggetto Cluster con i suoi attributi
class c_Cluster:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

# lista che conterrà tutti gli oggetti Cluster
Cluster = []
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

# numero di campi letti dal file cluster
Cluster_read = 14

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# dizionario che conterrà i dati aggregati dei vCenter
VCenter = {}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#
# caricamento dei dati dal file VM_list
#
# Caricamento dei dati da VM_list
#

cm.check_outdir(cm.out_path)

# dizionario che memorizza le statistiche delle VM per cluster
VM = {}

# =============================================================

# 3️⃣ PRELUCRARE VM_list 

# ============================================================

file_path = cm.out_path + cm.dr + "VM_list.csv"
f = open(file_path, "r")
Linee = f.readlines()

# eliminazione delle prime due righe (header + separatore)
# -- > sarim peste separatoare si header, adica sterge
del Linee[0]
del Linee[0]

# elaborazione delle righe del file VM_list

# pentru fiecare VM extragem powerstate, cluster name, OS according to the VMware Tools
for linea in Linee:
    y = linea.split(cm.cs) # --> separator descris in Common.py 
    a = str(y[1]).lower() # powerstate
    b = str(y[11]).lower() # cluster name
    c = y[14] # --> coloana OS according to the VMware Tools

    if b in VM:
        VM[b]["nVM"] += 1

        if a == "poweredon":
            VM[b]["nVM active"] += 1
# logica pentru windows
        if c.find("Windows") >= 0: # daca in coloana OS se contine "Windows"
            VM[b]["nVM Windows"] += 1 # atunci creste counter, nVM Windows --> camp calculat, se aseamana cu HashMap ca in Java(key, value)

    else: 
        VM[b] = {}
        VM[b] = {"nVM": 1,
                 "nVM active": 0,
                 "nVM Windows": 0
                 }

        if a == "poweredon":
            VM[b]["nVM active"] += 1

        if c.find("Windows") >= 0:
            VM[b]["nVM Windows"] += 1   
                   
                   
                   
 # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =====================================================================
# 4️⃣ PROCESAREA CLUSTER (RVTools)
# -======================================================================
print("Procedura per la elaborazion Cluster_liste dei dati da RVTOOLS - tabvCluster.csv")

#
# ricerca dei file secondo il pattern indicato in Parametri.json
#
# Cerco i file in base al pattern indicato in Parametri.json

# ==============================================================
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Cluster_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")

    # reset della posizione dei campi
    for c in Cluster_field:
        Cluster_field[c] = 0

    fc = open(w, "r")
    Linee = fc.readlines()

    # rilevazione del separatore utilizzato nel file
    separa = cm.trova_separa(Linee[0])
    # -----------------------------------------------------------------
    # 4b. Detectare header
    # -----------------------------------------------------------------
    # rimozione apici dalla riga di intestazione
    tmp = cm.togli_apici(Linee[0], separa)  # --- Linee[0] contiene l'intestazione delle colonne.

    # separazione dei campi dell'intestazione
    y = tmp.split(cm.cs)   # ----------- Separo i campi dell'intestazione

    n = len(y)
    i = 0

    # identificazione della posizione dei campi di interesse
    for c in y:
        if ( c in Cluster_field ):
            Cluster_field[c] = i    # ---- Memorizzo la posizione del campo che mi interessa per questo file.
        i += 1

    # eliminazione della riga di intestazione già elaborata
    del Linee[0]    # ------------------ Elimino la prima riga in quanto già elaborata

    i = 0

    # ciclo sulle righe del file
    for linea in Linee:

        print('\r', mesg.format(i), end='', flush=True)

        tmp = cm.togli_apici(linea, separa)
        y = tmp.split(cm.cs)

        # estrazione nome cluster
        nome = str(y[Cluster_field["Name"]]).lower()

        # separazione nome e dominio
        l = cm.togli_dominio(nome)
        nome = l[0]

        if (l[1]== '' ):
            dominio = '-'
        else:
            dominio = l[1]

        # costruzione lista campi selezionati
        l = list(Cluster_field.keys())
        t = []

        for c in range(0, Cluster_read):
            t.append(y[Cluster_field[l[c]]])

#
# la lista 't' contiene solo i campi selezionati
# e definiti nella struttura Cluster_field
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CMDB_field
#

        # creazione oggetto cluster
        z = c_Cluster(nome, t)
# ====================================================================

#  5️⃣ ENRICHMENT (ÎMBOGĂȚIRE DATE) 
# =-===================================================================
        # estrazione informazioni del vCenter
        l = cm.togli_dominio(z.dati[13])
        z.dati.append(l[0])
        z.dati.append(l[1])

        # aggiunta statistiche VM al cluster
        # adaugam statistici VM in cluster
        if nome in VM:  # daca nome este in VM, atunci adaugam
            z.dati.append( VM[nome]["nVM"])
            z.dati.append( VM[nome]["nVM active"])
            z.dati.append( VM[nome]["nVM Windows"])
        else: 
            z.dati.append(0)
            z.dati.append(0)
            z.dati.append(0)

#
# verifica e aggiornamento delle statistiche per il file Vcenter_list
#
# Verifica e aggiornamento dati per Vcenter_list.
# ==================================================================
#6️⃣ AGREGARE VCenter 
# ==================================================================
    # --------- 6a. Extrage date
    # ---------------------------------------------
        v = z.dati[14]          # --- Nome del vcenter
        a = int(z.dati[4])      # --- NumCpuCores
        b = int(z.dati[1])      # --- NumHosts
        c = z.dati[15]          # --- Dominio del vcenter

        if v in VCenter:
            VCenter[v]["Cluster"] += 1
            VCenter[v]["Core Totali"] += a
            VCenter[v]["Host"] += b
        else: 
            VCenter[v] = {}
            VCenter[v] = {"Cluster": 1,
                             "Core Totali": 0,
                             "Host": 0,
                             "Dominio": ''
                            }

            VCenter[v]["Core Totali"] += a
            VCenter[v]["Host"] += b   
            VCenter[v]["Dominio"] = c

#
# 'z' è l'oggetto creato dalla classe c_Cluster
# che viene memorizzato nella lista Cluster
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CMDB e che
# viene memorizzato nella lista di oggetti 'CMDB'
#

        Cluster.append(z)
        i += 1

# -----------------------------------------  FINE ciclo sulle righe


#
# scrittura del file Cluster_list.csv
#
# Scrittura del file Cluster_list.csv
#

cm.scrivi_dati("OUT_CLUSTER", Cluster_field, Cluster)

#
# scrittura del file "Vcenter_list.csv" dal dizionario VCenter
#
# -- Scrittura del file "Vcenter_list.csv" dal dizionario VCenter
#

y = [cm.out_path, cm.pr["OUT_VCENTER"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

l = list(VCenter.keys())
m = list(VCenter[l[0]].keys())

riga = "Nome" + cm.cs + cm.cs.join(m)

f.write(riga + "\n")

n = len(VCenter)

for j in range(0, n):

    print('\r', mesg.format(j), end='', flush=True)

    riga = l[j] + cm.cs + cm.cs.join(map(str, VCenter[l[j]].values()))

    f.write(riga + "\n")

f.close()