# Python Classi dati della tabella WIN 

#from sys import exit
import csv
import Common as cm


#------------------------------------------------------------------------------
class c_Rapid7:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


Rapid7 = {}
Rapid7_Field = {
    "nome": 0,
    "virtuale": 4,
    "tipo": 5,
    "cliente": 37,
    "ambiente": 35,
    "destinazione": 9,                 
    "versione_componente": 42   #in SW_list
}

Rapid7_read = 11

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


print("Procedura per la elaborazione dei dati da Tabella HW.")


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

print("Elaborazione file " +cm.files[0])

fc = open(cm.files[0], "r")
h = 0
i = 0       # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione
j = 0       # Questo serve per poter scorrere la lista di oggetti per verficiare che non ce ne sia 
            # presente uno che contenga già le informazioni della riga in elaborazione.
t = []      # Lista che contiene la riga del file elaborata e con le informazioni elencate in CMDB_field
mesg = "Elemento [{}/{}]"
righe=fc.readlines()
del righe[0]
del righe[0]
h = len(righe)
for r in righe:
    print('\r', mesg.format(i,h), end='', flush=True)

    y = r.split(cm.cs)
    if y[41].find("rapid7") > -1:
        Software[y[0]]=y[42]    # versione componente
             
    i += 1
for k in Software:
    Rapid7[k]=[]
    for c in Rapid7_Field:
        if c == "versione_componente":
            break
        Rapid7[k].append(Hardware[k][Rapid7_Field[c]])
        
    Rapid7[k].append(Software[k]) 

# Scrittura file Tabella Rapid7

y = [cm.out_path, cm.pr["OUT_Rapid7_TAB"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(Rapid7_Field)

f.write(riga + "\n")

lnome = list(Rapid7.keys())

n = len(Rapid7)
j = 0
for c in lnome:
    print('\r', mesg.format(j, n), end='', flush=True)
    riga = cm.cs.join(map(str, Rapid7[c]))

    f.write(riga + "\n")
    j += 1
f.close()
print ("\n>-----------------------------------------------------------<\n")