# Python classi dati Asset Server

import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_CMDB:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

CMDB = []
CMDB_esx = []
CMDB_field = {  "Nome CI"     : 0, 
                "OS"          : 7, 
                "DNS"         : 30, 
                "Domain Name" : 12, 
                "Is Virtual"  : 27, 
                "Numero CPU" : 15,   
                "Numero Socket" : 14, 
                "Processore" : 16, 
                "Modello" : 26, 
                "VM_Cluster" : 19, 
                "VM_Virtualcenter": 24, 
                "VM_Host" : 21,
                "VMWare_LastReportDate" : 20,
                "Bigfix_LastReportDate": 31,
                "Applicazione (lista)" : 8,
                "Ruolo" : 5,
                "Category" : 2,
                "Type" : 3,
                "Ambiente" : 6,
                "Responsabile" : 9,
                "Used By": 38,
                "Contratto" : 39,
                "server_iscloud" : 33
            }

class c_DISS:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

DISS = []
DISS_field = {"server": 0,
              "datadismissione": 2
             }

class c_PDL:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

PDL = []
PDL_field = {"Nome CI": 0,
            "Category": 2,
            "Type": 3,
            "Domain Name": 7,
            "Used By": 19
            }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


print("Procedura per la elaborazione dei dati da CMDB - Server.")

cm.check_outdir(cm.out_path)

#
# Cerco il file più recente in base al pattern indicato in Parametri.json
#
file_pattern = cm.pr["CMDB_Pattern"]
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
    if ( i < 2 ):
        i += 1
        continue
    separa = cm.trova_separa(x)
    tmp = cm.togli_apici(x, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici

    y = tmp.split(cm.cs)
    is_esx = 0
    s_ruolo = str(y[CMDB_field["Ruolo"]]).lower()
    if ( s_ruolo[:9] == "appliance" ):
        continue
    if s_ruolo[:3] == "esx":
        is_esx = 1
    nome = str(y[CMDB_field["Nome CI"]]).lower()
    if nome in nomi:
        continue
    nomi.append(nome)     # Non l'ho trovato e così lo aggiungo alla lista dei nomi univoci.
#
# Preparo la riga con tutti gli attributi/caratteristiche del server. Quelle che interessano
#
    t = []
    for c in CMDB_field:
        if c == "Nome CI": 
            t.append(nome)
        else:
            t.append(y[CMDB_field[c]])
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CMDB_field
#
    z = c_CMDB(nome, t)
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CMDB e che
# viene memorizzato nella lista di oggetti 'CMDB'
#
    if ( is_esx ):
        z.dati[6] = z.dati[5]   # --- Copio il dato di "Numero CPU" in "Numero Socket"
        z.dati[5] = y[32]       # --- In "Numero CPU" metto il valore della colonna "Server_numerocore" del file scaricato da CMDB.
        CMDB_esx.append(z)

    CMDB.append(z)
    i += 1

# -----------------------------------------  FINE ciclo sulle righe

# -----------------------------------------  Caricamento server DISMESSi

cm.files.clear()

file_pattern = cm.pr["DISMESSI_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

temp = sorted(cm.files, reverse=True)
print("\nElaborazione file " + temp[0])

fc = open(temp[0], "r")

i = 0   # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione

mesg = "Elemento [{}]"
i = 0
for x in fc:
    print('\r', mesg.format(i), end='', flush=True)
    if ( i < 2 ):
        i += 1
        continue
    separa = cm.trova_separa(x)
    tmp = cm.togli_apici(x, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici

    t = []  # Lista che contiene la riga del file elaborata e con le informazioni elencate in DISS_field

    y = tmp.split(cm.cs)
    nome = str(y[DISS_field["server"]]).lower()
    for c in DISS_field:
        if c == "server": 
            t.append(nome)
        else:
            t.append(y[DISS_field[c]])
    z = c_DISS(nome, t)
    DISS.append(z)
    i += 1

# -----------------------------------------  Caricamento Post Di Lavoro (PDL)

cm.files.clear()

file_pattern = cm.pr["PDL_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

temp = sorted(cm.files, reverse=True)
print("\nElaborazione file " + temp[0])

fc = open(temp[0], "r")

i = 0   # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione

mesg = "Elemento [{}]"
i = 0
for x in fc:
    print('\r', mesg.format(i), end='', flush=True)
    if ( i < 2 ):
        i += 1
        continue
    separa = cm.trova_separa(x)
    tmp = cm.togli_apici(x, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici

    t = []  # Lista che contiene la riga del file elaborata e con le informazioni elencate in PDL_field

    y = tmp.split(cm.cs)
    nome = str(y[PDL_field["Nome CI"]]).lower()
    for c in PDL_field:
        if c == "Nome CI": 
            t.append(nome)
        else:
            t.append(y[PDL_field[c]])
    
    trovato = 0
    n = len(PDL)
    for x in range(0, n):
        if ( PDL[x].nome == nome ):
            trovato = 1
            break
    if trovato == 1:
        continue    

    z = c_PDL(nome, t)
    PDL.append(z)
    i += 1


#
# Scrittura del file AssetServe_CMDB.csv
#

y = [cm.out_path, cm.pr["OUT_CMDB"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(CMDB_field)

f.write(riga + "\n")

n = len(CMDB)
for j in range(0, n):
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, CMDB[j].dati))
    f.write(riga + "\n")
f.close()

#
# Scrittura del file AssetCMDB_Esx.csv
#

y = [cm.out_path, cm.pr["OUT_CMDB_ESX"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(CMDB_field)

f.write(riga + "\n")

n = len(CMDB_esx)
for j in range(0, n):
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, CMDB_esx[j].dati))
    f.write(riga + "\n")
f.close()

#
# Scrittura file DISMESSI
#

y = [cm.out_path, cm.pr["OUT_DISMESSI"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(DISS_field)

f.write(riga + "\n")

n = len(DISS)
for j in range(0, n):
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, DISS[j].dati))
    f.write(riga + "\n")
f.close()

#
# Scrittura file Posti Di Lavoro
#

y = [cm.out_path, cm.pr["OUT_PDL"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(PDL_field)

f.write(riga + "\n")

n = len(PDL)
for j in range(0, n):
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, PDL[j].dati))
    f.write(riga + "\n")
f.close()
