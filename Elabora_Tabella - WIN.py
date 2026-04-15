# Python Classi dati della tabella WIN 

#from sys import exit
import csv
import Common as cm


#------------------------------------------------------------------------------
class c_WIN:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


WIN = {}
WIN_Field = {
    "nome": 0,
    "powerstate": 26,
    "virtuale": 4,
    "tipo": 5,
    "n_cpu": 20,
    "n_core": 21,
    "cluster_name": 6,
    "cluster_cores": 10,
    "cluster_numhosts": 11,
    "cluster_n_vms_win": 14,
    "cliente": 37,
    "ambiente": 35,
    "destinazione": 9,
    "contratto": 38,
    "nome_edizione": 0,         # in SW_list
    "standard_lic_number": 0,        # calcolato
    "datacenter_lic_number": 0       # calcolato

}
WIN_read = 14

#class c_Hardware:
#    def __init__(self, nome, attributo):
#        self.nome = nome
#        self.dati = attributo

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
    "versione_componente": 0,
    "versione dettagliata componente": 0,
    "percorso_di_installazione": 0,
    "nome prodotto": 0,
    "versione_prodotto": 0,
    "metrica": 0,
    "nome_edizione": 0,
    "versione_edizione": 0
}

ClusterName = {}    # Dizionario per la verifica del nome del cluster: se il nome è già stato elaborato, per le righe successive, il numero di cluster_cores 
                    #   deve essere azzerato.

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

print("Elaborazione file " + cm.files[0])

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
    if y[SW_field["nome componente"]].find("windows server") > -1:
        if y[SW_field["nome componente"]].find("datacenter") > -1:
            Software[y[0]]="datacenter"
        if y[SW_field["nome componente"]].find("standard") > -1:
            Software[y[0]]="standard"
        if y[SW_field["nome componente"]].find("enterprise") > -1:
            Software[y[0]]="enterprise"               

   
    i += 1
lst_win = list(WIN_Field.keys())
n_lst_win = len(lst_win)
for k in Hardware:
    sysop = Hardware[k][HW_field["operating_system"]].lower()
    if (sysop.find("windows server") > -1) or (sysop.find("win20") > -1):

#        WIN[k]=[]
        WIN[k] = {}
        for c in range(0, WIN_read):
#        for c in WIN_Field:
            if lst_win[c] == "nome_edizione":
                break
            q = Hardware[k][WIN_Field[lst_win[c]]]   # valore del campo 'c' in elaborazione
            if lst_win[c] == "cluster_cores":
                p = Hardware[k][WIN_Field['cluster_name']]  # Nome del cluster.
                if p in ClusterName:
#                    WIN[k].append('0')
                    WIN[k][lst_win[c]] = '0'
                else:
                    ClusterName[p] = q
                    WIN[k][lst_win[c]] = q
            else: 
                WIN[k][lst_win[c]] = q
        if k in Software:
            WIN[k]['nome_edizione'] = Software[k]
        else: 
            WIN[k]['nome_edizione'] = '-'

# Elaborazione dei dati per il calcolo delle licenze.
#   Criteri:
#       E' stata definita la soglia di 6 macchine virtuali per ogni host ESX.
#       Tale soglia definisce il limite oltre il quale conviene licenziare i core dei server host
#           mentre al di sotto di tale soglia, conviene licenziare i core delle singole macchine virtuali

lnome = list(WIN.keys())

for c in lnome:
    n_core = int(WIN[c]['n_core']) if WIN[c]['n_core'].isnumeric() else 0
    z = int(n_core / 2)
    if WIN[c]['virtuale'] == 'SI':
        n_vmwin = int(WIN[c]['cluster_n_vms_win']) if WIN[c]['cluster_n_vms_win'].isnumeric() else 0
        n_hosts = int(WIN[c]['cluster_numhosts']) if WIN[c]['cluster_numhosts'].isnumeric() else 1     # questo valore è a denominatore quindi non può essere zero
        n_ccores = int(WIN[c]['cluster_cores']) if WIN[c]['cluster_cores'].isnumeric() else 0
        w = n_vmwin / n_hosts
        if w > 6:           # ----------------------- Il numero di macchine virtuali è tale da suggerire di licenziare i core fisici degli host.
            WIN[c]['standard_lic_number'] = 0
            WIN[c]['datacenter_lic_number'] = int(round(n_ccores / 2))
        else:               # ----------------------- Il numero di macchine virtuali è tale da suggerire di licenziare i core della singola VM.
            WIN[c]['standard_lic_number'] = cm.Minimo_lic_Win_vm if z < cm.Minimo_lic_Win_vm else z
            WIN[c]['datacenter_lic_number'] = 0            
    else:
        if WIN[c]['nome_edizione'] == 'datacenter':
            WIN[c]['standard_lic_number'] = 0
            WIN[c]['datacenter_lic_number'] = cm.Minimo_lic_Win_fs if z < cm.Minimo_lic_Win_fs else z
        else:
            WIN[c]['standard_lic_number'] = cm.Minimo_lic_Win_fs if z < cm.Minimo_lic_Win_fs else z
            WIN[c]['datacenter_lic_number'] = 0            


# Scrittura file Tabella WIN

y = [cm.out_path, cm.pr["OUT_WIN_TAB"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(WIN_Field)

f.write(riga + "\n")

lnome = list(WIN.keys())
m = list(WIN[lnome[0]].keys())
# riga = "Nome" + cm.cs + cm.cs.join(m)
riga = cm.cs.join(m)
n = len(WIN)
j = 0
for c in lnome:
    print('\r', mesg.format(j, n), end='', flush=True)
    riga = cm.cs.join(map(str, WIN[c].values()))

    f.write(riga + "\n")
    j += 1
f.close()
print ("\n>-----------------------------------------------------------<\n")
print ("+-----------------------------------------------------------+")
print ("!   Procedura Elabora_Tabella - WIN completata              !")
print ("+-----------------------------------------------------------+")
