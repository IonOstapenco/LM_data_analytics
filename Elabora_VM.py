 # Python Classi dati server VM

# Elabora i dati delle macchine virtuali (VM) provenienti da RVTools e li combina con:
# CPU (tabvCPU)
# VMware Tools (tabvTools)

#prelucreaza datele despre masini virtuale (VM) din RVTools si le combina cu :
# CPU (tabvCPU)
# Vmware Tools (tabvTools)

"""
Citește 3 surse RVTools:
•	CPU (tabvCPU) 
•	TOOLS (tabvTools) 
•	INFO (tabvInfo) 
 Normalizează și filtrează VM-urile
 face JOIN între cele 3 surse
 elimină VM-uri nedorite (test, clone etc.)
 elimină duplicate
 generează fișier final VM_list.csv

"""

#from sys import exit
import csv
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class c_CPU:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

CPU = []  # se ia din ---> RVtools_tabvCPU
CPU_field = { "VM": 0,
               "CPUs": 4,
               "Sockets": 5,
               "Cores p/s": 6
              }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_TOOLS:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

TOOLS = []    #se ia din RvTools_tabvTools --->
TOOLS_field = {"VM": 1,              
                 "VM Version": 5,      
                 "Tools": 6,           
                 "Tools Version": 7,   
                 "Required Version": 8,
                 "Upgradeable": 9,     
                 "Upgrade Policy": 10  
                }


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_VM: # structura de date pentru fisier final, de output
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

VM = [] # # --> structura fisierului final  ---> se ia din RvTools_tabvInfo
VM_field = {
    "VM": 0,
    "Powerstate": 1,
    "Template": 2,
    "SRM Placeholder": 3,
    "DNS Name": 4,
    "CPUs": 5,
    "Memory": 6,
    "Primary IP Address": 7,
    "HW version": 8,
    "Annotation": 9,
    "Datacenter": 10,
    "Cluster": 11,
    "Host": 12,
    "OS according to the configuration file": 13,
    "OS according to the VMware Tools": 14,
    "VM ID": 15,
    "VI SDK Server type": 16,
    "VI SDK API Version": 17,
    "VI SDK Server": 18,         # ---- Ultimo campo letto da RvTools
    "Sockets": 19,        # ---> campuri extra (Sockets se ia din RvTools_tabvCPU)
    "Cores p/s": 20,
    "Tools": 21,
    "Tools Version": 22, # ---> se ia probabil din RvTools_tabvTools
    "Required Version": 23, # ---> se ia probabil din RvTools_tabvTools
    "Upgradeable": 24,  # ---> se ia probabil din RvTools_tabvTools
    "Upgrade Policy": 25
    }
n_VM_field = 19

#VM_list = [
#   "VM",
#   "Powerstate",
#   "Template",
#   "SRM Placeholder",
#   "DNS Name",
#   "CPUs",
#   "Memory",
#   "Primary IP Address",
#   "HW version",
#   "Annotation",
#   "Datacenter",
#   "Cluster",
#   "Host",
#   "OS according to the configuration file",
#   "OS according to the VMware Tools",
#   "VM ID",
#   "VI SDK Server type",
#   "VI SDK API Version",
#   "VI SDK Server",
#   "Sockets",
#   "Cores p/s",
#   "Tools",
#   "Tools Version",
#   "Required Version",
#   "Upgradeable",
#   "Upgrade Policy"
#   ]
#VM_read = 19

# ------- Parole chiave che se presenti nel nome della VM indicano che deve essere scartata
#  -- cuvinte chei pentru eliminare
key_word = ["indismissione", "clone", "replica", "non_toccare", "test", "corrupt", "template", "issue_snap"]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da RVTOOLS - tabvCPU.")

cm.check_outdir(cm.out_path)

#
# Cerco il file più recente in base al pattern indicato in Parametri.json
#
# ===================================================================
#                   PROCESAREA CPU (tabvCPU)
# ==================================================================


#               --- CAUTARE FISIER ------
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_CPU_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

# --> probabil aici sa modific cu lambda expression
for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
    for c in CPU_field:
        CPU_field[c] = 0
    fc = open(w, "r")
    Linee = fc.readlines()
    separa = cm.trova_separa(Linee[0])
    tmp = cm.togli_apici(Linee[0], separa)  # --- Linee[0] contiene l'intestazione delle colonne.
    y = tmp.split(cm.cs)   # ----------- Separo i campi dell'intestazione
    n = len(y)
    i = 0
    for c in y:
        # --- > Detectare header + mapare
        if ( c in CPU_field ):
            CPU_field[c] = i    # ---- Memorizzo la posizione del campo che mi interessa per questo file.
        i += 1
    del Linee[0]    # ------------------ Elimino la prima riga in quanto già elaborata
    i = 0
    for linea in Linee:
        print('\r', mesg.format(i), end='', flush=True)

#
# Preparo la riga con tutti gli attributi/caratteristiche del server. Quelle che interessano
#
        tmp = cm.togli_apici(linea, separa)
        y = tmp.split(cm.cs)
        nome = str(y[CPU_field["VM"]]).lower() # --> Procesare rânduri
        t = []  # --> lista pentru CPU
        for c in CPU_field:
            t.append(y[CPU_field[c]])
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CPU_field
#
        z = c_CPU(nome, t)
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CPU e che
# viene memorizzato nella lista di oggetti 'CPU'
#
        CPU.append(z)
        i += 1

# -----------------------------------------  FINE ciclo sulle righe

#
# Scrittura file intermedio: CPU_list.csv
#

cm.scrivi_dati("OUT_CPU", CPU_field, CPU)

# -----------------------------------------  FINE ciclo sulle righe

print("Procedura per la elaborazione dei dati da RVTOOLS - tabvTools.")

#
# Cerco il file più recente in base al pattern indicato in Parametri.json
#
cm.files = []
# Căutare fișier
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Tools_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
    for c in TOOLS_field:
        TOOLS_field[c] = 0

    fc = open(w, "r")
    Linee = fc.readline()
    separa = cm.trova_separa(Linee)
    fc.close()

# =============================================================
#  PROCESAREA TOOLS (tabvTools)
# ----- =============================================================
    with open(w,  mode ='r') as file:
        TOOLS_righe = csv.DictReader(file, delimiter=separa, quotechar='"')
        for riga in TOOLS_righe:
            nome = str(riga["VM"]).lower() # --> Procesare
            t = []
            for c in TOOLS_field:  # --> se extrag valori
                t.append(riga[c])
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CPU_field
#
            z = c_TOOLS(nome, t)
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CPU e che
# viene memorizzato nella lista di oggetti 'CPU'
#
            TOOLS.append(z)
            i += 1

# -----------------------------------------  FINE ciclo sulle righe

#
# Scrittura file intermedio: TOOLS_list.csv
#

cm.scrivi_dati("OUT_TOOLS", TOOLS_field, TOOLS)

#
# ----------------------------------------------------------------------------
#

print("Procedura per la elaborazione dei dati da RVTOOLS - tabvInfo.csv")

#
# Cerco i file in base al pattern indicato in Parametri.json
#
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Info_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"


# ==================================================================
# PROCESAREA VM (tabvInfo) 
# ===================================================================
for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
#    for c in VM_field:
#        VM_field[c] = 0

    fc = open(w, "r")
    Linee = fc.readline()
    separa = cm.trova_separa(Linee)
    fc.close()

    with open(w,  mode ='r') as file:
        i = 0
        VM_righe = csv.DictReader(file, delimiter=separa, quotechar='"')
        for riga in VM_righe:
            print('\r', mesg.format(i), end='', flush=True)
            nome = str(riga["VM"]).lower() # ---> pentru fiecare VM


#============================================================

 

#==================================================================

#
# Cerchiamo se nel nome della macchina compare una delle parole chiavi elencate in key_word
#  se verifica daca \cheile din lista se gaseste in numele masinei 
            trovato = 0
            for x in key_word:
                # ============================================================
                # FILTRARE VM-uri 
                # =============================================================
                if nome.find(x) >= 0: # --> returneaza pozitia unde apare x sa -1 daca NU APARE
                     #c ---> daca s-a gasit, atunci se elimina cheile
                    trovato = 1
            if ( trovato == 1):  # cred ca se putea mai simplu 
                """
                if any(x in nome for x in key_word):
                    continue
                """
                continue # --> un fel de skip, sare peste cuvant din lista de chei de exlucdere
            l = list(VM_field.keys()) 
            t = []
            t.append(nome)
            for k in range(1, n_VM_field):
                t.append(riga[l[k]])

#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CPU_field
#
            z = c_VM(nome, t)
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CPU e che
# viene memorizzato nella lista di oggetti 'CPU'

# ===========================================================================
# 6️⃣ MERGE CU CPU 
#==============================================================================

            trovato = next(
                (o_g for o_g in CPU if o_g.nome == nome),
                None
            )
            try:
                z.dati[VM_field["CPUs"]] = trovato.dati[1]
                z.dati.append(trovato.dati[2])
                z.dati.append(trovato.dati[3])
            except: 
                z.dati.append(0)
                z.dati.append(0)
#@========================================================

# 7️⃣ MERGE CU TOOLS 

# =======================================================
            trovato = next(
                (o_g for o_g in TOOLS if o_g.nome == nome),
                None
            )
            try:
                z.dati.append(trovato.dati[2])    # "Tools"
                z.dati.append(trovato.dati[3])    # "Tools Version"
                z.dati.append(trovato.dati[4])    # "Required Version"
                z.dati.append(trovato.dati[5])    # "Upgradeable"
                z.dati.append(trovato.dati[6])    # "Upgrade Policy"
            except:  # --> daca nu se gaseste --- se inscrie 0
                z.dati.append(0)
                z.dati.append(0)
                z.dati.append(0)
                z.dati.append(0)
                z.dati.append(0)

# 
# Verifichiamo che questo nome di VM non sia già stato elaborato.
#

# =============================================
#   8️⃣ ELIMINARE DUPLICATE
#============================================

# --> voi incerca sa utilizez doar dropduplicates
            trovato = 0
            n = len(VM)
            for x in range(0, n):
                if ( VM[x].nome == nome ):
                    trovato = 1
                    break
            if trovato == 1:
                continue    
# =================================
# SALVAREA FINALA
# ==============================
            VM.append(z)
            i += 1

# -----------------------------------------  FINE ciclo sulle righe


#
# Scrittura del file VM_list.csv
#


cm.scrivi_dati("OUT_VM", VM_field, VM)

print ("+-----------------------------------------------------------+")
print ("!   Procedura Elabora_VM completata                         !")
print ("+-----------------------------------------------------------+")
