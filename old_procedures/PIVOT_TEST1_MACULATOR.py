#### asta doar cu CSV!!!! fara excel si numpy!!


# ! terbuie de schimbat campurile!!!!
import pandas as pd


# ====== 1. Citire fisier ======
## !! schimbam input din ianuarie, apoi februaire!!!
# vechi care a mers
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2025-10-16 09_02_33.csv"

# !! IANUARIE
#care merge
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2026-01-05 13_01_14.csv"

# !! DECEMBRIE
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-12_01_2025, 08_05_56 AM.csv"

# dupa fisier mancanza de la Violeta
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Book1_TEST.csv"

# nou, care ar trebui sa mearga dar nu merge FEBRUAIRE!!!!
file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2026-02-02 09_52_41.csv"

output_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\pivot_results.txt"

# de scgimbat separator si ENCODING!!!!
#df = pd.read_csv(file_path, sep=';', dtype=str, encoding='cp1252') # --> varianta pentru octombrie


#iarasi stergem BOM, care e ufeff
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()

# ====== citire inteligenta CSV, fara BOM, ufeff ======

with open(file_path, "r", encoding="utf-8") as f:
    delimiter = ","
    header_pos = 0
    
    while True:
        pos = f.tell()
        line = f.readline()
        if not line:
            break

        clean = line.replace("\ufeff", "").strip()

        if clean.lower().startswith("sep="):
            delimiter = clean.split("=")[1]
            continue

        if "nome ci" in clean.lower():
            header_pos = pos
            f.seek(pos)
            break

    df = pd.read_csv(f, sep=delimiter, dtype=str)

# normalizare coloane
df.columns = [norm(c) for c in df.columns]






# de scgimbat separator si ENCODING!!!!
#df = pd.read_csv(file_path, sep=',', dtype=str, encoding='cp1252') #--> varianta mai noua


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
"""
t1_OLD = (
    df[df['ruolo'].isna()]
    .groupby('ruolo')['nomeci']
    .count()
    .reset_index(name='COUNT_nomeci')
)
# varianta noua care arata mai corect 
#t1 = df[df['ruolo'].isna() | (df['ruolo'].str.strip() == '')] # --> parca tot socoate

"""
t1_OK_OLD = (
    df[df['Ruolo'].isna()] # -- > mai pun si alte conditii la WHERE
    .groupby('Ruolo', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)


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
tab1_tot = df['Ruolo'].isna().sum() 
print("\n total la ruolo este ",tab1_tot)
#print(t1) # -->aratam continutl
#print(t1)
#t1_FARA = df[df['Ruolo'].isna() | (df['Ruolo'].str.strip() == '')] # --> parca tot socoate
#print("\n suma este total la ruolo FARA conditii aditionale este ",t1_FARA)



##### scoatem suma 
#tab1_tot = df['Ruolo'].isna().sum() 
#print("\n suma este total la ruolo este ",tab1_tot)

#print("TEST")

"""
#3333
print("Total Ruolo NULL:",
      df['Ruolo'].isna().sum())

print("Total Ruolo NULL + Server:",
      df[
          (df['Ruolo'].isna()) &
          (df['Type'] == 'Server')
      ].shape[0])

print("Total Ruolo NULL + Server + fara Appliance:",
      df[
          (df['Ruolo'].isna()) &
          (df['Type'] == 'Server') &
          (df['OS'] != 'APPLICANCE')
      ].shape[0])

"""      


"""

print("NULL pur:", df['Ruolo'].isna().sum())

print("Cu spatii doar:",
      df['Ruolo'].apply(lambda x: isinstance(x, str) and x.strip() == '').sum())

mask = (
    (
        df['Ruolo'].isna() |
        (df['Ruolo'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLICANCE')
)


tab1_tot = df[mask].shape[0]

print("Total corect =", tab1_tot)
"""

# ===================
# TABEL 2
# ====================
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
t2 = (
    df[
        (
            df['Ambiente'].isna() | (df['Ambiente'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Ambiente', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask2 = (
    (
        df['Ambiente'].isna() |
        (df['Ambiente'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab2_tot = df[mask2].shape[0]

print("\nTotal Ambiente =", tab2_tot)




# ====================================================
# TABEL 3
# ====================


t3 = (
    df[
        (
            df['OS'].isna() | (df['OS'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['Ruolo'] != 'APPLIANCE') # --> excludem Appliance!!
        & (df['Ruolo'] != 'APPLIANCE;') # --> excludem Appliance!!
    ]
    .groupby('OS', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)

mask3 = (
    (
        df['OS'].isna() |
        (df['OS'].fillna('').str.strip() == '')
    )
    #modificam
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['Ruolo'].fillna('').str.strip() != 'APPLIANCE')
    & (df['Ruolo'].fillna('').str.strip() != 'APPLIANCE;')
)

tab3_tot = df[mask3].shape[0]

print("\nTotal corect OS =", tab3_tot)


# ====================================================
# TABEL 4
# ====================

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
t4 = (
    df[
        (
            df['Numero Socket'].isna() | (df['Numero Socket'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Numero Socket', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask4 = (
    (
        df['Numero Socket'].isna() |
        (df['Numero Socket'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab4_tot = df[mask4].shape[0]

print("\nTotal  Numero Socket =", tab4_tot)

# ===================
# TABEL 5
# ====================
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
t5 = (
    df[
        (
            df['Domain Name'].isna() | (df['Domain Name'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Domain Name', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask5 = (
    (
        df['Domain Name'].isna() |
        (df['Domain Name'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab5_tot = df[mask5].shape[0]

print("\nTotal Domain Name =", tab5_tot)


#=======================================

#TABEL 6

# =====================

t6 = (
    df[
        (
            df['Numero CPU'].isna() | (df['Numero CPU'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Numero CPU', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask6 = (
    (
        df['Numero CPU'].isna() |
        (df['Numero CPU'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab6_tot = df[mask6].shape[0]

print("\nTotal Numero CPU =", tab6_tot)




#=======================================

#TABEL 7 --> Cliente (Used By)

# =====================

t7 = (
    df[
        (
            df['Used By'].isna() | (df['Used By'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Used By', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask7 = (
    (
        df['Used By'].isna() |
        (df['Used By'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab7_tot = df[mask7].shape[0]

print("\nTotal Cliente (used by) =", tab7_tot)



# ===================
# TABEL 8 --> CONTRATTO
# ====================
# logica SQL p-u tabel nou

t8 = (
    df[
        (
            df['Contratto'].isna() | (df['Contratto'] == '') | (df['Contratto'] == 0)
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Contratto', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask8 = (
    (
        df['Contratto'].isna() |
        (df['Contratto'].fillna('').str.strip() == '') |
        (df['Contratto'].astype(str).str.strip() == '0') # -- casa socoata si 0
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab8_tot = df[mask8].shape[0]

print("\nTotal Contratto (inclusiv cu 0) =", tab8_tot)



# ====================================================
# TABEL 9 --> Is Virtual
# =========================================


t9 = (
    df[
        (
            df['Is Virtual'].isna() | (df['Is Virtual'] == '')
        )
        & (df['Type'] == 'Server') # --> selectarm Type = Server
        & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Is Virtual', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#mask este o serie de valori True/False.
mask9 = (
    (
        df['Is Virtual'].isna() |
        (df['Is Virtual'].fillna('').str.strip() == '')
    )
    & (df['Type'].fillna('').str.strip() == 'Server')
    & (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab9_tot = df[mask9].shape[0]

print("\nTotal  Is Virtual =", tab9_tot)



#=======================================

#TABEL 10 --> AWS (Manufacturer)

# =====================


# in loc de Nome CI --> server_iscloud
# in loc de Used By --> Manufacturer (AWS)

t10 = (
    df[
        (
            #df['Manufacturer'].isna() | (df['Manufacturer'] == '')
            (df['Manufacturer'] == 'aws')
        )
       # & (df['Type'] == 'Server') # --> selectarm Type = Server
       # & (df['OS'] != 'APPLIANCE') # --> excludem Appliance!!
    ]
    .groupby('Manufacturer', dropna=False)['server_iscloud']
    .count()
    .reset_index(name='COUNT_server_iscloud')
)
#mask este o serie de valori True/False.
mask10 = (
    (
        #df['Manufacturer'].isna() |
        (df['Manufacturer'].fillna('').str.strip() == 'aws')
    )
    #& (df['Type'].fillna('').str.strip() == 'Server')
    #& (df['OS'].fillna('').str.strip() != 'APPLIANCE')
)

tab10_tot = df[mask10].shape[0]

print("\nTotal AWS (Manufacturer) =", tab10_tot)


# ------- pentru afisarea sumei in terminal 
#total_servers = df['Nome CI'].count()
coloane = [
    'Ruolo',  # tab1
    'Ambiente', # tab2
    'OS', # tab3
    'Numero Socket', # tab4
    'Domain Name', # tab5
    'Numero CPU', # tab6
    'Used By', # tab7
    'Contratto', #tab8
    'Is Virtual', #tab9
    'Manufacturer' # tab10
]

total_nulluri = df[coloane].isna().sum().sum() # --> facem sumare la toate

#print("Suma TOTALA a tuturor valorilor NULL este:", total_nulluri)


### adunare clasica, caci in alt mod imi da eroare

suma_totala = (
    tab1_tot +
    tab2_tot +
    tab3_tot +
    tab4_tot +
    tab5_tot +
    tab6_tot +
    tab7_tot +
    tab8_tot +
    tab9_tot +
    tab10_tot
)

print("\nSuma tuturor totalurilor =", suma_totala)





# un fel de haschcode ca la Java (asta pentru ciclu)
raport = [
    ("Ruolo", tab1_tot),
    ("Ambiente", tab2_tot),
    ("OS", tab3_tot),
    ("Numero Socket", tab4_tot),
    ("Domain Name", tab5_tot),
    ("Numero CPU", tab6_tot),
    ("Used By", tab7_tot),
    ("Contratto", tab8_tot),
    ("Is Virtual", tab9_tot),
    ("Manufacturer", tab10_tot)
]



# aratam in terminal (cred ca voi lasa s i in varianta finala)

# Header
print("\nCategory       | Servers (blank) | Percentage")
print("---------------|-----------------|-----------")

# Randuri
for categorie, valoare in raport:
    procent = (valoare / suma_totala) * 100
    print(f"{categorie:<14} | {valoare:>15} | {procent:>9.2f}%")
    print("---------------|-----------------|-----------")

# Total final
print(f"{'Total servers':<14} | {suma_totala:>15} | {100:>9.2f}%")
print("---------------|-----------------|-----------")




## SALVARE IN CSV


# ---- de salvat in output. txt

with open(output_path, 'w', encoding='utf-8') as f:

# s-a ccopiat de mai sus, in loc de print  -- f.write
    f.write(f"total la Ruolo este ")
    f.write(f"{tab1_tot}\n")
    f.write(f"---------------------------------------------\n") 
    #
    f.write(f"total este total la Ambiente este ")
    f.write(f"{tab2_tot}\n") 
    f.write(f"---------------------------------------------\n")    

    f.write(f"total la os este ")
    f.write(f"{tab3_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la Numero Socket este ")
    f.write(f"{tab4_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la Domain Name este ")
    f.write(f"{tab5_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la Numero CPU este ")
    f.write(f"{tab6_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la Used By este ")
    f.write(f"{tab7_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la Contratto este ")
    f.write(f"{tab8_tot}\n")
    f.write(f"---------------------------------------------\n") 
    

    f.write(f"total la Is Virtual este ")
    f.write(f"{tab9_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la Manufacturer este ")
    f.write(f"{tab10_tot}\n")
    f.write(f"---------------------------------------------\n")        

#tabela finala
    f.write("*********************************************-\n")
    f.write("\n")
    f.write("** tabela finala ***\n")
    f.write("=============================================\n")
    f.write("Category       | Servers (blank) | Percentage\n")
    f.write("---------------|-----------------|-----------\n")

    #ciclu
    for categorie, valoare in raport:
        procent = (valoare / suma_totala) * 100
        f.write(f"{categorie:<14} | {valoare:>15} | {procent:>9.2f}%\n")
        f.write("---------------|-----------------|-----------\n")

# Total final
    f.write(f"{'Total servers':<14} | {suma_totala:>15} | {100:>9.2f}%\n")
    f.write("---------------|-----------------|-----------")

print("fisier s-a sasalvat cu succes!")