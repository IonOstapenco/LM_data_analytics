import pandas as pd
import os
import logging
import re
from datetime import date, datetime  # --> asta pentru data
import json


# ============================================================
# Lettura del file parameters.json per configurare INPUT e OUTPUT
# Citire parametri.json pentru INPUT si OUTPUT
# ==========================================================

with open("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)


Source_dir = parametri["Source_dir"]
Report_dir = parametri["Report_dir"]
Output_dir = parametri["Output_dir"]
Separa_dir = parametri["Separa_dir"]
XLS_end = parametri["XLS_end"]


# -----------------------------------------------------------------------
# Data: prendiamo il primo giorno del mese corrente dal sistema
# data, luam prima zi din luna curenta (ceva ia din sistem)
# -----------------------------------------------------------------------

#! Attenzione: la data viene presa dal mese corrente
#! atentie, se ia data din luna aceasta!!!
today_date = date.today()

## Otteniamo il primo giorno del mese corrente
# din google --> Get the first day of the current month
first_day_of_month = today_date.replace(day=1)

# "%Y-%m-%d"  - anno, mese, giorno
# "%Y-%m-%d"  - an, luna, zi
data_de_intai = first_day_of_month.strftime("_%d%m%Y") # --> am pus format din rvtools


#print(first_day_of_month)

# -----------------------------------
# configurazione cartelle
# configuratie
# -----------------------------------------------

# cartella base dove si trovano i report
# mapa de baza
base_folder = os.path.join(Source_dir, Report_dir)




# esempio preso dagli esercizi
# exemplu luat din exercitii

# prefissi desiderati per i file RVTools
# prefixe dorite, ca sa nu mai schimbam de fiecare data scriptul
prefixe_dorite = ("med-vvc-dg-0802", "med-vvc-pg-0801") #  prefissi per files
                                                       #--> prefixe pentru fisiere


# costruiamo lista dei file di input
# punem input files intr-o variabila
input_filenames = [

    # ciclo che scorre tutti i file nella cartella
    #punem ciclu for 
    f for f in os.listdir(base_folder)

    # selezioniamo solo file con prefisso desiderato e estensione xlsx
    #daca f se incepe cu prefix dorit si se sfarseste cu xlsx
    if f.startswith(prefixe_dorite)  and f.endswith(XLS_end)

]

print("fisiere detectate pentru procesare:  ")

# ciclo di stampa dei file trovati
#ciclu de afisare  care s-au detectat
for f in input_filenames:
    print(" -- ", f)


# lista dei fogli Excel da esportare
# pentru ambele fisiere 
sheets_to_export = ["vCluster", "vCPU", "vHost", "vInfo", "vTools"]


# funzione principale per esportare i fogli Excel in CSV
# !! punem intr-o functie
def export_excel_file(input_filename):

    input_path = os.path.join(base_folder, input_filename)

#------------------------ ---------------------------------------
# rileviamo il prefisso dal nome del file
# DETECTAM PREFIX din nume file
# -------------------------------------------------------------------
    prefix_match = re.match(r"^[^.]+", input_filename) # --> pana la punct detectam

    # verificare se prefixul a fost identificat
    # conditia p-u prefix
    if not prefix_match:
        raise ValueError("Impossibile determinare il prefisso dal nome del file / Nu s-a putut  sa determinam prefix din numele la fisier")
    
    prefix = prefix_match.group(0)

    folder_name = f"{prefix}_{data_de_intai}"

    #rv_tools_folder = f"rvtools"_{data_de_intai}

    # probabil cartella principale dove salvare output
    # !!!! cred ca de pus sa se salveze deodata in rvtools! 
    # cautam mapa destinatie (rvtools_data_de_intai)

    # se cartella esiste -> usiamo quella
    # daca este , atunci afisam mesajul ca este

    # se non esiste -> salviamo in cartella output standard
    # daca nu-i, atunci se va salva automat in output_folder
    
    """
    rvtools_folder_name = f"rvtools{data_de_intai}"
    rvtools_folder = os.path.join(base_folder, rvtools_folder_name)
    


    if os.path.isdir(rvtools_folder):
        print(f"Folder {rvtools_folder_name} exista. sa vva salva in acesta")
        output_folder = os.path.join(rvtools_folder, folder_name)
    else:
        print(f"Folder {rvtools_folder_name} NU esista! se salveasza in output standard")       
        # creiamo automaticamente la cartella output
        # cream Folder output automat  --> med-vvc-dg-0802
        output_folder = os.path.join(base_folder, Output_dir,folder_name)
"""
    rvtools_folders = [
        f for f in os.listdir(base_folder)
        if f.startswith("rvtools") and os.path.isdir(os.path.join(base_folder, f))
    ]

    if rvtools_folders:
        rvtools_folders.sort(reverse=True)  # cel mai recent
        rvtools_folder_name = rvtools_folders[0]
      #  rvtools_folder = os.path.join(rvtools_folder, folder_name)  --> nu vroia, dadea eroare
        rvtools_folder = os.path.join(base_folder, rvtools_folder_name)

        print(f"cartella trovata/folder gasit: {rvtools_folder_name}. verrà salvato qui/ se va salva aici ")
        output_folder = os.path.join(rvtools_folder, folder_name)
    else:
        print("Non esiste una cartella rvtools! Verrà salvato nell'output standard.")
        print(" nu exista nici un folder rvtools! se va salva in outptu standard")
        output_folder = os.path.join(base_folder, Output_dir, folder_name)



    os.makedirs(output_folder, exist_ok=True)



    # apriamo il file Excel
    # deschidem file Excel
    try:
        excel_file = pd.ExcelFile(input_path)
        existing_sheets = excel_file.sheet_names
    except Exception as e:
        print(f"ERRORE nell'apertura del file: {e}")
        print(f"EROARE la deschiderea fisierului: {e}")
        raise    

    
    # esportazione selettiva dei fogli
    # se face export selectiv
    for sheet_name in sheets_to_export:

        # verificam daca sheet exista
        if sheet_name not in existing_sheets:
            print(f"[{prefix}] Il foglio con questo nome non esiste!")
            print(f"[{prefix}] Sheet cu assa denumire nu exista!")
            continue

        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)

            output_filename = f"RVTools_tab{sheet_name}.csv"
            output_path = os.path.join(output_folder, output_filename)

            # salvam dataframe in CSV
            df.to_csv(output_path, index=False, sep=";")
            print(f"Creat: {output_filename}")

        except Exception as e:
            print(f"errore durante l'esportazione del foglio {sheet_name}: {e}")
            print(f"erore la export sheet {sheet_name}: {e}")

    print("\n Export finisat ")        



# --------------------------------------------------------------------------------------
# eseguiamo funzione per tutti i file trovati
#  exectuam petru toate fisierele
#-----------------------------------------------------------------------------

for filename in input_filenames:
    export_excel_file(filename)