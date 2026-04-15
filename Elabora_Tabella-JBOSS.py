# Python Classi dati della tabella JBOSS

#from sys import exit
import csv
import Common as cm


#------------------------------------------------------------------------------
class c_JBOSS:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


JBOSS = {}
JBOSS_Field = {
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
    "nome componente": 41,
    "edizione": 0,
    "versione_componente": 42   # in SW_list
}

JBOSS_read = 13


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

Software = {}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da Tabella JBOSS.")

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
i = 0
t = []
mesg = "Elemento [{}/{}]"
righe = fc.readlines()
del righe[0]
del righe[0]
h = len(righe)

for r in righe:
    print('\r', mesg.format(i, h), end='', flush=True)
    y = r.split(cm.cs)
    if y[41].find("red hat jboss") > -1:
        if y[41].find("enterprise") > -1:
            Software[y[0]] = [y[41], "enterprise", y[42]]
        elif y[41].find("web server") > -1:
            Software[y[0]] = [y[41], "web server", y[42]]
    i += 1

# Elaborazione JBOSS
ClusterName = {}

for k in Hardware:
    sysop = Hardware[k][HW_field["operating_system"]].lower()
    if sysop.find("red hat") > -1 or k in Software:
        JBOSS[k] = []
        for c in JBOSS_Field:
            if c in ["nome componente", "edizione", "versione_componente"]:
                break
            q = Hardware[k][JBOSS_Field[c]]
            if c == "cluster_cores":
                p = Hardware[k][JBOSS_Field["cluster_name"]]
                if p in ClusterName:
                    JBOSS[k].append('0')
                else:
                    ClusterName[p] = q
                    JBOSS[k].append(q)
            else:
                JBOSS[k].append(q)

        if k in Software:
            JBOSS[k].append(Software[k][0])   # nome componente
            JBOSS[k].append(Software[k][1])   # edizione
            JBOSS[k].append(Software[k][2])   # versione
        else:
            JBOSS[k].append("-")  # nome componente
            JBOSS[k].append("-")  # edizione
            JBOSS[k].append("-")  # versione

# Scrittura file Tabella JBOSS
y = [cm.out_path, cm.pr["OUT_JBOSS_TAB"]]
output_file = cm.dr.join(y)
f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")
print("\n\nScrittura file " + output_file)

riga = cm.cs.join(JBOSS_Field)
f.write(riga + "\n")

lnome = list(JBOSS.keys())
n = len(JBOSS)
j = 0
for c in lnome:
    print('\r', mesg.format(j, n), end='', flush=True)
    riga = cm.cs.join(map(str, JBOSS[c]))
    f.write(riga + "\n")
    j += 1
f.close()

print("\n>-----------------------------------------------------------<\n")
print("+-----------------------------------------------------------+")
print("!   Procedura Elabora_Tabella - JBOSS completata            !")
print("+-----------------------------------------------------------+")
