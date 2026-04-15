# Python Classi dati della tabella SW - VERSIUNEA FINALa

import csv
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Classi principali
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

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

class c_BGFXSW:
    def __init__(self, nome):
        self.nome = nome
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))

class c_CMDBSW:
    def __init__(self, nome):
        self.nome = nome
        self.sw = []

    def software(self, dati):
        self.sw.append(AssetSW(dati))

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# FUNZIONE PER IL CALCOLO DELLE EDIZIONI (DEFINITa LA INCEPUT)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def calcola_edizione(dati_sw):
    """Calculează nome_edizione și versione_edizione pentru software"""
    nome_componente = dati_sw[1]  # nome componente
    y = nome_componente.split(' ')
    
    # SQL Server
    if 'sql server' in nome_componente.lower() and 'edition' in nome_componente.lower():
        z = cm.cerca_elemento(y, 'edition', 0, 1, -1)
        if z >= 0:
            ediz_nome = y[z - 1]
            if z - 2 >= 0 and y[z - 2].lower() == 'r2':
                ediz_vers = y[z - 3] + ' ' + y[z - 2] if z - 3 >= 0 else y[z - 2]
            else:
                ediz_vers = y[z - 2] if z - 2 >= 0 else '-'
            return ediz_nome.strip(), ediz_vers.strip()
    
    # Office 365
    if 'office' in nome_componente.lower():
        ultimo = len(y) - 1
        if cm.cerca_elemento(y, '365', 0, 1, -1) > -1:
            if cm.cerca_elemento(y, 'proplus', 0, 1, -1) > -1:
                return "Professional Plus", "365"
            else:
                return y[ultimo], "365"
        elif cm.cerca_elemento(y, 'professional plus', 0, 1, -1) > -1:
            return "Professional Plus", y[ultimo]
        elif cm.cerca_elemento(y, '2003', 0, 1, -1) > -1:
            return y[ultimo], "2003"
        else:
            return y[ultimo-1] if ultimo-1 >= 0 else '-', y[ultimo] if ultimo >= 0 else '-'
    
    # Default
    return '-', '-'

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# DICTIONARI E CAMPI - STRUCTURA COMPLETTA
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Software = {}
BGFXSW = {}
CMDBSW = {}

# STRUTTURA COMPLETA - 40 campi HW + 10 campi SW
SW_field = [
    "nome", "operating_system", "dominio", "dns_name", "virtuale", "tipo",
    "cluster_name", "cluster_ambiente", "cluster_cliente", "cluster_destinazione",
    "cluster_cores", "cluster_numhosts", "cluster_n_vms_total", "cluster_n_vms", 
    "cluster_n_vms_win", "hyperthreadactive", "ha_enabled", "drs_enabled", "host",
    "vm_hw_version", "n_cpu", "n_core", "pvu_per_core", "valore_pvu_modificato",
    "valore_pvu_predefinito", "fattore_core_oracle", "powerstate", "vcenter",
    "vcenter_cores", "vcenter_hosts", "vcenter_dominio", "vcenter_cluster",
    "cpu_model", "applicazione", "ruolo", "ambiente", "responsabile", "cliente",
    "contratto", "sito",
    "nome publisher", "nome componente", "versione_componente", 
    "versione dettagliata componente", "percorso_di_installazione", 
    "nome prodotto", "versione_prodotto", "metrica", "nome_edizione", 
    "versione_edizione"
]

# Campi BGFXSW
"""
#versiune vechie 

BGFXSW_field = {
    "Nome computer": 0,
    "Nome publisher": 2,
    "Nome componente": 3,
    "versione_componente": 4,
    "Versione dettagliata componente": 5,
    "percorso_di_installazione": 7,
    "Nome prodotto": 8,
    "versione_prodotto": 9,
    "metrica": 10
}
"""

BGFXSW_field = {
    "Nome computer": 8,
    "Nome publisher": 0,
    "Nome componente": 1,
    "versione_componente": 2,
    "Versione dettagliata componente": 3,
    "percorso_di_installazione": 9,
    "Nome prodotto": 4,
    "versione_prodotto": 10,
    "metrica": 6
}

# Campi CMDBSW  
CMDBSW_field = {
    "server": 0, 
    "software": 4, 
    "manufacturer_name_": 9, 
    "version_number": 10              
}

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# CARICARE DATE HW
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

print("Caricare date Hardware...")
cm.check_outdir(cm.out_path)
input_file = cm.dr.join([cm.out_path, cm.pr["OUT_Hardware_TAB"]])
Hardware = {}
cm.carica_dati(input_file, Hardware, 0)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# CARICARE ELENCHI per EXCLUSIONE
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def carica_lista(file_name, lista):
    try:
        input_file = cm.dr.join([cm.exc_path, file_name])
        with open(input_file, 'r') as fc:
            for linea in fc:
                lista.append(linea.strip())
    except FileNotFoundError:
        print(f"⚠️  Fișier {file_name} nu există - continuă...")

mcrsft_kywrd_2_xcld = []; mcrsft_nomi_2_xcld = []
ibm_kywrd_2_xcld = []; ibm_nomi_2_xcld = []
vmwr_kywrd_2_xcld = []; vmwr_nomi_2_xcld = []
orcl_nomi_2_xcld = []; rdht_nomi_2_xcld = []

carica_lista("IBM_keyword.csv", ibm_kywrd_2_xcld)
carica_lista("IBM_nomi.csv", ibm_nomi_2_xcld)
carica_lista("Microsoft_keyword.csv", mcrsft_kywrd_2_xcld)
carica_lista("Microsoft_nomi.csv", mcrsft_nomi_2_xcld)
carica_lista("Oracle_nomi.csv", orcl_nomi_2_xcld)
carica_lista("RedHat_nomi.csv", rdht_nomi_2_xcld)
carica_lista("VMware_keyword.csv", vmwr_kywrd_2_xcld)
carica_lista("VMware_nomi.csv", vmwr_nomi_2_xcld)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ELABORARE BGFXSW
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

print("Elaborare BGFXSW...")
file_pattern = cm.pr["BFGX_SW_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)
with open(temp[0], "r") as fc:
    righe_escluse = [next(fc)]  # Header
    for h, r in enumerate(fc, 1):
        separa = cm.trova_separa(r)
        tmp = cm.togli_apici(r, separa)
        y = tmp.split(cm.cs)

        nome_publisher = y[BGFXSW_field["Nome publisher"]].lower()
        nome_prodotto = y[BGFXSW_field["Nome prodotto"]]

        if cm.cerca_elemento(cm.pr["Vendor"], nome_publisher, -1, 1, -1) < 0:
            righe_escluse.append(r)
            continue

        # CONTROALE EXCLUDERE
        exclude = False
        if nome_publisher == 'microsoft':
            if (cm.cerca_elemento(mcrsft_kywrd_2_xcld, nome_prodotto, -1, 1, -1) > -1 or 
                cm.cerca_elemento(mcrsft_nomi_2_xcld, nome_prodotto, -1, 1, -1) > -1):
                exclude = True
        elif nome_publisher == 'ibm':
            if (cm.cerca_elemento(ibm_kywrd_2_xcld, nome_prodotto, -1, 1, -1) > -1 or 
                cm.cerca_elemento(ibm_nomi_2_xcld, nome_prodotto, -1, 1, -1) > -1):
                exclude = True
        elif nome_publisher == 'oracle':
            if cm.cerca_elemento(orcl_nomi_2_xcld, nome_prodotto, -1, 1, -1) > -1:
                exclude = True
        elif nome_publisher == 'vmware':
            if (cm.cerca_elemento(vmwr_kywrd_2_xcld, nome_prodotto, -1, 1, -1) > -1 or 
                cm.cerca_elemento(vmwr_nomi_2_xcld, nome_prodotto, -1, 1, -1) > -1):
                exclude = True
        elif nome_publisher == 'red hat':
            if cm.cerca_elemento(rdht_nomi_2_xcld, nome_prodotto, -1, 1, -1) > -1:
                exclude = True

        if exclude:
            righe_escluse.append(r)
            continue

        # CREARE LISTA SW (10 câmpuri)
        t = [
            y[BGFXSW_field["Nome publisher"]].lower(),
            y[BGFXSW_field["Nome componente"]].lower(),
            y[BGFXSW_field["versione_componente"]].lower(),
            y[BGFXSW_field["Versione dettagliata componente"]].lower(),
            y[BGFXSW_field["percorso_di_installazione"]].lower(),
            y[BGFXSW_field["Nome prodotto"]].lower(),
            y[BGFXSW_field["versione_prodotto"]].lower(),
            y[BGFXSW_field["metrica"]].lower(),
            '-', '-',  # nome_edizione, versione_edizione
        ]

        nome_computer = y[BGFXSW_field["Nome computer"]].lower()
        if nome_computer not in BGFXSW:
            BGFXSW[nome_computer] = c_BGFXSW(nome_computer)
        BGFXSW[nome_computer].software(t)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# ELABORARE CMDBSW
# elaborazione CMDBSW
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

print("Elaborare CMDBSW...")
cm.files = []
file_pattern = cm.pr["CMDB_SW_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
if cm.files:
    temp = sorted(cm.files, reverse=True)
    with open(temp[0], "r") as fc:
        for h, r in enumerate(fc, 1):
            if h < 3:  # Skip header ---  percio saltare a 3 posizioni
                continue
                
            separa = cm.trova_separa(r)
            tmp = cm.togli_apici(r, separa)
            y = tmp.split(cm.cs)

            nome_publisher = y[CMDBSW_field["manufacturer_name_"]].lower()
            nome_prodotto = y[CMDBSW_field["software"]].lower()

            if cm.cerca_elemento(cm.pr["Vendor"], nome_publisher, -1, 1, -1) < 0:
                continue

            # Aceleași controale de excludere
            # stesso controlleri per escludere
            exclude = False
            if nome_publisher == 'microsoft':
                if (cm.cerca_elemento(mcrsft_kywrd_2_xcld, nome_prodotto, -1, 1, -1) > -1 or 
                    cm.cerca_elemento(mcrsft_nomi_2_xcld, nome_prodotto, -1, 1, -1) > -1):
                    exclude = True
            # ... (restul controalelor identic)

            if exclude:
                continue

            t = [
                nome_publisher,
                nome_prodotto,
                y[CMDBSW_field["version_number"]].lower(),
                '-',  # versione dettagliata
                '-',  # percorso
                nome_prodotto,
                y[CMDBSW_field["version_number"]].lower(),
                '-',  # metrica
                '-', '-',  # edizione
            ]

            nome_server = y[CMDBSW_field["server"]].lower()
            if nome_server not in CMDBSW:
                CMDBSW[nome_server] = c_CMDBSW(nome_server)
            CMDBSW[nome_server].software(t)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# COMBINARE HW + SW ȘI SCRIERE FINAL

# combinazione di HW + SW e scivere final
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

print("Combinare HW + SW...")
for nome in Hardware:
    Software[nome] = c_TABSW(nome, Hardware[nome])

# ADAUGARE SW --
# AGIUNGI SW
for nome in list(Software.keys()):
    # BGFXSW
    if nome in BGFXSW:
        for sw_data in BGFXSW[nome].sw:
            edizione_nome, edizione_vers = calcola_edizione(sw_data.datisw)
            sw_data.datisw[8] = edizione_nome
            sw_data.datisw[9] = edizione_vers
            Software[nome].software(sw_data.datisw[:])
    
    # CMDBSW
    if nome in CMDBSW:
        for sw_data in CMDBSW[nome].sw:
            edizione_nome, edizione_vers = calcola_edizione(sw_data.datisw)
            sw_data.datisw[8] = edizione_nome
            sw_data.datisw[9] = edizione_vers
            Software[nome].software(sw_data.datisw[:])

# SCRIERE FISIER -- SCrivere il file
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_Software_TAB"]])
with open(output_file, "w", encoding='utf-8') as f:
    f.write("sep=|\n")
    f.write("|".join(SW_field) + "\n")
    
    for nome in Software:
        dati_hw = Software[nome].datihw  # circa 40 câmpuri //circa 40 campi
        for sw in Software[nome].sw:
            linea = dati_hw + sw.datisw  # 40 + 10 = 50 câmpuri
            f.write("|".join(map(str, linea)) + "\n")

print("\n+-----------------------------------------------------------+")
print("!   Procedura Elabora_SW completata                         !")
print("+-----------------------------------------------------------+")

'''
# kind of debugging
# pentru un felk de debugging
print("\n PROCEDURA COMPLETATĂ!")
print(f" Fișier: {cm.pr['OUT_Software_TAB']}")
print(f" Total servere: {len(Software)}")
print(f"  Total software: {sum(len(s.sw) for s in Software.values())}")
'''

