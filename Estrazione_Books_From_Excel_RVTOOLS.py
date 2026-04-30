import os
import json

# import pentru rinominare
import re
from datetime import datetime

# import pentru extragere sheets in fisiere csv
import pandas as pd

# ======================================---------------------====================
# Citire parametri.json
# ====================================================================--------
with open("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)

Source_dir = parametri["Source_dir"]
Report_dir = parametri["Report_dir"]

# folder de bază (ex: C:\License_Management\Report_202604)
base_folder = os.path.join(Source_dir, Report_dir)

print(f"\nScanare folder: {base_folder}\n")

# =============================================---=============
# trecem cu recursie -----  (subfoldere incluse)
# ==================================================================================================
print("Afisare toate subfoldere")

for root, dirs, files in os.walk(base_folder):
    
    #foldername -- denumirea mapei care ne intereseaza

    folder_name = os.path.basename(root)

    #sarim, trecem daca nu este rvtools, in cazul dat 
    #if not folder_name.lower().startswith("rvtools"):
    #    continue

    # afisam folderul curent
    print(f"\n📁 Folder: {root}")
    
    if not files:
        print("   (niciun fisier)")
    
    # afisam fisierele din folder
    for file in files:
        full_path = os.path.join(root, file)
        print(f"   📄 {file}")
        print(f"      -> {full_path}")


print("!!! afisare doar subfoldere la rvtools")

for root, dirs, files in os.walk(base_folder):

    # verificam daca in path exista un folder rvtools
    if "rvtools" not in root.lower():
        continue

    print(f"\n📁 Folder: {root}")
    
    if not files:
        print("   (niciun fisier)")
    
    for file in files:
        full_path = os.path.join(root, file)
        print(f"   📄 {file}")
        print(f"      -> {full_path}")



print(f"\nNormalizare foldere in: {base_folder}\n")

# ====================================================-------======
# Functie normalizare nume folder
# ==========================================================
def normalize_folder_name(folder_name):

    # match: ceva_YYYYMMDD_HHMMSS
    match = re.match(r"(.+?)_(\d{8})_\d{6}", folder_name)
    if not match:
        return None

    name_part = match.group(1)
    date_part = match.group(2)

    # daca e hostname cu domeniu → il scurtam
    name_part = name_part.split(".")[0]

    try:
        dt = datetime.strptime(date_part, "%Y%m%d")
        date_fmt = dt.strftime("%d%m%Y")
    except:
        return None

    return f"{name_part}_{date_fmt}"


# =========================================
# Colectam toate folderele (BOTTOM-UP!)
# =========================================---------------===
folders_to_rename = []

for root, dirs, files in os.walk(base_folder, topdown=False):
    for d in dirs:
        full_path = os.path.join(root, d)
        folders_to_rename.append(full_path)

# ============================================================
# Facem rename
# =========================================
for old_path in folders_to_rename:

    folder_name = os.path.basename(old_path)
    parent = os.path.dirname(old_path)

    new_name = normalize_folder_name(folder_name)

    if not new_name:
        continue

    new_path = os.path.join(parent, new_name)

    if old_path == new_path:
        continue

    if os.path.exists(new_path):
        print(f"⚠️ Exista deja: {new_path}")
        continue

    try:
        os.rename(old_path, new_path)
        print(f"✅ {folder_name} → {new_name}")
    except Exception as e:
        print(f"❌ Eroare la {folder_name}: {e}")

print("\n✔ Rename complet (rvtools + subfoldere)\n")


#####==========================----------------====================
# extragere shets si salvare in csv

# ------=========================================================

sheets_to_export = ["vCluster", "vCPU", "vHost", "vInfo", "vTools"]

sheet_map = {
    "vCluster": "RVTools_tabvCluster",
    "vCPU": "RVTools_tabvCPU",
    "vHost": "RVTools_tabvHost",
    "vInfo": "RVTools_tabvInfo",
    "vTools": "RVTools_tabvTools"
}


def extract_sheets_from_excel(file_path):
    folder = os.path.dirname(file_path)

    try:
        xls = pd.ExcelFile(file_path)
    except Exception as e:
        print(f"❌ Nu pot deschide: {file_path} -> {e}")
        return

    for sheet in sheets_to_export:
        if sheet not in xls.sheet_names:
            print(f"⚠️ Sheet lipsa: {sheet}")
            continue

        try:
            df = pd.read_excel(xls, sheet_name=sheet)

            # 👇 nume standardizat
            output_name = sheet_map.get(sheet, sheet)
            output_file = os.path.join(folder, f"{output_name}.csv")

            df.to_csv(output_file, index=False, sep=';')

            print(f"✅ Exportat: {output_file}")

        except Exception as e:
            print(f"❌ Eroare la {sheet}: {e}")



print("\n🔍 Caut fisiere Excel RVTools...\n")

for root, dirs, files in os.walk(base_folder):

    if "rvtools" not in root.lower():
        continue

    for file in files:
        if file.lower().endswith(".xlsx") and "rvtools" in file.lower():
            
            full_path = os.path.join(root, file)

            print(f"\n📊 Procesare: {full_path}")
            extract_sheets_from_excel(full_path)






