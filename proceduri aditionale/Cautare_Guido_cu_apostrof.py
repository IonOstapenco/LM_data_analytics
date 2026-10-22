#cautam "Dell'Omo Guido" in Active Directory
import json
import csv
from pathlib import Path
import os # metodologie putin mai veche


# ==========================================================
# Ricerca informazioni AD per Dell'Omo Guido
# Cerca in tutti i CSV delle cartelle Active Directory
# ==========================================================

# ----=-=-=-=-===-=-=-=-=-=-==-===------------------------============
# Cautam informatii AD pe nume, continut 
# ----=-=-=-=-===-=-=-=-=-=-==-===------------------------============

# ==========================================================
# Configurare
# =================================---============================

with open ("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)

Source_dir = parametri["Source_dir"] # --> C:\\License_Management
Report_dir = parametri["Report_dir"] # --> Report_202608

# valoare cautata
search_value = "Dell'Omo Guido"

# ======================================
# Mapa lunara path
# ======================================================================

# cu OS
#base_folder = os.path.join(Source_dir, Report_dir) # --> mapa de baza

# cu PAthLib
base_folder = Path(Source_dir) / Report_dir


# mapele Ad -- active direcotry
#ad_ced_folders = parametri["AD_CED_Pattern"] # --> "Active Directory Results - CED"
ad_ced_folders = parametri["AD_Base_Pattern"] # --> ""Active Directory Results - SERVIZICED""

# OUTPUT
# fisier csv output

output_file = ( # --> varianta veche Pathlib
    base_folder
    / "Rezultate_cautare_Dell'Omo Guido.csv"
)


#rezultate
results = []

# ===================================================
# CAUTARE CSV
# -=================================================

for folder in ad_ced_folders:
    # varianta cu pathlib
    current_folder = base_folder / folder


#    current_folder = os.path.join(
#        Source_dir,
#        Report_dir
#    )

    if current_folder.exists():
        print(f"se analizeaza folderul curent: {current_folder}")

        # se va face cautare la toate fisiere csv
        # care se termin cu ad-users_results
        csv_files = current_folder.rglob("AD-userResult.csv")

        for csv_file in csv_files:

            print(f" Analizeaza: {csv_file.name}")

            try:
                  with open(
                      csv_file,
                      "r",
                      encoding="utf-8",
                      newline=""
                  ) as f :
                      reader = csv.DictReader(
                          f,
                          delimiter=";" # sau |
                      ) 

                      # rand cu data initiale = 1
                      line_number = 1

                      for row in reader:

                          # analiza toate coloanele randului
                        for column, value in row.items():

                            if value is not None and search_value in value:

                                results.append({
                                    "FullPath": str(csv_file), # fisierul unde s-a gasit
                                    "LineNumber": line_number,
                                    "Column": column,
                                    "Value": value
                                })
                        line_number +=1

            except Exception as e:

                print(
                    f"WARNIG: Eroare la cittire fisier: "
                    f"{current_folder}"
                )


# ===============================================================
# SALVARE REZULTAT                                     
# =================================================================


if results:

    #cream mapa pentru otuput
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
        f"nu s-a gasit nici un rezuktat pentru {search_value}"
    )