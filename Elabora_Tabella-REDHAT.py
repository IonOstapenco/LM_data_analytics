# Python Classi dati della tabella REDHAT

#from sys import exit
import csv
import Common as cm



# s-a luat din elabora_HW mai nou, care elimina spatiile invizibile + schimbarea standadtrelor

# ───────────────────────────────────────────────
# Normalizare texte (fără BOM, spații inutile)
# ───────────────────────────────────────────────
def norm(s, lower=False):
    if s is None:
        return ""
    s = s.replace("\ufeff", "").strip()
    return s.lower() if lower else s


#------------------------------------------------------------------------------
class c_REDHAT:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


REDHAT = {}
REDHAT_Field = {
    "nome": 0,
    "powerstate": 26,
    "operating_system": 1,
    "virtuale": 4,
    "tipo": 5,
    "n_socket": 20,
    "n_core": 21,
    "cluster_name": 6,
    "cluster_cores": 10,
    "cluster_numhosts": 11,
    "cliente": 37,
    "ambiente": 35,
    "destinazione": 9,
    "versione_componente": 42   #in SW_list
}   

REDHAT_read = 13


class c_Hardware:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

Hardware = {}
HW_field = {
    "nome": 0,
    "operating_system": 1,
    "dominio": 0,
    "dns_name": 0,
    "virtuale": 0,
    "tipo": 0,
    "cluster_name": 0,
    "cluster_ambiente": 0,
    "cluster_cliente": 0,
    "cluster_destinazione": 0,
    "cluster_cores": 0,
    "cluster_numhosts": 0,
    "cluster_n_vms_total": 0,
    "cluster_n_vms_active": 0,
    "cluster_n_vms_win": 0,
    "hyperthreadactive": 0,
    "ha_enabled": 0,
    "drs_enabled": 0,
    "host": 0,
    "vm_hw_version": 0,
    "n_cpu": 0,
    "n_core": 0,
    "pvu_per_core": 0,
    "valore_pvu_modificato": 0,
    "valore_pvu_predefinito": 0,
    "fattore_core_oracle": 0,
    "powerstate": 0,
    "vcenter": 0,
    "vcenter_cores": 0,
    "vcenter_hosts": 0,
    "vcenter_dominio": 0,
    "vcenter_cluster": 0,
    "cpu_model": 0,
    "applicazione": 0,
    "ruolo": 0,
    "ambiente": 0,
    "responsabile": 0,
    "cliente": 0,
    "contratto": 0,
    "sito": 0
}

class c_Software:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

Software = {}
SW_field = {
    "nome": 0,
    "operating_system": 0,
    "dominio": 0,
    "dns_name": 0,
    "virtuale": 0,
    "tipo": 0,
    "cluster_name": 0,
    "cluster_ambiente": 0,
    "cluster_cliente": 0,
    "cluster_destinazione": 0,
    "cluster_cores": 0,
    "cluster_numhosts": 0,
    "cluster_n_vms_total": 0,
    "cluster_n_vms": 0,
    "cluster_n_vms_win": 0,
    "hyperthreadactive": 0,
    "ha_enabled": 0,
    "drs_enabled": 0,
    "host": 0,
    "vm_hw_version": 0,
    "n_cpu": 0,
    "n_core": 0,
    "pvu_per_core": 0,
    "valore_pvu_modificato": 0,
    "valore_pvu_predefinito": 0,
    "fattore_core_oracle": 0,
    "powerstate": 0,
    "vcenter": 0,
    "vcenter_cores": 0,
    "vcenter_hosts": 0,
    "vcenter_dominio": 0,
    "vcenter_cluster": 0,
    "cpu_model": 0,
    "applicazione": 0,
    "ruolo": 0,
    "ambiente": 0,
    "responsabile": 0,
    "cliente": 0,
    "contratto": 0,
    "sito": 0,
    "nome publisher": 0,
    "nome componente": 41,
    "versione_componente": 42,
    "versione dettagliata componente": 0,
    "percorso_di_installazione": 0,
    "nome prodotto": 0,
    "versione_prodotto": 0,
    "metrica": 0,
    "nome_edizione": 0,
    "versione_edizione": 0
}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da Tabella REDHAT.")

# Verifica directory output
cm.check_outdir(cm.out_path)

mesg = "Elemento [{}]"
mes1 = "File in caricamento: [{}]"

# Caricamento dati elaborati in precedenza
y = [cm.out_path, cm.pr["OUT_Hardware_TAB"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, Hardware, 0)

file_pattern = cm.pr["OUT_Software_TAB"]
cm.list_files_scandir(cm.out_path, file_pattern, cm.pr["Extension_end"])

print("Elaborazione file " + cm.files[0])

fc = open(cm.files[0], "r")
h = 0
i = 0   # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione
t = []  # Lista che contiene la riga del file elaborata e con le informazioni elencate in CMDB_field
mesg = "Elemento [{}/{}]"
righe = fc.readlines()
del righe[0]
del righe[0]
h = len(righe)

for r in righe:
    print('\r', mesg.format(i, h), end='', flush=True)
    y = r.split(cm.cs)
    if y[SW_field["nome componente"]].find("red hat enterprise") > -1:
        Software[y[0]] = y[SW_field["versione_componente"]]
    i += 1



# Elaborazione REDHAT

ClusterName = {}
#added
ClusterCores = {}
'''ClusterName = {}

for k in Hardware:
    sysop = Hardware[k][HW_field["operating_system"]].lower()
    if sysop.find("red hat enterprise") > -1:
        REDHAT[k] = []
        for c in REDHAT_Field:
            if c == "versione_componente":
                break
            q = Hardware[k][REDHAT_Field[c]]
            if c == "cluster_cores": #---daca este cluster cores, atunci, 
                p = Hardware[k][REDHAT_Field["cluster_name"]] 
                if p in ClusterName:
                    REDHAT[k].append('0')
                else:
                    ClusterName[p] = q
                    REDHAT[k].append(q)
            else:
                REDHAT[k].append(q)
        if k in Software:
            REDHAT[k].append(Software[k])   # versione_componente
        else:
            REDHAT[k].append("-")
            '''

ClusterCores = {}
ClusterNumHosts = {}   # <-- TREBUIE DECLARAT! -- DEVE essere dichiarato!

for k in Hardware:
    sysop = Hardware[k][HW_field["operating_system"]].lower()
    if sysop.find("red hat enterprise") > -1:

        REDHAT[k] = []

        for c in REDHAT_Field:
            if c == "versione_componente":
                break

            q = Hardware[k][REDHAT_Field[c]]
            p = Hardware[k][REDHAT_Field["cluster_name"]] #added recently --- aggiunto recente

            # --- logica pentru cluster_cores ---
            #   logica per cluster cores
            if c == "cluster_cores":
                if p in ClusterCores:
                    REDHAT[k].append('0')
                else:
                    ClusterCores[p] = q
                    REDHAT[k].append(q)

            # --- logica pentru cluster_numhosts ---
            # -- logica per cluster_numhosts ---
            elif c == "cluster_numhosts": 
                if p in ClusterNumHosts:
                    REDHAT[k].append('0')
                else:
                    ClusterNumHosts[p] = q
                    REDHAT[k].append(q)

            else:
                REDHAT[k].append(q)

        if k in Software:
            REDHAT[k].append(Software[k])
        else:
            REDHAT[k].append("-")




# Scrittura file Tabella REDHAT
y = [cm.out_path, cm.pr["OUT_REDHAT_TAB"]]
output_file = cm.dr.join(y)
f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")
print("\n\nScrittura file " + output_file)

riga = cm.cs.join(REDHAT_Field)
f.write(riga + "\n")

lnome = list(REDHAT.keys())
n = len(REDHAT)
j = 0
for c in lnome:
    print('\r', mesg.format(j, n), end='', flush=True)
    riga = cm.cs.join(map(str, REDHAT[c]))
    f.write(riga + "\n")
    j += 1
f.close()

print("\n>-----------------------------------------------------------<\n")
print("+-----------------------------------------------------------+")
print("!   Procedura Elabora_Tabella - REDHAT completata           !")
print("+-----------------------------------------------------------+")
