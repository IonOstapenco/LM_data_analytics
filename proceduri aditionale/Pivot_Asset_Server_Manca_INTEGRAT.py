# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
from pathlib import Path


# ==========================================================
# FUNCTIE PRINCIPALA
# ==========================================================

def Genera_Report_Blank():

    # ==========================
    # 1. Citire parametri.json
    # ==========================
    with open("parametri.json", "r", encoding="utf-8") as f:
        param = json.load(f)

    
    BASE_DIR = Path(param["Source_dir"])
    REPORT_DIR = param["Report_dir"]
    OUTPUT_DIR = param["Output_dir"] 
    pattern = param["CMDB_Pattern"]

    # Folderul unde se află CMDB
    CMDB_FOLDER = BASE_DIR / REPORT_DIR

    print("Caut in folder:", CMDB_FOLDER)

    

    # ==========================
    # 2. Gasire fisier CMDB
    # ==========================
    cmdb_file = None

    for file in CMDB_FOLDER.iterdir():
        if pattern in file.name and file.suffix ==".csv":
            cmdb_file = file
            break

    if not cmdb_file:
        print("Fisier CMDB nu a fost gasit!")
        return

    print("Fisier gasit:", cmdb_file)

    # ==========================
    # 3. Citire CSV
    # ==========================
    df = pd.read_csv(cmdb_file, sep=';', dtype=str, encoding='cp1252')
    df = df.replace('', pd.NA)

    # ==========================
    # 4. Coloane analizate
    # ==========================
    coloane = [
        ("Ruolo", "ruolo"),
        ("Ambiente", "ambiente"),
        ("OS", "os"),
        ("Core", "server_numerocore"),
        ("Cliente", "server_people_name"),
        ("CPU", "server_numerocpu"),
        ("IS Virtual", "server_isvirtual"),
        ("Socket", "numero_socket"),
        ("Contratto", "contratto"),
    ]

    # ==========================
    # 5. Calcul NULL per coloană
    # ==========================
    rezultate = []
    total_nulluri = 0

    for label, col in coloane:
        if col in df.columns:
            null_count = df[col].isna().sum()
            rezultate.append((label, null_count))
            total_nulluri += null_count
        else:
            rezultate.append((label, 0))

    # ==========================
    # 6. Creare folder output daca nu exista
    # ==========================
    full_output_dir = CMDB_FOLDER / OUTPUT_DIR

    if not os.path.exists(full_output_dir):
        os.makedirs(full_output_dir)

    output_file = os.path.join(full_output_dir, "PIVOT_RAPORT_BLANK.txt")

    # ==========================
    # 7. Scriere raport
    # ==========================
    with open(output_file, "w", encoding="utf-8") as f:

        f.write("=============================================\n")
        f.write("   tabela finala macanza blanks\n")
        f.write("=============================================\n\n")

        f.write("Category       | Servers (blank) | Percentage\n")
        f.write("---------------|-----------------|-----------\n")

        for categorie, valoare in rezultate:
            procent = (valoare / total_nulluri) * 100 if total_nulluri > 0 else 0
            f.write(f"{categorie:<14} | {valoare:>15} | {procent:>9.2f}%\n")
            f.write("---------------|-----------------|-----------\n")

        f.write(f"{'Total blanks':<14} | {total_nulluri:>15} | {100:>9.2f}%\n")

    print("Raport generat cu succes:", output_file)


# ==========================================================
# RUN -- functia main ca in java
# ==========================================================
if __name__ == "__main__":
    Genera_Report_Blank()