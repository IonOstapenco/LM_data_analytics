#### asta doar cu CSV!!!! fara excel si numpy!!


# ! terbuie de schimbat campurile!!!!
import pandas as pd

# ====== 1. Citire fisier ======
## !! schimbam input din ianuarie, apoi februaire!!!
# vechi care a mers
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2025-10-16 09_02_33.csv"

# !! IANUARIE
file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-03_02_2026, 05_56_05 PM.csv"

# nou, care ar trebui sa mearga dar nu merge FEBRUAIRE!!!!
#file_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2026-02-02 09_52_41.csv"

output_path = r"C:\Users\crme240\OneDrive - ION\Desktop\manca\pivot_results__MARZO.txt"

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

t1_OLD = (
    df[df['ruolo'].isna()]
    .groupby('ruolo')['nomeci']
    .count()
    .reset_index(name='COUNT_nomeci')
)

# varianta noua care arata mai corect 
#t1 = df[df['ruolo'].isna() | (df['ruolo'].str.strip() == '')] # --> parca tot socoate
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
#print(t1) # -->aratam continutl



##### scoatem suma 
tab1_tot = df['Ruolo'].isna().sum() 
print("\n suma este total la ruolo este ",tab1_tot)


""""""
# =========================================================
# 2) ambiente - COUNT(server_category) unde ambiente IS NULL
# =========================================================
t2_ODL = ( # --- nu vrea sa arate
    df[df['ambiente'].isna()]
    .groupby('ambiente')['server_category']
    .count()
    .reset_index(name='COUNT_server_category')
)

t2 = (
    df[df['Ambiente'].isna()]
    .groupby('Ambiente', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)
#print("\nTABEL 2 - ambiente NULL")
#print(t2)


##### scoatem suma 
tab2_tot = df['Ambiente'].isna().sum() 
print("\n suma este total la ambiente este ",tab2_tot)

# =========================================================
# 3) os - COUNT(nomeci) unde os IS NULL
# =========================================================
t3_OLD = (
    df[df['os'].isna()]
    .groupby('os')['nomeci']
    .count()
    .reset_index(name='COUNT_nomeci')
)

t3 = (
    df[df['OS'].isna()]
    .groupby('OS', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)

#print("\nTABEL 3 - os NULL")
#print(t3)
##### scoatem suma si afisam
tab3_tot = df['OS'].isna().sum() 
print("\n suma este total la os este ",tab3_tot)

# =========================================================
# 4) server_numerocore - COUNT(nomeci) unde server_numerocore IS NULL
# =========================================================
t4_OLD = (
    df[df['server_numerocore'].isna()]
    .groupby('server_numerocore')['nomeci']
    .count()
    .reset_index(name='COUNT_nomeci')
)

t4 = (
    df[df['Numero Socket'].isna()]
    .groupby('Numero Socket', dropna=False)['Nome CI']
    .count()
    .reset_index(name='COUNT_Nome CI')
)


#print("\nTABEL 4 - server_numerocore NULL")
#print(t4)

##### scoatem suma si afisam
tab4_tot = df['Numero Socket'].isna().sum() 
print("\n suma este total la Numero Socket este ",tab4_tot)


# =========================================================
# 5) server_people_name - COUNT(server_category) unde server_people_name IS NULL
# =========================================================
t5_OLD = (
    df[df['server_people_name'].isna()]
    .groupby('server_people_name')['server_category']
    .count()
    .reset_index(name='COUNT_server_category')
)


t5 = (
    df[df['server_people_name'].isna()]
    .groupby('server_people_name', dropna=False)['server_category']
    .count()
    .reset_index(name='COUNT_server_category')
)

#print("\nTABEL 5 - server_people_name NULL")
#print(t5)


tab5_tot = df['server_people_name'].isna().sum() 
print("\n suma este total la server_people_name este ",tab5_tot)


# ==============================================================================
# 6) CPU - COUNT(server_category) unde server_numerocpu IS NULL
# =========================================================

t6 = (
    df[df['server_numerocpu'].isna()]
    .groupby('server_numerocpu', dropna=False)['nomeci']
    .count()
    .reset_index(name='COUNT_nomeci')
)

#print("\nTABEL 6 - server_numerocpu NULL")
#print(t6)

tab6_tot = df['server_numerocpu'].isna().sum() 
print("\n suma este total la server_numerocpu este ",tab6_tot)

# =========================================================
# 7) CPU - COUNT(server_category) unde server_numerocpu IS NULL
# =========================================================

t7 = (
    df[df['server_isvirtual'].isna()]
    .groupby('server_isvirtual', dropna=False)['server_type']
    .count()
    .reset_index(name='COUNT_server_type')
)

#print("\nTABEL 7 - server_isvirtual NULL")
#print(t7)

tab7_tot = df['server_isvirtual'].isna().sum() 
print("\n suma este total la server_isvirtual este ",tab7_tot)

# ==============================================================================
# 8) sockets - COUNT(server_type) unde server_numerocpu IS NULL
# =========================================================

t8 = (
    df[df['numero_socket'].isna()]
    .groupby('numero_socket', dropna=False)['nomeci']
    .count()
    .reset_index(name='COUNT_server_type')
)

#print("\nTABEL 8 - server_numerocpu NULL")
#print(t8)


tab8_tot = df['numero_socket'].isna().sum() 
print("\n suma este total la numero_socket este ",tab8_tot)

# =========================================================
# 9) Contratto - COUNT(server_category) unde server_numerocpu IS NULL
# =========================================================

t9 = (
    df[df['contratto'].isna()]
    .groupby('contratto', dropna=False)['server_type']
    .count()
    .reset_index(name='COUNT_server_type')
)

#print("\nTABEL 9 - contratto NULL")
#print(t9)


tab9_tot = df['contratto'].isna().sum() 
print("\nsuma este total la contratto este ",tab9_tot)

# ------- pentru afisarea sumei in terminal 
total_servers = df['nomeci'].count()


#print(total_servers) # ---> aratam total, cam arata gresit, trebuie sa arate 6921, dar arata 15153

coloane = [
    'ruolo',
    'ambiente',
    'os',
    'server_numerocore',
    'server_people_name',
    'server_numerocpu',
    'server_isvirtual',
    'numero_socket',
    'contratto'
]

total_nulluri = df[coloane].isna().sum().sum() # --> facem sumare la toate

print("Suma TOTALA a tuturor valorilor NULL este:", total_nulluri)


# ============================================================================
#    RAPORT FINAL FORMATAT
# =========================================================----------

#total_servers = len(df)
# un fel de haschcode ca la Java
raport = [
    ("Ruolo", tab1_tot),
    ("Ambiente", tab2_tot),
    ("OS", tab3_tot),
    ("Core", tab4_tot),
    ("Cliente", tab5_tot),
    ("CPU", tab6_tot),
    ("IS Virtual", tab7_tot),
    ("Socket", tab8_tot),
    ("Contratto", tab9_tot),
]

# Header
print("\nCategory       | Servers (blank) | Percentage")
print("---------------|-----------------|-----------")

# Randuri
for categorie, valoare in raport:
    procent = (valoare / total_nulluri) * 100
    print(f"{categorie:<14} | {valoare:>15} | {procent:>9.2f}%")
    print("---------------|-----------------|-----------")

# Total final
print(f"{'Total servers':<14} | {total_nulluri:>15} | {100:>9.2f}%")
print("---------------|-----------------|-----------")


# ---- de salvat in output. txt

with open(output_path, 'w', encoding='utf-8') as f:
# s-a ccopiat de mai sus, in loc de print  -- f.write
    f.write(f"total la ruolo este ")
    f.write(f"{tab1_tot}\n")
    f.write(f"---------------------------------------------\n") 
    #
    f.write(f"total este total la ambiente este ")
    f.write(f"{tab2_tot}\n") 
    f.write(f"---------------------------------------------\n")    

    f.write(f"total la os este ")
    f.write(f"{tab3_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la server_numerocore este ")
    f.write(f"{tab4_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la server_people_name este ")
    f.write(f"{tab5_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la server_numerocpu este ")
    f.write(f"{tab6_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la server_isvirtual este ")
    f.write(f"{tab7_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la numero_socket este ")
    f.write(f"{tab8_tot}\n")
    f.write(f"---------------------------------------------\n") 
    

    f.write(f"total la contratto este ")
    f.write(f"{tab9_tot}\n")
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
        procent = (valoare / total_nulluri) * 100
        f.write(f"{categorie:<14} | {valoare:>15} | {procent:>9.2f}%\n")
        f.write("---------------|-----------------|-----------\n")

# Total final
    f.write(f"{'Total servers':<14} | {total_nulluri:>15} | {100:>9.2f}%\n")
    f.write("---------------|-----------------|-----------")

print("fisier s-a sasalvat cu succes!")






"""
print("Total rows:", len(df))
print("Total distinct servers:", df['nomeci'].nunique())
print("Total non-null nomeci:", df['nomeci'].count())


print("Total rows:", len(df))
print("Total distinct servers:", df['nomeci'].nunique())
"""

"""
###########_____________________--------------

# 1. Eliminăm duplicatele pe server
df_unique = df.drop_duplicates(subset=['nomeci'])
total_servers = len(df_unique)


# 3. Funcție pentru calcul NULL + procent
def calc_null(column_name):
    null_count = df_unique[column_name].isna().sum()
    percentage = (null_count / total_servers) * 100
    return null_count, percentage




## lasam, e ok 
# 4. Lista de coloane
columns = [
    ("Ruolo", "ruolo"),
    ("Ambiente", "ambiente"),
    ("OS", "os"),
    ("Core", "server_numerocore"),
    ("Cliente", "server_people_name"),
    ("CPU", "server_numerocpu"),
    ("IS Virtual", "server_isvirtual"),
    ("Sockets", "numero_socket"),
    ("Contratto", "contratto"),
]



# !! lasam e OK p-u afisare! 
print("Category       | Servers (blank) | Percentage ")
print("---------------|-----------------|------------")

for label, col in columns:
    count, perc = calc_null(col)
    print(f"{label:<14} | {count:>15} | {perc:>9.2f}%")
    print("---------------|-----------------|------------")

print(f"{'Total servers':<14} | {total_servers:>15} | {100:>9.2f}%")
print("---------------|-----------------|------------")

"""