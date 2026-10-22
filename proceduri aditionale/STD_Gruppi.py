
import Common as cm
import re
import openpyxl
import csv
import pandas
import os # ---> pentru verificare exidtenta fisier
from pathlib import Path

import time # ---> pentru calcul timp
start_time = time.time()
"""
scriptul preia date din mai multe surse 
(Flexera si Active Directory), 
filtreaza si normalizeaza info,
elimina duplicate si genereaza fisier Excel cu sheets

"""
print(" procedura per elabortazione dei dati " \
"de Active Directory e flexera file")

#==========================================

# 1. DIRECTORy
#======================================================


# verificare directoriu principal de lucru
cm.check_outdir(cm.out_path)

basePath = os.path.join(
    cm.start_path,
    cm.dr
)

outputPath = os.path.join(
    basePath,
    "gruppi"
)

os.makedirs(outputPath, exist_ok=True)

# =-==========================================-=-=-=-=-
# CITIRE PARAMETRI 
# =============================================--=-=


# seturi de grupuri -- > pentru velocitate mai rapida

"""
* **Gruppi Office** ++++ → FLEXERA_Lista gruppi Office.txt
* **AD Groups** ++++ → toate fișierele AD-usersAndGroupsResult.csv
* **AD Users** ++++ → AD_Users_Results_attivi.csv

"""
Gruppi_Office = {} # --> FLEXERA_Lista gruppi Office.txt
AD_groups = {} # --> toate fisiere AD-usersAndGroupsResult.csv
AD_Users = {} # --> AD_Users_Results_attivi.csv


#=======================================
# seturi de grupuri
# ========================================
GROUP_STD = set() # --> grupe standardte
GROUP_PRO = set() # -----> grupe professional
# ------------------------------------

# ----------------------------=-=-=-=-
# seturi Utilizatori grupuri
# =-============================

USER_GROUP_STD = set() # ---> set 
USER_GROUP_PRO = set()


#====================================================
# flexera grupurio
#=====================================================


# incarcam grupele care trebuie sa fie evaluate
# versiune veche 
#GroupList = cm.start_path + cm.dr + "FLEXERA_Lista gruppi Office.txt"

# versiune noua cu OS
GroupList = os.path.join(
    basePath,
    "FLEXERA_Lista gruppi Office.txt"
)

"""
# citire fisier metfda clasica
fc = open(GroupList, "r")
Linee  = fc.readlines() # --> citim linii din fisier
for linea in Linee:
    #impartim in standard si pro 
    a = str(linea).lower().rstrip('\n') # --> impartim in prima parte
    b = a.split(cm.cs)
    if b[1] == 'std':
        GROUP_STD.append
"""

# citire fisiere metoda mai rapida
with open(GroupList, "r") as fc: # --> daca ceva de adaugat encoding
    for linea in fc:

        if not linea:
            continue

        a = linea.strip()
        b = a.split(cm.cs)

        #nume de grup
        group_name = b[0].strip()
        group_type = b[1].strip().replace('\ufeff', '')

        # sortare grupur dupa standard si professional

        if group_type == 'STD':
            GROUP_STD.add(group_name)
        else:
            GROUP_PRO.add(group_name)

print("Grupppui STD:", GROUP_STD)
print("Grupppui PRO:", GROUP_PRO)


# =============================================-=--=-=-=-=-=-=-
# GRoup map
# -----------------------======================================

group_map = {}


pattern = re.compile(r"^(.*)_(prd|ads|col)$", re.IGNORECASE)

for group in GROUP_STD:

    group = group.strip()
    match = pattern.match(group)

    if not match: # --> daca nu se gaseste -- sarim, continuam
        continue

    base = match.group(1) # ---> denumirea grupuri filtrate/matchuite
    group_type = match.group(2) # --> grupuri nimerite

    if base not in group_map:
        continue

    group_map[base].add(group_type)


# -------------------------------------
# regula veche ca in PowerShell
# ----------------------------------------------
# EXCEPTII care trebuie pastrate
# -================================

exceptie = {
    "ctx_047_tta"
}

"""
$exceptions = @(
    "ctx_047_tta"
)
"""

valide_bases = []

# ciclu pentru trecere prin baza
for base, types in group_map.items():

    if len(types) == 1 and "prd" in types:
        valide_bases.append(base)
    elif base in exceptie:
        valide_bases.append(base)

# =============================================
# RECONSTRUIM GRUPELE
# ===============================================-

"""
# reconstruim lista FINALĂ de grupuri --- > poate de lasat sau modificat si integrat in nmetoda noua
$groups = foreach ($base in $validBases) {

    # excepție specială
    if ($base -eq "ctx_047_tta") {
        "${base}_ads"
    }
    else {
        "${base}_prd"
    }
}
"""
groups = set()

for base in valide_bases:

    if base == "ctx_047_tta":
        groups.add(f"{base}_ads")

    else:
        groups.add(f"{base}_prd")    


# un fel de debug

print("Gruppi finali:", len(groups))


# ===============================================
# normalize name
# ========================================

def normalize_name(name):
    if not name:
        return name

    n = str(name).strip()

    n = re.sub(r"[?*.-]+$","",n)

    n = re.sub(r"\\s+d+$","",n)
   
    n = re.sub(r"[* ]+\d+$","",n)


    n = re.sub(r"\s+","",n)

# *-*-*-*-**-*-*
    # elimina cuvantul bis din nume
    #$n = $n -replace '(?i)\s+bis$',''
    n = re.sub(r"\s+bis$", "",n, flags = re.IGNORECASE)

    return n.strip()




                 















#=================================================
# afisare timp elaborat procedura
# timp
end_time = time.time()
elapsed_time = end_time - start_time

print("\n==============================================")
print(f"Timp total de rulare: {elapsed_time:.2f} secunde")
print("==============================================")
