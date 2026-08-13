#cautam "VDI_USER_VOLTERRA_026_MT" in Active Directory
import json
import csv
from pathlib import Path
import os # metodologie putin mai veche


# ==========================================================
# Ricerca informazioni AD per gruppo VDI_USER_VOLTERRA_026_MT
# Cerca in tutti i CSV delle cartelle Active Directory
# ==========================================================

# ----=-=-=-=-===-=-=-=-=-=-==-===------------------------============
# Cautam informatii AD pe grup VDI_USER_VOLTERRA_026_MT
# ----=-=-=-=-===-=-=-=-=-=-==-===------------------------============

# ==========================================================
# Configurare
# =================================---============================

with open ("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)


Source_dir = parametri["Source_dir"] # --> C:\\License_Management
Report_dir = parametri["Report_dir"] # --> Report_202608

#separator
csv_delimiter = parametri["Separa_car"] # --> separator |

# valoare cautata
search_value = "VDI_USER_VOLTERRA_026_MT"

#fisier cautat, numele fisierului
csv_pattern = parametri["AD-usersAndGroupsResult"]

#patternuri la mapa/mapele in care se va cauta
AD_CED_Pattern = parametri["AD_CED_Pattern"] # --> "Active Directory Results - CED"
AD_Base_Pattern = parametri["AD_Base_Pattern"] # --> "Active Directory Results - SERVIZICED"
# ======================================
# Mapa lunara path
# ======================================================================

# cu OS
#base_folder = os.path.join(Source_dir, Report_dir) # --> mapa de baza

# cu PAthLib, mapa cu raoport lunar
base_folder = Path(Source_dir) / Report_dir

# mapele Ad -- active direcotry
# l-am pus in lista
ad_ced_folders = parametri["AD_CED_Pattern"] # --> "Active Directory Results - CED"

# OUTPUT
# fisier csv output

output_file = ( # --> varianta veche Pathlib
    base_folder
    / "Rezultate_cautare_VDI_USER_VOLTERRA_026_MT.csv"
)


# --> varianta mai noua Pathlib
output_file = Path(base_folder)/"Rezultate_cautare_VDI_USER_VOLTERRA_026_MT.csv"
'''

output_file = os.path.join(
    base_folder,
    "Rezultate_cautare_VDI_USER_VOLTERRA_026_MT.csv"
)
'''

#rezultate
results = []

# ==================================----============
# CAUTARE MAPE AD
# -=-=-=-=============================================

AD_patterns = [
    AD_CED_Pattern,
    AD_Base_Pattern # --> fiindca se afla si in "Active Directory Results - SERVIZICED"
]

# ciclu de cautARE
for AD_pattern in AD_patterns:
    print(f"se cauta mapele cu pattern : {AD_CED_Pattern}")
    print(f"se cauta mapele cu pattern : {AD_Base_Pattern}")
    
    # cautam toate mapele case se incep cu pattern 
    AD_folders = [
        folder
        for folder in base_folder.iterdir()
        if folder.is_dir()
        and folder.name.startswith(AD_pattern) # 
    ]

    #daca nu este in pattern AD
    if not AD_folders:
        print(
            f"ATENTIE!!! nu se gaseste cu asa format sau nu exista mape;e",
            f"{AD_pattern}"
        )

        continue 

    for current_folder in AD_folders:
        print()
        print(f"mapa curenta care se analizeaza: {current_folder}")

        # in mapa curenta se vor citi fisierele csv
        csv_files  = current_folder.rglob(csv_pattern)

        for csv_file in csv_files:

            print(
                f" se analizeaza: {csv_file}"
            )

            try:

                with open(csv_file,
                          "r",
                          encoding="utf-16",
                          newline="") as f:
                    reader = csv.DictReader(
                        f,
                        delimiter=csv_delimiter
                    )

                    line_number = 1

                    for row in reader:
                        for column, value in row.items():

                            if (
                                value is not None
                                and search_value.lower()
                                in str(value).lower()
                            ):

                                results.append({
                                    "FullPath": str(csv_file),
                                    "LineNumber": line_number,
                                    "Column": column,
                                    "Value": value

                                })
                        line_number += 1        

            except Exception as e:
                print(
                    f" WARNING: Eroare la CITIRE CSV:"
                )

                print(
                    f"Fisier: {csv_file}"
                )

                print(
                    f" errpare: {e}"
                )


# ********************************************************************
# ===============================================================
# SALVARE REZULTAT                                     
# =================================================================


if results:

    #cream mapa pentru otuput ---> varianta cu PathLib
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        fieldnames = [
            "FullPath",
            "LineNumber",
            "Column",
            "Value"
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(results)

    print()
    print("=======================================================")
    print(f"Trovato {len(results)} risultati")
    print("Output:")
    print(output_file)
    print(" ==========================================================")

else:

    print()
    print(
        f"nu s-a gasit nici un rezultat pentru {search_value}"
    )