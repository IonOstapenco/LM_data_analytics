import pandas as pd
import os
import logging
import re
from datetime import date, datetime  # --> asta pentru data
import json


# ==========================================================
# 0. Citire parametri.json pentru INPUT si OUTPUT
# ==========================================================

with open("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)


Source_dir = parametri["Source_dir"]
Report_dir = parametri["Report_dir"]
Output_dir = parametri["Output_dir"]
Separa_dir = parametri["Separa_dir"]
XLS_end = parametri["XLS_end"]
# source dir 
# xls_ end


# -----------------------------------------------------------------------

# data, luam prima zi din luna curenta (ceva ia din sistem)
# Get today's date (as a date object)
# -----------------------------------------------------------------------

#! atentie, se ia data din luna aceasta!!! 
today_date = date.today()
# Get the first day of the current month
first_day_of_month = today_date.replace(day=1)

# "%Y-%m-%d"  -an, luna - zi
data_de_intai = first_day_of_month.strftime("_%d%m%Y") # --> am pus format din rbtools

print(first_day_of_month)

# -----------------------------------
# configurazione
# -----------------------------------------------

# mapoa de baza
# varianta vehce harccodata
#base_folder = r"C:\Users\crme240\OneDrive - ION\Desktop\rvtools_extract_TEST"

# varianta noua 
base_folder = os.path.join(Source_dir, Report_dir)
"""

# input file1 med-vvc-dg-0802
input_filename = "med-vvc-dg-0802.gbm.lan_CASTELLAZZO_DR_RVTools_export_all_2026-01-07_11.19.29.xlsx"
input_file = os.path.join(base_folder, input_filename)

"""




# exemplu luat din exercitii
# prefixe dorite, ca sa nu mai schimbam de fiecare data scriplut

prefixe_dorite = ("med-vvc-dg-0802", "med-vvc-pg-0801") # --> prefixe pentru fisiere


"""
EXEMPLU 

filename = "document_001.txt"
if filename.startswith("document_"):
    print("The file belongs to the document series.") # Output: The file belongs to the document series
"""

# punem input files intr-o variabila
input_filenames = [
    #punem ciclu for 
    f for f in os.listdir(base_folder)
    #daca f se incepe cu prefix dorit si se sfarseste cu xlsx
    if f.startswith(prefixe_dorite)  and f.endswith(XLS_end)

]

print("fisiere detectate pentru procesare:  ")
#ciclu de afisare  care s-au detectat
for f in input_filenames:
    print(" -- ", f)


#pentru ambele fisiere 
sheets_to_export = ["vCluster", "vCPU", "vHost", "vInfo", "vTools"]


# !! punem intr-o functie


def export_excel_file(input_filename):

    input_path = os.path.join(base_folder, input_filename)
#------------------------ ---------------------------------------
# DETECTAM PREFIX din nume file
# -------------------------------------------------------------------
    prefix_match = re.match(r"^[^.]+", input_filename) # --> pana la punct detectam

    # conditia p-u prefix
    if not prefix_match:
        raise ValueError("Nu s-a putut  sa determinam prefix din numele la fisier")
    
    prefix = prefix_match.group(0)

    folder_name = f"{prefix}_{data_de_intai}"

    #rv_tools_folder = f"rvtools"_{data_de_intai}

    # !!!! cred ca de pus sa se salveze deodata in rvtools! 
    # cautam mapa destinatie (rvtools_data_de_intai)
    # daca este , atunci afisam mesajul ca este
    # daca nu-i, atunci se va salva automat in output_folder
    rvtools_folder_name = f"rvtools{data_de_intai}"
    rvtools_folder = os.path.join(base_folder, rvtools_folder_name)


    if os.path.isdir(rvtools_folder):
        print(f"Folder {rvtools_folder_name} exista. sa vva salva in acesta")
        output_folder = os.path.join(rvtools_folder, folder_name)
    else:
        print(f"Folder {rvtools_folder_name} NU esista! se salveasza in output standard")       
        # cream Folder output automat  --> med-vvc-dg-0802
        output_folder = os.path.join(base_folder, Output_dir,folder_name

)
    os.makedirs(output_folder, exist_ok=True)



    # deschidem file Excel

    try:
        excel_file = pd.ExcelFile(input_path)
        existing_sheets = excel_file.sheet_names
    except Exception as e:
        print(f"EROARE al deschiderea fisierului: {e}")
        raise    

    
    # se face export selectiv
    for sheet_name in sheets_to_export:
        if sheet_name not in existing_sheets:
            print(f"[{prefix}] Sheet cu assa denumire nu exista!")
            continue

        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)

            output_filename = f"RVTools_tab{sheet_name}.csv"
            output_path = os.path.join(output_folder, output_filename)


            df.to_csv(output_path, index=False, sep=";")
            print(f"Creat: {output_filename}")



        except Exception as e:
            print(f"erore la export sheet {sheet_name}: {e}")
    print("\n Export finisat ")        



# --------------------------------------------------------------------------------------
#  exectuam petru toate fisierele

#-----------------------------------------------------------------------------

for filename in input_filenames:
    export_excel_file(filename)



