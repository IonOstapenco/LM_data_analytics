# Python Classi dati della tabella Oracle 

#from sys import exit
import csv
import Common as cm


#------------------------------------------------------------------------------

class c_Oracle:
    def __init__(self, nome, dati):
        self.nome = nome
        self.datihw = dati
        self.sw = []

    def software(self, dati):
        self.sw.append(dati)


Oracle = {}
Oracle_Field = {
    "Nome computer": 0,
    "Nome": 1,
    "Versione": 2,
    "Edizione": 3,
    "Sistema operativo": 4,
    "Funzione": 5,
    "SID": 6,
    "AIX Full OS Level": 7,
    "NumeroCore": 8,
    "NumeroCore x Socket": 9,
    "Domain": 10,
    "Tipo di computer": 11,
    "NumeroSocket": 12,
    "Processore": 13,
    "Core partizione": 14,
    "Fattore core Oracle": 15,
    "Socket attivi del server": 16,
    "ambiente": 35,       # da Tabella HW - numero della relativa colonna nel report Tabella_HW
    "contratto": 38,      # da Tabella HW
    "cliente":  37,       # da Tabella HW
#    "Funzione - diagnostics pack": 20,    # Campo per la prima feature a pagamento installata sul server con versione Enterprise
#    "Funzione - tuning pack": 21,    # Campo per la seconda feature a pagamento installata sul server con versione Enterprise
#    "Funzione - advanced compression": 22,    # Campo per la terza feature a pagamento installata sul server con versione Enterprise
#    "Funzione - real application clusters": 23,    # Campo per la quarta feature a pagamento installata sul server con versione Enterprise
#    "Funzione - partitioning": 24     # Campo per la quinta feature a pagamento installata sul server con versione Enterprise
}

Hardware = {}
HW_field =  {  "nome": 0,
				"operating_system": 1,
				"dominio":2,
				"dns_name":3,
				"virtuale":4,
				"tipo":5,
				"cluster_name":6,
				"cluster_ambiente":7,
				"cluster_cliente":8,
				"cluster_destinazione":9,
				"cluster_cores":10,
				"cluster_numhosts":11,
				"cluster_n_vms_total": 12,
				"cluster_n_vms_active": 13,
				"cluster_n_vms_win": 14,
				"hyperthreadactive": 15,
				"ha_enabled": 16,
				"drs_enabled": 17,
				"host": 18,
				"vm_hw_version": 19,
				"n_cpu": 20,
				"n_core": 21,
				"pvu_per_core" : 22,
				"valore_pvu_modificato": 23,
				"valore_pvu_predefinito": 24,
				"fattore_core_oracle": 25,
				"powerstate": 26,
				"vcenter": 27,
				"vcenter_cores": 28,
				"vcenter_hosts": 29,
				"vcenter_dominio": 30,
				"vcenter_cluster": 31,
				"cpu_model": 32,
				"applicazione": 33,
				"ruolo": 34,
				"ambiente": 35,
				"responsabile": 36,
				"cliente": 37,
				"contratto": 38,
				"sito": 39
}

BGFX_Field = {              # Descrizione tracciato del report ICTG-0-database-oracle- 
    "Nome computer": 0,     # Le sole colonne che ci interessano
    "nome": 1,
    "Versione": 2,
    "Edizione": 3,
    "Sistema operativo": 4,
    "Funzione": 5,
    "SID": 6,
    "AIX Full OS Level": 8,
    "NumeroCpu": 9,
    "NumeroCore": 10,
    "Domain": 11,
    "Tipo di computer": 12,
    "NumeroSocket": 13,
    "Processore": 14,
    "Core partizione": 15,
    "Fattore core Oracle": 16,
    "Socket attivi del server": 17
}

Funzioni = {}

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



print("Procedura per la elaborazione dei dati da Database - Oracle BIGFIX.")

cm.check_outdir(cm.out_path)

#
# Cerco il file più recente in base al pattern indicato in Parametri.json
#
file_pattern = cm.pr["Oracle_Database_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

temp = sorted(cm.files, reverse=True)
print("Elaborazione file " + temp[0])

fc = open(temp[0], "r")

i = 0   # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione
j = 0   # Questo serve per poter scorrere la lista di oggetti per verficiare che non ce ne sia 
        # presente uno che contenga già le informazioni della riga in elaborazione.
t = []  # Lista che contiene la riga del file elaborata e con le informazioni elencate in CMDB_field
nomi = [] # Lista dei soli nomi, rende molto più veloce la ricerca di un nome già presente
mesg = "Elemento [{}]"
s_ruolo = ''

for x in fc:
    print('\r', mesg.format(i), end='', flush=True)
    if ( i < 1 ):
        i += 1
        continue
    a = x.rstrip('\n')
    separa = cm.trova_separa(a)
    tmp = cm.togli_apici(a, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici

    y = tmp.split(cm.cs)
    t = []
    for c in BGFX_Field:
        if c == "ambiente":
            break
        t.append(str(y[BGFX_Field[c]]).lower())
        
    nome = t[0]
    l = cm.togli_dominio(nome)
    
    nome = l[0]
    del t[0]
    t.insert(0, nome)
    if nome in Hardware:
        t.append(Hardware[nome][Oracle_Field["ambiente"]])
        t.append(Hardware[nome][Oracle_Field["contratto"]])
        t.append(Hardware[nome][Oracle_Field["cliente"]])
    else:
        t.append("-")
        t.append("-")
        t.append("-")
    for z in range(0, 15):
        t.append(' ')

    if nome not in Oracle:
        Oracle[nome] = c_Oracle(nome, t)
    Oracle[nome].software(t[Oracle_Field["Funzione"]])
    i += 1
k = 20
for c in Oracle:
    l = len(Oracle[c].sw)
    edz = Oracle[c].datihw[Oracle_Field["Edizione"]]
    if (edz.find("standard") > -1) or (edz.find("express") > -1):
        continue
    else:
        for i in range(0, l):
            r = str(Oracle[c].sw[i])
            if len(r) > 36:
                r = r[36:]
                if r not in Funzioni:
                    Funzioni[r] = k
                    k += 1
                Oracle[c].datihw[Funzioni[r]] = r


# Scrittura file Tabella Oracle

y = [cm.out_path, cm.pr["OUT_Oracle_TAB"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

l = Funzioni.keys()
riga = cm.cs.join(Oracle_Field)
riga = riga + cm.cs + cm.cs.join(l)

f.write(riga + "\n")

lnome = list(Oracle.keys())

n = len(Oracle)
j = 0

for c in lnome:
    print('\r', mesg.format(j, n), end='', flush=True)
    s = "|".join(map(str,Oracle[c].datihw))
    f.write(s + "\n")
    j += 1
f.close()
print ("\n>-----------------------------------------------------------<\n")
