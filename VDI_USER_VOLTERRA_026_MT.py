"""
to do task:
1 de extras coloana UserName, din toate fisierele
AD-usersAndGroupsResult.csv al carui GroupName este VDI_USER_VOLTERRA_026_MT

2. de inscris in fisier UserName, SamAccountName in Sheet1 

3. de facut innerjoin cu AD_Users_Results_attivi.csv (UserName si CN_00)

4, de inscris in sheet2 coloanele CN_00 (nume din attivi)
Principal Name  si Banche (OU_01)


"""

import json
import csv
from pathlib import Path
import pandas as pd
import os

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta # adaugat 01/09/2026, pentru transformare info din coloana Last Logon

# ==========================================================
# Configurare
# =================================---============================

with open ("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)

# varianta clasica
Source_dir = parametri["Source_dir"] # --> C:\\License_Management
Report_dir = parametri["Report_dir"] # --> Report_202608    

# varianta cu Path, mai nou
Source_dir = Path(
    parametri["Source_dir"]
)

Report_dir = Path(
    parametri["Report_dir"]
)

# separatoru oficial din 
ad_groups_delimiter = ";" # --> separator |
#ad_groups_delimiter


#delimitator pentru ad-users-results_attivi
csv_delimiter = "|"


# grupull cautat

# valoare cautata
search_group = "VDI_USER_VOLTERRA_026_MT"

# fisier care contine gripur si utserii AD
ad_groups_file = parametri[
    "AD-usersAndGroupsResult"
]

# fisier cu useri attivi --> din output-1
ad_users_attivi_file = parametri[
    "AD_Users_Results_attivi"
]



#patternuri la mapa/mapele in care se va cauta
AD_CED_Pattern = parametri["AD_CED_Pattern"] # --> "Active Directory Results - CED"
AD_Base_Pattern = parametri["AD_Base_Pattern"] # --> "Active Directory Results - SERVIZICED"


# ===================================-=-=-=-
# MAPA RAPROT LUNAR
#========================================================
# C:\License_Management\Report_202608

base_folder = (
    Source_dir /
    Report_dir
)

#=======================================================
# fisier OUTPUT
# -============================================================================
output_file = (
    base_folder /
    "VDI_USER_VOLTERRA_026_MT_con_sources.xlsx"
)


# ==================================================================
# funcite pentru detecare encoding

#------=-=-================================================================

def detect_encoding(file_path):
    # RO:
    # Detectam encoding-ul fisierului pe baza BOM.
    #
    # IT:
    # Rileviamo l'encoding del file in base al BOM.

    with open(
        file_path,
        "rb"
    ) as f:

        first_bytes = f.read(4)


    # RO:
    # UTF-16 Little Endian -> FF FE
    #
    # IT:
    # UTF-16 Little Endian -> FF FE

    if first_bytes.startswith(b"\xff\xfe"):
        return "utf-16"


    # RO:
    # UTF-16 Big Endian -> FE FF
    #
    # IT:
    # UTF-16 Big Endian -> FE FF

    if first_bytes.startswith(b"\xfe\xff"):
        return "utf-16"


    # RO:
    # UTF-8 cu BOM -> EF BB BF
    #
    # IT:
    # UTF-8 con BOM -> EF BB BF

    if first_bytes.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"


    # RO:
    # Daca nu exista BOM, folosim UTF-8.
    #
    # IT:
    # Se non esiste BOM, utilizziamo UTF-8.

    return "utf-8"

# ==========================================================
# CITIREA AD-usersAndGroupsResult.csv
# Lettura AD-usersAndGroupsResult.csv
# ==========================================================

def read_ad_groups_files(
    base_folder,
    patterns,
    csv_filename,
    delimiter,
    target_group
):

    # RO:
    # Lista in care vom salva utilizatorii gasiti.
    #
    # IT:
    # Lista nella quale salveremo gli utenti trovati.

    results = []


    # RO:
    # Set pentru eliminarea duplicatelor.
    #
    # IT:
    # Set utilizzato per eliminare i duplicati.

    unique_users = set()


    # ======================================================
    # CAUTARE FOLDERE AD
    # Ricerca delle cartelle AD
    # ======================================================

    for pattern in patterns:

        print()
        print(
            f"Se cauta mapele cu pattern: {pattern}"
        )

        print(
            f"Cerco le cartelle con pattern: {pattern}"
        )


        # RO:
        # Cautam toate directoarele din Report_202608
        # al caror nume incepe cu pattern-ul.
        #
        # IT:
        # Cerchiamo tutte le cartelle in Report_202608
        # il cui nome inizia con il pattern.

        AD_folders = [

            folder

            for folder in base_folder.iterdir()

            if (
                folder.is_dir()
                and folder.name.startswith(pattern)
            )
        ]


        # ==================================================
        # VERIFICARE FOLDERE
        # Verifica delle cartelle
        # ==================================================

        if not AD_folders:

            print(
                f"ATENTIE!!! Nu s-a gasit nicio mapa "
                f"pentru pattern: {pattern}"
            )

            print(
                f"ATTENZIONE!!! Nessuna cartella trovata "
                f"per il pattern: {pattern}"
            )

            continue


        # ==================================================
        # ANALIZARE FOLDERE
        # Analisi delle cartelle
        # ==================================================

        for current_folder in AD_folders:

            #print()
            #print(    f"Mapa curenta care se analizeaza: "                f"{current_folder}")

            #print(    f"Cartella corrente analizzata: "f"{current_folder}")


            # RO:
            # Cautam recursiv toate fisierele
            # AD-usersAndGroupsResult.csv
            #
            # IT:
            # Cerchiamo ricorsivamente tutti i file
            # AD-usersAndGroupsResult.csv

            csv_files = current_folder.rglob(
                csv_filename
            )


            # ==================================================
            # ANALIZARE FISIERE CSV
            # Analisi dei file CSV
            # ==================================================

            for csv_file in csv_files:

                #print(    f"  Se analizeaza: {csv_file}")

                #print(                    f"  Analizzo: {csv_file}")


                try:

                    # RO:
                    # Detectam automat encoding-ul fisierului.
                    #
                    # IT:
                    # Rileviamo automaticamente l'encoding del file.

                    encoding = detect_encoding(csv_file)


                   # print(    f"    Encoding detectat: {encoding}")

                    #print(                        f"    Encoding rilevato: {encoding}")


                    # RO:
                    # Deschidem fisierul CSV.
                    #
                    # IT:
                    # Apriamo il file CSV.

                    with open(
                        csv_file,
                        "r",
                        encoding=encoding,
                        newline=""
                    ) as f:

                        reader = csv.DictReader(
                            f,
                            delimiter=delimiter
                        )

                        #print()
                        #print("DEBUG HEADER:")
                        #print(reader.fieldnames)


                        line_number = 1


                        # ==================================================
                        # CITIRE RANDURI
                        # Lettura delle righe
                        # ==================================================

                        for row in reader:

                            # RO:
                            # Citim coloana GroupName.
                            #
                            # IT:
                            # Leggiamo la colonna GroupName.

                            group_name = row.get(
                                "GroupName"
                            )


                            if group_name is None:

                                line_number += 1

                                continue


                            # RO:
                            # Verificam daca GroupName corespunde
                            # grupului cautat.
                            #
                            # IT:
                            # Verifichiamo se GroupName corrisponde
                            # al gruppo cercato.

                            if (
                                str(group_name).strip().lower()
                                ==
                                target_group.strip().lower()
                            ):

                                user_name = row.get(
                                    "UserName"
                                )

                                sam_account_name = row.get(
                                    "SamAccountName"
                                )


                                # RO:
                                # Salvam doar daca UserName exista.
                                #
                                # IT:
                                # Salviamo solo se UserName esiste.

                                if user_name:

                                    user_name_clean = (
                                        str(user_name).strip()
                                    )

                                    sam_account_clean = (
                                        str(
                                            sam_account_name
                                            if sam_account_name
                                            is not None
                                            else ""
                                        ).strip()
                                    )


                                    # RO:
                                    # Eliminam duplicatele pe baza
                                    # combinatiei UserName + SamAccountName.
                                    #
                                    # IT:
                                    # Eliminiamo i duplicati in base
                                    # alla combinazione UserName +
                                    # SamAccountName.

                                    unique_key = (
                                        user_name_clean,
                                        sam_account_clean
                                    )


                                    if unique_key not in unique_users:

                                        unique_users.add(
                                            unique_key
                                        )


                                        results.append({

                                            "UserName":
                                                user_name_clean,

                                            "SamAccountName":
                                                sam_account_clean,

                                            "Fisier sursa":
                                            str(csv_file)    
                                        })


                            line_number += 1


                except Exception as e:

                    print(
                        "  WARNING: Eroare la CITIRE CSV:"
                    )

                    print(
                        f"    Fisier: {csv_file}"
                    )

                    print(
                        f"    Eroare: {e}"
                    )


    return results


# ==========================================================
# CITIRE AD_Users_Results_attivi.csv
# Lettura AD_Users_Results_attivi.csv
# ==========================================================

def read_ad_users_attivi(
    file_path,
    delimiter
):

    # RO:
    # Dictionarul va avea forma:
    #
    # CN_00 -> {
    #     Principal Name: ...,
    #     OU_01: ...
    # }
    #
    # IT:
    # Il dizionario avrà la forma:
    #
    # CN_00 -> {
    #     Principal Name: ...,
    #     OU_01: ...
    # }

    users = {}


    print()
    print(  "=================================================")

    print(        "Se citeste AD_Users_Results_attivi.csv")

    print(        "Lettura di AD_Users_Results_attivi.csv")

    print(        "=================================================")


    # RO:
    # Detectam encoding-ul fisierului.
    #
    # IT:
    # Rileviamo l'encoding del file.

    encoding = detect_encoding(
        file_path
    )


    #print(        f"Encoding detectat: {encoding}")


    try:
        # AD_Users_Results_attivi.csv
        with open(
            file_path,
            "r",
            encoding=encoding,
            newline=""
        ) as f:
            first_line = f.readline().strip()
            if first_line.lower().startswith("sep="):
                pass # --> sarim peste prima linie, sau putem face skip

            reader = csv.DictReader(
                f,
                delimiter="|"
            )
            #reader = csv.DictReader(f, delimiter="|")

            

            #print()
            #print("DEBUG HEADER ATTIVI:")
            #print(reader.fieldnames)


            for row in reader:

                # RO:
                # Citim CN_00.
                #
                # IT:
                # Leggiamo CN_00.

                cn_00 = row.get(
                    "CN_00"
                )


                if not cn_00:
                    continue


                cn_00_clean = (
                    str(cn_00).strip()
                )


                # RO:
                # Salvam doar prima aparitie pentru CN_00.
                #
                # IT:
                # Salviamo solo la prima occorrenza per CN_00.
# -----##############################333 -- inlocuim partea aceasta

                ou_01 = str(
                    row.get(
                        "OU_01",
                        ""
                    )
                ).strip()


                #verificam daca ou_01 contine volterra, lower() face verificare case insensitive

                if "volterra" not in ou_01.lower():
                    continue

                if cn_00_clean not in users:

                    users[cn_00_clean] = {

                        "CN_00":
                            cn_00_clean,

                        "Principal Name":
                            str(
                                row.get(
                                    "Principal Name",
                                    ""
                                )
                            ).strip(),

                        "OU_01":
                            str(
                                row.get(
                                    "OU_01",
                                    ""
                                )
                            ).strip()
                    }
##------------------------------------------## ### 

# fragment nou adaugat pe 01/09/2026

# mai intai citim ou_01, selectand CR Volterra, apoi CN_00


                

    except Exception as e:

        print(
            "WARNING: Eroare la CITIRE "
            "AD_Users_Results_attivi.csv"
        )

        print(
            f"Fisier: {file_path}"
        )

        print(
            f"Eroare: {e}"
        )


    return users




#=============================================================
# normalizare coloane pentru inner join
# ====================================================


import pandas as pd

def normalize_account(value):
    if pd.isna(value) or str(value).strip() == "":
        return ""

    value = str(value).strip().upper()
    return value.split("@", 1)[0]




# ==========================================================
# CREARE EXCEL
# Creazione Excel
# ==========================================================

def create_excel(
    output_file,
    sheet1_data,
    sheet2_data,
    sheet3_data
):

    # RO:
    # Cream workbook-ul Excel.
    #
    # IT:
    # Creiamo il workbook Excel.

    workbook = Workbook()


    # ======================================================
    # SHEET1
    # ======================================================

    sheet1 = workbook.active

    sheet1.title = "Utenti da cartelle AD"


    # RO:
    # Coloanele pentru Sheet1.
    #
    # IT:
    # Colonne per Sheet1.

    sheet1_headers = [
        "UserName",
        "SamAccountName",
        "Fisier sursa"
    ]


    sheet1.append(
        sheet1_headers
    )


    # RO:
    # Scriem utilizatorii extrasi din grupul AD.
    #
    # IT:
    # Scriviamo gli utenti estratti dal gruppo AD.

    for item in sheet1_data:

        sheet1.append([
            item["UserName"],
            item["SamAccountName"],
            item["Fisier sursa"]
        ])
     


    # ======================================================
    # SHEET2
    # ======================================================

    sheet2 = workbook.create_sheet(
        "utenti da AD e Attivi"
    )




    # RO:
    # Coloanele pentru rezultatul INNER JOIN.
    #
    # IT:
    # Colonne per il risultato dell'INNER JOIN.

    sheet2_headers = [
        "CN_00",
        "Principal Name",
        "Banche"
    ]


    sheet2.append(
        sheet2_headers
    )
# ===========================
# SHEET 3

# ==================================================
    sheet3 = workbook.create_sheet(
        "Sheet3"
    )

    sheet3_headers = [
        "UserName",
        "CN_00",
        #"InnerJoin",
        "Principal Name",
        "Banche"
    ]

    sheet3.append(sheet3_headers)    


    # RO:
    # Scriem rezultatele INNER JOIN.
    #
    # IT:
    # Scriviamo i risultati dell'INNER JOIN.

    for item in sheet2_data:

        sheet2.append([
            item["CN_00"],
            item["Principal Name"],
            item["Banche"]
        ])

    for item in sheet3_data:

        sheet3.append([
            item["UserName"], # --> adaugat pe 28/08/2026
            #item["InnerJoin"],
            item["CN_00"], # -- adaugat pe 28/08/2026
            item["Principal Name"],
            item["Banche"]
    ])   




    # ======================================================
    # FORMAT EXCEL
    # Formattazione Excel
    # ======================================================

    # RO:
    # Formatam header-ele.
    #
    # IT:
    # Formattiamo le intestazioni.

    for sheet in [
        sheet1,
        sheet2,
        sheet3
    ]:

        for cell in sheet[1]:

            cell.font = Font(
                bold=True
            )

            cell.alignment = Alignment(
                horizontal="center"
            )


    # RO:
    # Ajustam automat dimensiunea coloanelor.
    #
    # IT:
    # Adattiamo automaticamente la larghezza delle colonne.

    for sheet in [
        sheet1,
        sheet2
    ]:

        for column_cells in sheet.columns:

            max_length = 0

            column_letter = (
                get_column_letter(
                    column_cells[0].column
                )
            )


            for cell in column_cells:

                if cell.value is not None:

                    cell_length = len(
                        str(cell.value)
                    )

                    if cell_length > max_length:
                        max_length = cell_length


            sheet.column_dimensions[
                column_letter
            ].width = min(
                max_length + 2,
                60
            )


    # RO:
    # Inghetam primul rand.
    #
    # IT:
    # Blocchiamo la prima riga.

    sheet1.freeze_panes = "A2"
    sheet2.freeze_panes = "A2"


    # RO:
    # Salvam fisierul Excel.
    #
    # IT:
    # Salviamo il file Excel.

    workbook.save(
        output_file
    )


# ==========================================================
# PROGRAM PRINCIPAL
# Programma principale
# ==========================================================

def main():

    print()
    print("=================================================")
    print(
        "RICERCA VDI_USER_VOLTERRA_026_MT"
    )
    print(
        "RICERCA UTENTI DEL GRUPPO AD"
    )
    print("=================================================")


    # ======================================================
    # VERIFICARE MAPA PRINCIPALA
    # Verifica della cartella principale
    # ======================================================

    if not base_folder.exists():

        print(
            f"WARNING: Mapa nu exista: {base_folder}"
        )

        return


    # ======================================================
    # PASUL 1
    # PASSO 1
    #
    # Extragem UserName si SamAccountName
    # din AD-usersAndGroupsResult.csv
    # pentru grupul VDI_USER_VOLTERRA_026_MT
    # ======================================================

    sheet1_data = read_ad_groups_files(

        base_folder=base_folder,

        patterns=[
            AD_CED_Pattern,
            AD_Base_Pattern
        ],

        csv_filename=ad_groups_file,

        delimiter=ad_groups_delimiter,

        target_group=search_group
    )


    print()
    print("=================================================")
    print(
        f"Utilizatori gasiti in grup: "
        f"{len(sheet1_data)}"
    )

    print(
        f"Utenti trovati nel gruppo: "
        f"{len(sheet1_data)}"
    )

    print("=================================================")


    # ======================================================
    # PASUL 2
    # PASSO 2
    #
    # Sheet1:
    # UserName
    # SamAccountName
    # ======================================================


    # ======================================================
    # CAUTARE AD_Users_Results_attivi.csv
    # Ricerca AD_Users_Results_attivi.csv
    # ======================================================

    # RO:
    # Fisierul AD_Users_Results_attivi.csv este cautat
    # in mapa raportului lunar si in subfolderele sale.
    #
    # IT:
    # Il file AD_Users_Results_attivi.csv viene cercato
    # nella cartella del report mensile e nelle sue sottocartelle.

    attivi_files = list(
        base_folder.rglob(
            ad_users_attivi_file
        )
    )


    if not attivi_files:

        print()
        print(
            "WARNING: Nu s-a gasit "
            "AD_Users_Results_attivi.csv"
        )

        print(
            "ATTENZIONE: "
            "AD_Users_Results_attivi.csv non trovato"
        )

        return


    # RO:
    # In mod normal exista un singur fisier.
    #
    # IT:
    # Normalmente dovrebbe esistere un solo file.

    attivi_file = attivi_files[0]


    print()
    print(
        f"Fisier AD Users Attivi: {attivi_file}"
    )


    # ======================================================
    # PASUL 3
    # PASSO 3
    #
    # INNER JOIN:
    #
    # Sheet1.UserName
    #         =
    # AD_Users_Results_attivi.CN_00
    # ======================================================

    attivi_users = read_ad_users_attivi(
        attivi_file,
        csv_delimiter
    )


    # RO:
    # Lista pentru rezultatul INNER JOIN.
    #
    # IT:
    # Lista per il risultato dell'INNER JOIN.

    sheet2_data = []


# pentru innerjoinu
    sheet3_data = []


    # RO:
    # Set pentru evitarea duplicatelor.
    #
    # IT:
    # Set per evitare duplicati.

    join_keys = set()


    # ======================================================
    # EXECUTARE INNER JOIN
    # Esecuzione INNER JOIN
    # ======================================================

    for item in sheet1_data:

        user_name = (
            item["UserName"].strip()
        )


        # RO:
        # Cautam UserName in CN_00.
        #
        # IT:
        # Cerchiamo UserName in CN_00.

        matched_user = attivi_users.get(
            user_name
        )


        # RO:
        # Daca nu exista potrivire, utilizatorul
        # nu intra in Sheet2.
        #
        # IT:
        # Se non esiste una corrispondenza,
        # l'utente non viene inserito in Sheet2.

        if matched_user is None:

            continue


        join_value = normalize_account(
        matched_user["Principal Name"]
        )

        # RO:
        # Cream cheia pentru evitarea duplicatelor.
        #
        # IT:
        # Creiamo la chiave per evitare duplicati.

        join_key = (
            matched_user["CN_00"],
            matched_user["Principal Name"],
            matched_user["OU_01"]
        )


        if join_key in join_keys:

            continue


        join_keys.add(
            join_key
        )

        join_value = user_name.strip()


        # RO:
        # OU_01 este scris in Excel cu numele Banche.
        #
        # IT:
        # OU_01 viene scritto in Excel con il nome Banche.

        sheet2_data.append({

            "CN_00":
                matched_user["CN_00"],

            "Principal Name":
                matched_user["Principal Name"],

            "Banche":
                matched_user["OU_01"]
        })


        sheet3_data.append({
            #"InnerJoin": join_value,
            "UserName": user_name,
            "CN_00": matched_user["CN_00"],
            "Principal Name": matched_user["Principal Name"],
            "Banche": matched_user["OU_01"]
        })





    # ======================================================
    # STATISTICI INNER JOIN
    # Statistiche INNER JOIN
    # ======================================================

    print()
    print("=================================================")

    print(
        f"Randuri Sheet1: {len(sheet1_data)}"
    )

    print(
        f"Righe Sheet1: {len(sheet1_data)}"
    )

    print(
        f"Randuri INNER JOIN / Sheet2: "
        f"{len(sheet2_data)}"
    )

    print(
        f"Righe INNER JOIN / Sheet2: "
        f"{len(sheet2_data)}"
    )

    print(
        f"Righe INNER JOIN cu mai mult info / Sheet3: "
        f"{len(sheet3_data)}"
    )


    print("=================================================")


    # ======================================================
    # PASUL 4
    # PASSO 4
    #
    # CREARE EXCEL
    # Creazione Excel
    # ======================================================

    create_excel(
        output_file,
        sheet1_data,
        sheet2_data,
        sheet3_data
    )


    # ======================================================
    # FINAL
    # Fine
    # ======================================================

    print()
    print("=================================================")

    print(
        "Procedura terminata cu succes!"
    )

    print(
        "Procedura terminata con successo!"
    )

    print()

    print(
        f"Output: {output_file}"
    )

    print("=================================================")


# ==========================================================
# START
# Avvio
# ==========================================================

if __name__ == "__main__":

    main()    