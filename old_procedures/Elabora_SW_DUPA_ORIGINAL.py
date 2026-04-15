 # Python Classi dati della tabella SW 

#from sys import exit
import csv
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class AssetSW:
    def __init__(self, dati):
        self.datisw = dati

class c_TABSW:
    def __init__(self, nome, dati):
        self.nome = nome
        self.datihw = dati
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))


Software = {}
SW_field = {
    "nome": {"Hardware":0},                                            
    "operating_system": {"Hardware":1},      
    "dominio": {"Hardware": 2},
    "dns_name":  {"Hardware":3}, 
    "virtuale":  {"Hardware":4},             
    "tipo": {"Hardware":5},                                      
    "cluster_name":  {"Hardware":6},      
    "cluster_ambiente": {"Hardware":7},   
    "cluster_cliente":  {"Hardware":8},        
    "cluster_destinazione":  {"Hardware":9},  
    "cluster_cores": {"Hardware":10},        
    "cluster_numhosts":  {"Hardware":11},     
    "cluster_n_vms_total":  {"Hardware":12}, 
    "cluster_n_vms":  {"Hardware":13}, 
    "cluster_n_vms_win":  {"Hardware":14}, 
    "hyperthreadactive": {"Hardware":15},           
    "ha_enabled":  {"Hardware":16},           
    "drs_enabled":  {"Hardware":17},              
    "host":  {"Hardware":18}, 
    "vm_hw_version":  {"Hardware":19},        
    "n_cpu":  {"Hardware":20},                   
    "n_core":  {"Hardware":21},                             
    "pvu_per_core":  {"Hardware":22},             
    "valore_pvu_modificato":  {"Hardware":23},     
    "valore_pvu_predefinito": {"Hardware":24},    
    "fattore_core_oracle": {"Hardware":25},     
    "powerstate": {"Hardware":26},               
    "vcenter":  {"Hardware":27},           
    "vcenter_cores": {"Hardware":28},         
    "vcenter_hosts": {"Hardware":29},        
    "vcenter_dominio": {"Hardware":30},     
    "vcenter_cluster": {"Hardware":31},     
    "cpu_model": {"Hardware":32},             
    "applicazione": {"Hardware":33},           
    "ruolo":  {"Hardware":34},                    
    "ambiente":  {"Hardware":35},                                 
    "responsabile": {"Hardware":36},                              
    "cliente": {"Hardware":37},                
    "contratto":  {"Hardware":38},                     
    "sito":  {"Hardware": 39},
#
# La parte di dati che provengono da "Tabella_HW" è memorizzata in self.datihw della classe c_TABSW
#
    "nome publisher": {"BGFXSW": 0, "CMDBSW": 1},
    "nome componente": {"BGFXSW": 1, "CMDBSW": 0},
    "versione_componente": {"BGFXSW": 2, "CMDBSW": 2},
    "versione dettagliata componente": {"BGFXSW": 3},
    "percorso_di_installazione": {"BGFXSW": 4},
    "nome prodotto": {"BGFXSW": 5},
    "versione_prodotto": {"BGFXSW": 6},
    "metrica" : {"BGFXSW": 7},
    "nome_edizione": 8,
    "versione_edizione": 9
#
# La parte di dati che provengono dalle righe di software (CMDB oppure BIGFIX) è memorizzata in self.datisw della classe AssetSW
#
}
n_SW_field = 42

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

class c_BGFXSW:
    def __init__(self, nome):
        self.nome = nome
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))


BGFXSW = {}
BGFXSW_field = {"Nome computer" :0,
                "Nome publisher" :2,
                "Nome componente" :3,
                "versione_componente" :4,
                "Versione dettagliata componente" :5,
                "percorso_di_installazione" :7,
                "Nome prodotto" :8,
	            "versione_prodotto" :9,
  	            "metrica" :10
             }

class c_CMDBSW:
    def __init__(self, nome):
        self.nome = nome
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))


CMDBSW = {}
CMDBSW_field = {"server"     : 0, 
                "software"     : 4, 
                "manufacturer_name_" : 9, 
                "version_number" : 10              
             }
# ------- Parole chiave che se presenti nel nome della VM indicano che deve essere scartata

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Caricamento dati elaborati in precedenza

cm.check_outdir(cm.out_path)

mesg = "Elemento [{}]"
mes1 = "File in caricamento: [{}]"

y = [cm.out_path, cm.pr["OUT_Hardware_TAB"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, Hardware, 0)

 # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per il caricamento delle parole e dei nome per individuare i prodotti NON a pagamento.")

mcrsft_kywrd_2_xcld = []
mcrsft_nomi_2_xcld  = [] 
ibm_kywrd_2_xcld    = []
ibm_nomi_2_xcld     = []
vmwr_nomi_2_xcld    = []
vmwr_kywrd_2_xcld   = []
orcl_nomi_2_xcld    = []
rdht_nomi_2_xcld    = []

y = [cm.exc_path]

# Caricamento 'IBM_keyword.csv'

z = y[:]
z.append("IBM_keyword.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    ibm_kywrd_2_xcld.append(l)

# Caricamento 'IBM_nomi.csv'

z = y[:]
z.append("IBM_nomi.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    ibm_nomi_2_xcld.append(l)

# Caricamento 'Microsoft_keyword.csv' 

z = y[:]
z.append("Microsoft_keyword.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    mcrsft_kywrd_2_xcld.append(l)

# Caricamento 'Microsoft_nomi.csv'

z = y[:]
z.append("Microsoft_nomi.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    mcrsft_nomi_2_xcld.append(l)

# Caricamento 'Oracle_nomi.csv'

z = y[:]
z.append("Oracle_nomi.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    orcl_nomi_2_xcld.append(l)

# Caricamento 'RedHat_nomi.csv'

z = y[:]
z.append("RedHat_nomi.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    rdht_nomi_2_xcld.append(l)

# Caricamento 'VMware_keyword.csv'

z = y[:]
z.append("VMware_keyword.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    vmwr_kywrd_2_xcld.append(l)

# Caricamento 'VMware_nomi.csv'

z = y[:]
z.append("VMware_nomi.csv")
input_file = cm.dr.join(z)
fc = open(input_file, 'r')
Linee = fc.readlines()
print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(input_file))
print("----------------------------------------------------------------\n")
i = 0
for linea in Linee:
    print('\r', mesg.format(i), end='', flush=True)
    i += 1
    l = linea.replace('\n', '')
    vmwr_nomi_2_xcld.append(l)


 # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da BIGFIX - Classificazione Software.")

#
# Cerco il file più recente in base al pattern indicato in Parametri.json
#

file_pattern = cm.pr["BFGX_SW_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

temp = sorted(cm.files, reverse=True)
print("Elaborazione file " + temp[0])

fc = open(temp[0], "r")
h = 0
i = 0       # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione
j = 0       # Questo serve per poter scorrere la lista di oggetti per verficiare che non ce ne sia 
            # presente uno che contenga già le informazioni della riga in elaborazione.
t = []      # Lista che contiene la riga del file elaborata e con le informazioni elencate in CMDB_field
righe_escluse = []   # Lista di appoggio per verificare se quel server è già stato elaborato.
mesg = "Elemento [{}/{}]"
for r in fc:
    print('\r', mesg.format(i,h), end='', flush=True)
    h += 1
    if ( i < 1 ):
        i += 1
        righe_escluse.append(r)
        continue
    separa = cm.trova_separa(r)
    tmp = cm.togli_apici(r, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici
#
    y = tmp.split(cm.cs)

#
# Verifica che il nome del prodotto e/o del componente non contenga una delle parole che lo possono far escludere
#
    nome_publisher = y[BGFXSW_field["Nome publisher"]].lower()
    nome_prodotto = y[BGFXSW_field["Nome prodotto"]]

    x = cm.cerca_elemento(cm.pr["Vendor"], nome_publisher, -1, 1, -1)
    if x < 0:
        righe_escluse.append(r)
        continue

    match nome_publisher:
        case 'microsoft':
            x = cm.cerca_elemento(mcrsft_kywrd_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
            x = cm.cerca_elemento(mcrsft_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
        case 'ibm':
            x = cm.cerca_elemento(ibm_kywrd_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
            x = cm.cerca_elemento(ibm_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
        case 'oracle':
            x = cm.cerca_elemento(orcl_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
        case 'vmware':
            x = cm.cerca_elemento(vmwr_kywrd_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
            x = cm.cerca_elemento(vmwr_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue
        case 'red hat':
            x = cm.cerca_elemento(rdht_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(r)
                continue

    t = []
    for c in BGFXSW_field:
        t.append(y[BGFXSW_field[c]].lower())
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in BFGXSW_field dopo aver eliminato il primo elemento, cioè il nome della macchina
#
    nome = t[BGFXSW_field["Nome computer"]]
    del t[0]
    if nome not in BGFXSW:
        BGFXSW[nome] = c_BGFXSW(nome)
    BGFXSW[nome].software(t)

    i += 1

#
# ------------------------------------------------------- fine ciclo sulle righe
#

#
# Scrittura del file ICTG-SW.csv
#

y = [cm.out_path, cm.pr["OUT_BGFXSW"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(BGFXSW_field)

f.write(riga + "\n")

chiavi = list(BGFXSW.keys())
for k in chiavi:
    l = len(BGFXSW[k].sw)
    for i in range(0, l):
        s = BGFXSW[k].nome + "|" + "|".join(map(str, BGFXSW[k].sw[i].datisw))
        f.write(s+"\n")
f.close()

#
# Scrittura del file BGFXSW_righe_Escluse.csv
#

y = [cm.out_path, "BGFXSW_righe_Escluse.csv"]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=,\n")

print("\n\nScrittura file " + output_file)

n = len(righe_escluse)
for k in range(0, n):
    f.write(righe_escluse[k])
f.close()


#
# Valutare se scrivere il file contenente i nomi doppi rilevati in CMDB _ Asset SW.
#

###################################################################################################
###################################################################################################
###################################################################################################

print("Procedura per la elaborazione dei dati da CMDB - Asset Software.")

#
# Cerco il file più recente in base al pattern indicato in Parametri.json

cm.files = []

file_pattern = cm.pr["CMDB_SW_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

temp = sorted(cm.files, reverse=True)
print("\nElaborazione file " + temp[0])

fc = open(temp[0], "r")

i = 0   # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione
h = 0

righe_escluse = []   # Lista di appoggio per verificare se quel server è già stato elaborato.
mesg = "Elemento [{}/{}]"
for r in fc:
    print('\r', mesg.format(i,h), end='', flush=True)
    h += 1
    if ( i < 2 ):
        i += 1
        continue
    separa = cm.trova_separa(r)
    tmp = cm.togli_apici(r, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici
#
    y = tmp.split(cm.cs)

#
# Verifica che il nome del prodotto e/o del componente non contenga una delle parole che lo possono far escludere
#
    nome_publisher = y[CMDBSW_field["manufacturer_name_"]].lower()
    nome_prodotto = y[CMDBSW_field["software"]]

    x = cm.cerca_elemento(cm.pr["Vendor"], nome_publisher, -1, 1, -1)
    if x < 0:
        righe_escluse.append(tmp)
        continue

    match nome_publisher:
        case 'microsoft':
            x = cm.cerca_elemento(mcrsft_kywrd_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
            x = cm.cerca_elemento(mcrsft_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
        case 'ibm':
            x = cm.cerca_elemento(ibm_kywrd_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
            x = cm.cerca_elemento(ibm_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
        case 'oracle':
            x = cm.cerca_elemento(orcl_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
        case 'vmware':
            x = cm.cerca_elemento(vmwr_kywrd_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
            x = cm.cerca_elemento(vmwr_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue
        case 'red hat':
            x = cm.cerca_elemento(rdht_nomi_2_xcld, nome_prodotto, -1, 1, -1)
            if x > -1:
                righe_escluse.append(tmp)
                continue

    t = []
    for c in CMDBSW_field:
        t.append(y[CMDBSW_field[c]].lower())
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in BFGXSW_field
#
    nome = t[CMDBSW_field["server"]]
    del t[0]
    if nome not in CMDBSW:
        CMDBSW[nome] = c_CMDBSW(nome)
    CMDBSW[nome].software(t)

    i += 1


#
# Scrittura del file AssetSoftware_CMDB.csv
#

y = [cm.out_path, cm.pr["OUT_CMDB_SW"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(CMDBSW_field)

f.write(riga + "\n")

chiavi = list(CMDBSW.keys())
for k in chiavi:
    l = len(CMDBSW[k].sw)
    for i in range(0, l):
        s = CMDBSW[k].nome + "|" + "|".join(map(str, CMDBSW[k].sw[i].datisw))
        f.write(s+"\n")
f.close()

#
# Scrittura del file CMDBSW_righe_Escluse.csv
#

y = [cm.out_path, "CMDBSW_righe_Escluse.csv"]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(BGFXSW_field)

f.write(riga + "\n")

n = len(righe_escluse)
for k in range(0, n):
    f.write(righe_escluse[k])
f.close()


#######################################################################################
#
#  Caricamento dati tabella HW per definizione dati da scrivere come Tabella SW
#
#######################################################################################

TABHW = {}

y = [cm.out_path, cm.pr["OUT_Hardware_TAB"]]
input_file = cm.dr.join(y)
cm.carica_dati(input_file, TABHW, 0)

i = 0
kiavi = list(TABHW.keys())
for nome in kiavi:
    Software[nome] = c_TABSW(nome, TABHW[nome])


#  inserito i dati HW nel membro software[nome].datihw
#
#	"nome_prodotto": {"BGFXSW": 6, "CMDBSW": 1},
#   "nome_publisher": {"BGFXSW": 1, "CMDBSW": 2},
#	"versione_prodotto": {"BGFXSW": 7},
#	"nome_componente": {"BGFXSW": 2},
#	"versione_componente":{"BGFXSW": 3, "CMDBSW": 3},
#	"versione_dettagliata": {"BGFXSW": 4},
#	"nome_edizione": 0,
#	"versione_edizione": 0,
#	"metrica": {"BGFXSW": 8},
#	"percorso_di_installazione": {"BGFXSW": 5},
#
# i valori sopra indicati sono i campi da valorizzare per ogni software installato.
#
 
    if nome in BGFXSW:
        # 
        # Elaborazione dati del SW installato - Fonte BIGFIX
        #
        l = len(BGFXSW[nome].sw)
        for i in range(0, l):
            ediz_vers = '-'
            ediz_nome = '-'
            BGFXSW[nome].sw[i].datisw.append(ediz_nome)
            BGFXSW[nome].sw[i].datisw.append(ediz_vers)
            Software[nome].software(BGFXSW[nome].sw[i].datisw)
            nome_publisher = BGFXSW[nome].sw[i].datisw[SW_field["nome publisher"]["BGFXSW"]]
            nome_componente = BGFXSW[nome].sw[i].datisw[SW_field["nome componente"]["BGFXSW"]]
            versione_componente = BGFXSW[nome].sw[i].datisw[SW_field["versione_componente"]["BGFXSW"]]
            nome_prodotto = BGFXSW[nome].sw[i].datisw[SW_field["nome prodotto"]["BGFXSW"]]
            versione_prodotto = BGFXSW[nome].sw[i].datisw[SW_field["versione_prodotto"]["BGFXSW"]]
            y = nome_componente.split(' ')
            if ( nome_componente.find('sql server') > -1 ) and ( nome_componente.find('edition') > -1 ):
                z = cm.cerca_elemento(y, 'edition', 0, 1, -1)
                if z >= 0:
                    ediz_nome = y[z - 1]
                    if y[z - 2].lower() == 'r2':
                        ediz_vers = y[z - 3] + ' ' + y[z - 2]
                    else:
                        ediz_vers = y[z - 2]
                l_ediz_nome = ediz_nome.strip()
                if l_ediz_nome == 0:
                    ediz_nome = '-'
            if nome_componente.find("sharepoint") > -1:
                z = cm.cerca_elemento(y, "office", 0, 1, -1)
                if z > -1:
                    del y[z]
                    s = ' '.join(y)
                    BGFXSW[nome].sw[i].datisw[SW_field["nome componente"]["BGFXSW"]] = s
                    Software[nome].software(BGFXSW[nome].sw[i].datisw)
            if nome_prodotto.find("sharepoint") > -1:
                z = cm.cerca_elemento(y, "office", 0, 1, -1)
                if z > -1:
                    del y[z]
                    s = ' '.join(y)
                    BGFXSW[nome].sw[i].datisw[SW_field["nome prodotto"]["BGFXSW"]] = s
                    Software[nome].software(BGFXSW[nome].sw[i].datisw)
            if nome_prodotto.find("exchange server") > -1:
                if versione_prodotto == '14.3':
                    BGFXSW[nome].sw[i].datisw[SW_field["versione_prodotto"]["BGFXSW"]] = "2010"
                    Software[nome].software(BGFXSW[nome].sw[i].datisw)
            if nome_componente.find('office') > -1:
                ultimo = len(y) - 1
                z = cm.cerca_elemento(y, '365', 1, 1, -1)
                if z > -1:
                    z1 = cm.cerca_elemento(y, 'proplus', 1, 1, -1)
                    if z1 > -1:
                        ediz_nome = "Professional Plus"
                        ediz_vers = "365"
                    else:
                        ediz_nome = y[ultimo]
                        ediz_vers = "365"
                z = cm.cerca_elemento(y, 'professional plus', 1, 1, -1)
                if z > -1:
                    ediz_nome = "Professional plus"
                    ediz_vers = y[ultimo]
                z = cm.cerca_elemento(y, "2003", 1, 1, -1)
                if z > -1:
                    ediz_nome = y[ultimo]
                    ediz_vers = "2003"
                else:
                    ediz_nome = y[ultimo - 1]
                    ediz_vers = y[ultimo]
        # FOR elaborazione righe di software in BGFXSW[nome] --- FINE!

            Software[nome].sw[i].datisw[SW_field["nome_edizione"]] = ediz_nome
            Software[nome].sw[i].datisw[SW_field["versione_edizione"]] = ediz_vers
            
    else:
        if nome in CMDBSW:
            # 
            # Elaborazione dati del SW installato - Fonte CMDB
            #
            l = len(CMDBSW[nome].sw)
            for i in range(0, l):
                ediz_vers = '-'
                ediz_nome = '-'
                nome_publisher = CMDBSW[nome].sw[i].datisw[SW_field["nome publisher"]["CMDBSW"]]
                nome_componente = CMDBSW[nome].sw[i].datisw[SW_field["nome componente"]["CMDBSW"]]
                versione_componente = CMDBSW[nome].sw[i].datisw[SW_field["versione_componente"]["CMDBSW"]]
                Software[nome].software([nome_publisher, nome_componente, versione_componente, '-', 0, '-', 0, '-', ediz_nome, ediz_vers])
                y = nome_componente.split(' ')
                if ( nome_componente.find('sql server') > -1 ) and ( nome_componente.find('edition') > -1 ):
                    z = cm.cerca_elemento(y, 'edition', 0, 1, -1)
                    if z >= 0:
                        ediz_nome = y[z - 1]
                        if y[z - 2].lower() == 'r2':
                            ediz_vers = y[z - 3] + ' ' + y[z - 2]
                        else:
                            ediz_vers = y[z - 2]
                    l_ediz_nome = ediz_nome.strip()
                    if l_ediz_nome == 0:
                        ediz_nome = '-'
                if nome_componente.find("sharepoint") > -1:
                    z = cm.cerca_elemento(y, "office", 0, 1, -1)
                    if z > -1:
                        del y[z]
                        s = ' '.join(y)
                        CMDBSW[nome].sw[i].datisw[SW_field["nome componente"]["CMDBSW"]] = s
                        Software[nome].software(CMDBSW[nome].sw[i].datisw)
                if nome_componente.find("exchange server") > -1:
                    if versione_componente == '14.3':
                        CMDBSW[nome].sw[i].datisw[SW_field["versione_componente"]["CMDBSW"]] =  "2010"
                        Software[nome].software(CMDBSW[nome].sw[i].datisw)
                if nome_componente.find('office') > -1:
                    ultimo = len(y) - 1
                    z = cm.cerca_elemento(y, '365', 1, 1, -1)
                    if z > -1:
                        z1 = cm.cerca_elemento(y, 'proplus', 1, 1, -1)
                        if z1 > -1:
                            ediz_nome = "Professional Plus"
                            ediz_vers = "365"
                        else:
                            ediz_nome = y[ultimo]
                            ediz_vers = "365"
                    z = cm.cerca_elemento(y, 'professional plus', 1, 1, -1)
                    if z > -1:
                        ediz_nome = "Professional plus"
                        ediz_vers = y[ultimo]
                    z = cm.cerca_elemento(y, "2003", 1, 1, -1)
                    if z > -1:
                        ediz_nome = y[ultimo]
                        ediz_vers = "2003"
                    else:
                        ediz_nome = y[ultimo - 1]
                        ediz_vers = y[ultimo]
            # FOR elaborazione righe di software in CMDBSW[nome] --- FINE!

                Software[nome].sw[i].datisw[SW_field["nome_edizione"]] = ediz_nome
                Software[nome].sw[i].datisw[SW_field["versione_edizione"]] = ediz_vers

        # IF per nome in CMDB --- FINE!
    # IF per nome in BBGFXSW / ELSE per nome in CMDBSW --- FINE!
# FOR nome in Tabella_HW --- FINE!

#
# Scrittura del file 'Tabella_SW'
#

mesg = "Elemento [{}.{}/{}]"

y = [cm.out_path, cm.pr["OUT_Software_TAB"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(SW_field)

f.write(riga + "\n")
j = 0
i = 0
chiavi = list(Software.keys())
n = len(chiavi)
for k in chiavi:
    print('\r', mesg.format(j,i,n), end='', flush=True)
    t = "|".join(map(str,Software[k].datihw))
    l = len(Software[k].sw)
    for i in range(0, l):
        print('\r', mesg.format(j,i,n), end='', flush=True)
        s = t + "|" + "|".join(map(str,Software[k].sw[i].datisw))
        f.write(s + "\n")
    j += 1
f.close()

print("\n")
print ("+-----------------------------------------------------------+")
print ("!   Procedura Elabora_SW completata                         !")
print ("+-----------------------------------------------------------+")
