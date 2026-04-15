#### asta doar cu CSV!!!! fara excel si numpy!!


# ! terbuie de schimbat campurile!!!!
import pandas as pd

# ====== 1. Citire fisier ======
## !! schimbam input din ianuarie, apoi februaire!!!
# vechi care a mers
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2025-10-16 09_02_33.csv"

# !! IANUARIE
file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2026-01-05 13_01_14.csv"

# nou, care ar trebui sa mearga dar nu merge FEBRUAIRE!!!!
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2026-02-02 09_52_41.csv"

output_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\pivot_results__IANUARIE.txt"

# de scgimbat separator si ENCODING!!!!
#df = pd.read_csv(file_path, sep=';', dtype=str, encoding='cp1252') # --> varianta pentru octombrie

# de scgimbat separator si ENCODING!!!!
df = pd.read_csv(file_path, sep=',', dtype=str, encoding='cp1252') #--> varianta mai noua


# Transformam stringurile goale in NaN
df = df.replace('', pd.NA) ## tipa Not a Number, simboluri non numnerice, unerori sunt invizibile dar se citesc

# =========================================================
# 1) ruolo - COUNT(nomeci) unde ruolo IS NULL
# =========================================================

#logica SQL pentru tabel 1
"""SELECT ruolo, COUNT(nomeci)
FROM asset_server
WHERE ruolo IS NULL OR ruolo = ''
GROUP BY ruolo;"""


# logica SQL p-u tabel nou
"""
SELECT ruolo, COUNT(nomeci)
FROM asset_server
WHERE 
    (ruolo IS NULL OR ruolo = '')
    AND Type = 'Server'
    AND OS <> 'APPLICANCE'
GROUP BY ruolo;
"""

# varianta mai veche , care ar trebui sa lucreze, dar nu lucreaza



t1 = (
    df[
        (
            df['Ruolo'].isna() | (df['Ruolo'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLICANCE') # --> excludem Appliance!!
    ]
    .groupby('Ruolo', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)

#print("\nTABEL 1 - ruolo NULL")
#print(t1) # -->aratam continutl



##### scoatem suma 
tab1_tot = df['Ruolo'].isna().sum() 
print("\n suma este total la ruolo este ",tab1_tot)
