# ! terbuie de schimbat campurile!!!!
import pandas as pd


import json
import os

print("SE EXECUTA PIVOT JBOSS")
# ==========================================================
# 0. Citire parametri.json pentru INPUT si OUTPUT
# ==========================================================

with open("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)

# Director sursa principal
source_dir = parametri["Source_dir"]

# Subfolder unde se afla fisierul 
report_dir = parametri["Report_dir"]

# Subfolder output
output_subdir = parametri["Output_dir"]

# Pattern fisier CMDB
cmdb_pattern = parametri["OUT_JBOSS_TAB"]

# Extensie fisier
extensie = parametri["Extension_end"]

# ==========================================================
# CONSTRUIRE CALE INPUT  (Source_dir + Report_dir)
# ==========================================================

input_dir = os.path.join(source_dir, report_dir, output_subdir)

file_path = None

for fisier in os.listdir(input_dir):
    if cmdb_pattern in fisier and fisier.endswith(extensie):
        file_path = os.path.join(input_dir, fisier)
        break

if file_path is None:
    raise FileNotFoundError("Nu a fost gasit fisierul Tabella_JBOSS in Report_dir conform patternului!")


# ==========================================================
# CONSTRUIRE CALE OUTPUT  (Source_dir + Report_dir + Output_dir)
# ==========================================================

output_dir_full = os.path.join(source_dir, report_dir, output_subdir)

# cream director daca nu exista
os.makedirs(output_dir_full, exist_ok=True)

output_path = os.path.join(output_dir_full, "pivot_JBOSS_results.txt")

print("Fisier input detectat:", file_path)


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

    df = pd.read_csv(
    file_path,
    sep='|',
    dtype=str,
    encoding='utf-8',
    skiprows=1   # sare peste linia "sep=|"
)

# normalizare coloane
df.columns = [norm(c) for c in df.columns]






# de scgimbat separator si ENCODING!!!!
#df = pd.read_csv(file_path, sep=',', dtype=str, encoding='cp1252') #--> varianta mai noua


# Transformam stringurile goale in NaN
df = df.replace('', pd.NA) ## tipa Not a Number, simboluri non numnerice, unerori sunt invizibile dar se citesc


# asta daca n_core vine ca string
df["n_core"] = pd.to_numeric(df["n_core"], errors="coerce")

"""
#  QUERY NOU pentru JBOSS

SELECT 
    cliente,
    SUM(n_core) AS total_n_core
FROM tabella_jboss
WHERE 
    powerstate <> 'poweredOff'
    AND nome_componente <> '-'
    AND ambiente NOT IN ('DR', 'POC', 'TEST', 'UAT')
    AND ambiente IS NOT NULL
    -- optional, daca de exclus NULL:
    AND cliente IS NOT NULL
    AND cliente <> 'CREDEM'
GROUP BY 
    cliente
ORDER BY 
    total_n_core DESC;
    
"""

result = (
    df[
        (df["powerstate"] != "poweredOff") &
        (df["nome componente"] != "-") &
        (~df["ambiente"].isin(["DR", "POC", "TEST", "UAT"])) &
        (df["ambiente"].notna()) &
        (df["cliente"].notna()) &
        (df["cliente"] != "CREDEM")
    ]
    .groupby("cliente", as_index=False)
    .agg(total_n_core=("n_core", "sum"))
    .sort_values(by="total_n_core", ascending=False)
)
print(result)

total_general = result["total_n_core"].sum()
print("\nTOTAL GENERAL:", total_general)

total_general = result["total_n_core"].sum()

total_row = pd.DataFrame({
    "cliente": ["TOTAL"],
    "total_n_core": [total_general]
})

result_final = pd.concat([result, total_row], ignore_index=True)

print(result_final)

#debug coloane
"""
print("Valori 'nome componente':")
print(df['nome componente'].value_counts())
"""
print("Fisier output:", output_path)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result_final.to_string(index=False))



#in forma de csv
#result_final.to_csv(output_path, index=False)