import pandas as pd
import os

# de facut comparatii si pentru randruri
# comparam 2 fisiere csv si afisam diferentele (intr-un fisier csv nou cred ca)
# C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere

# classificazione software
directory_pathFile1 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-classificazione-software-20251219121352.csv'
directory_pathFile2 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-classificazione-software-20260119093439.csv'

# database oracle 
directory_pathFile3 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-database-oracle-20251219121001.csv'
directory_pathFile4 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-database-oracle-20260115162315.csv'

# inventario hardware
directory_pathFile5 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-inventario-hardware-20251219121533.csv'
directory_pathFile6 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-inventario-hardware-20260119093609.csv'


# denumirea fisierelor classificazione software
file_name_with_extention1 = os.path.basename(directory_pathFile1)
file_name_with_extention2 = os.path.basename(directory_pathFile2)
# denumirea fisierelor database oracle 
file_name_with_extention3 = os.path.basename(directory_pathFile3)
file_name_with_extention4 = os.path.basename(directory_pathFile4)
# denumirea fisierelor inventario hardware
file_name_with_extention5 = os.path.basename(directory_pathFile5)
file_name_with_extention6 = os.path.basename(directory_pathFile6)


# classificazione software citirea CSV fisiere
dfA = pd.read_csv(directory_pathFile1, skiprows=1)
dfB = pd.read_csv(directory_pathFile2, skiprows=1)
# database oracle citirea CSV fisiere
dfC = pd.read_csv(directory_pathFile3, skiprows=1)
dfD = pd.read_csv(directory_pathFile4, skiprows=1)
# inventario hardware citirea CSV fisiere
dfE = pd.read_csv(directory_pathFile5, skiprows=1)
dfF = pd.read_csv(directory_pathFile6, skiprows=1)

'''
# df.head()
print(f"headeruri la fisierul 1 {file_name_with_extention1} --->")
print(dfA.columns.tolist(), "\n")
print(f"headeruri la fisierul 2 {file_name_with_extention2} --->")
print(dfB.columns.tolist(), "\n")

print(" headeruri cu list() de la fisier1", list(dfA.columns))
print(" headeruri cu list() de la fisier2", list(dfB.columns))

nrOfHeadersFisier1 = len(dfA.columns)
nrOfHeadersFisier2 = len(dfB.columns)
print(f"nr de headeruri fisier 1 {file_name_with_extention1} --->", nrOfHeadersFisier1)
print(f"nr de headeruri fisier 2 {file_name_with_extention2} --->", nrOfHeadersFisier2)


if nrOfHeadersFisier1 != nrOfHeadersFisier2:
    print("!!nr de headeruri se difera")
else:
    print("!!nr de headeruri sunt difera")

diferenteHeaderuri = list(set(dfB.columns) - set(dfA.columns))
print("diferente intre headeruri sunt--- headeruri care sunt in fisier2 dar nu sunt in fisier1 sunt -->", diferenteHeaderuri)



'''
def load_csv_auto(path):
    """
    Citește CSV indiferent dacă primul rând este 'sep=,' sau direct header
    """
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline().lower()

    sep = ','
    skip = 0

    if first_line.startswith('sep='):
        sep = first_line.strip().split('=')[1]
        skip = 1

    try:
        return pd.read_csv(
            path,
            sep=sep,
            skiprows=skip,
            encoding='utf-8'
        )
    except Exception:
        return pd.read_csv(
            path,
            sep=sep,
            skiprows=skip,
            encoding='latin1',
            on_bad_lines='skip'
        )


def comparare_csv(firstFile_path, secondFile_path):
    try:
        if not os.path.exists(firstFile_path):
            print(f"Eroare: fisierul1 {firstFile_path} nu exista")
            return
        if not os.path.exists(secondFile_path):
            print(f"Eroare: fisierul2 {secondFile_path} nu exista")
            return

        # citire smart
        dfPrimul = load_csv_auto(firstFile_path)
        dfAldoilea = load_csv_auto(secondFile_path)

        numeleFisier1 = os.path.basename(firstFile_path)
        numeleFisier2 = os.path.basename(secondFile_path)

        # verificare headeruri
        print(f"\nHeaderuri fisier1 {numeleFisier1}:")
        print(list(dfPrimul.columns))

        print(f"\nHeaderuri fisier2 {numeleFisier2}:")
        print(list(dfAldoilea.columns))

        print("\nNumar headeruri:",
              len(dfPrimul.columns), "vs", len(dfAldoilea.columns))

        set1 = set(dfPrimul.columns)
        set2 = set(dfAldoilea.columns)

        print("\nHeaderuri doar in fisier2 (<<):",
              list(set2 - set1))
        print("Headeruri doar in fisier1 (>>):",
              list(set1 - set2))

        # comparare randuri
        print("\nComparare numar randuri:")
        print(f"{numeleFisier1}: {dfPrimul.shape}")
        print(f"{numeleFisier2}: {dfAldoilea.shape}")

        print("\n================ AFISARE ALINIATA =================")

        col1 = list(dfPrimul.columns)
        col2 = list(dfAldoilea.columns)

        i = j = 0
        while i < len(col1) or j < len(col2):
            c1 = col1[i] if i < len(col1) else ""
            c2 = col2[j] if j < len(col2) else ""

            if i < len(col1) and j < len(col2) and c1 == c2:
                print(f"{c1:<60}{c2:<60}")
                i += 1
                j += 1
            elif j < len(col2) and c2 not in set1:
                print(f"{'':<60}<< {c2}")
                j += 1
            elif i < len(col1) and c1 not in set2:
                print(f">> {c1:<57}{''}")
                i += 1
            else:
                print(f"{c1:<60}{c2:<60}")
                i += 1
                j += 1

        print("=" * 120)

    except Exception as e:
        print(f"Eroare neasteptata: {e}")



'''
#aplicam procedura
comparare_csv(directory_pathFile1, directory_pathFile2)

#salvataggio in txt
output_fileTXT = os.path.join(cm.out_path, "Lista gruppi Office.txt")
with open(output_fileTXT, "w", encoding="utf-8") as f:
    for gruppo, source in gruppi_standard_list:
        f.write(f"{gruppo}|{source}\n")
    f.write("\n")  # Linie goală între secțiuni
    for gruppo, source in gruppi_professional_list:
        f.write(f"{gruppo}|{source}\n")

'''


def generate_raport_diferente_OLD(fisier1, fisier2,
                              nume_report=r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\raport_diferente.txt",
                              titlu="===Asset client ==="):
    """
    f-tia creaza raport in format txt care compara headers  a doua fisiere csv.
    se foloseste << and >>
    :param fisier1:
    :param fisier2:
    :param nume_report:
    :param titlu:
    :return:
    """
    if not os.path.exists(fisier1):
        print(f"eroare: fisier1 {fisier1} nu exista!")
        return
    if not os.path.exists(fisier2):
        print(f"eroare: fisier2 {fisier2} nu exista!")
        return

    # citire CSV -- probabil aici e problema pentru ictg/BigFix
    df1 = pd.read_csv(fisier1, skiprows=1)
    df2 = pd.read_csv(fisier2, skiprows=1)

    # headeruri
    header1 = df1.columns.tolist()
    header2 = df2.columns.tolist()

    # headeruri lipsa ]
    lipsa_in_B = [h for h in header1 if h not in header2]  # apare in A, dar nu sunt in B -->  >>
    lipsa_in_A = [h for h in header2 if h not in header1]  # apare in B, dar nu-s in A --> <<

    # generare raport txt
    with open(nume_report, "w", encoding="utf-8") as f:

        f.write(titlu + "\n")
        f.write("=" * 180 + "\n\n")  # cream un sir format din 180 de caracter == unu dupa altu

        f.write("grafana precedente".ljust(60))  # adaugam 60 de spatii
        f.write("cmdb (attuale \n\n")

        max_len = max(len(header1), len(header2))
        for i in range(max_len):
            col1 = header1[i] if i < len(header1) else ""
            col2 = header2[i] if i < len(header2) else ""

            # indicatori << >>
            indicator = ""
            if col1 and col1 not in header2:
                indicator = " >>"  # va aparea om fisierul A
            if col2 and col2 not in header1:
                indicator = " <<" + col2

            line = col1.ljust(60) + indicator.ljust(60) + indicator
            f.write(line + "\n")
    print(f"\nRaport s-a generat cu succes in : {nume_report}")




# Apelam functia -- pentru inceput -- Asset Client
# generate_raport_diferente(directory_pathFile1, directory_pathFile2)

# apelam functia pentru clasificazione softare
print("apelarea functiei pentru clasificazione softare")
comparare_csv(directory_pathFile1, directory_pathFile2)
# apelam functia pentru database oracle 
print("apelarea functiei pentru database oracle ")
comparare_csv(directory_pathFile3, directory_pathFile4)
#apelam functia pentru inventario hardware
print("apelarea functiei pentru inventario hardware")
comparare_csv(directory_pathFile5, directory_pathFile6)


#######################33*************###################33

#generam pentru TXT
def generate_raport_diferente(f1, f2, nume_report, titlu=""):

    if not os.path.exists(f1) or not os.path.exists(f2):
        print("Eroare: unul din fișiere nu există!")
        return

    df1 = load_csv_auto(f1)
    df2 = load_csv_auto(f2)

    col1 = list(df1.columns)
    col2 = list(df2.columns)

    set1 = set(col1)
    set2 = set(col2)

    nume_f1 = os.path.basename(f1)
    nume_f2 = os.path.basename(f2)

    with open(nume_report, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 120 + "\n")
        if titlu:
            f.write(titlu + "\n")

        f.write(f"{'Fisier vechi / precedent':<60}{'Fisier nou / actual':<60}\n")
        f.write(f"{nume_f1:<50}  vs  {nume_f2}\n")
        f.write("-" * 120 + "\n")

        i = j = 0
        while i < len(col1) or j < len(col2):
            c1 = col1[i] if i < len(col1) else ""
            c2 = col2[j] if j < len(col2) else ""

            if i < len(col1) and j < len(col2) and c1 == c2:
                line = f"{c1:<60}{c2:<60}"
                i += 1
                j += 1
            elif j < len(col2) and c2 not in set1:
                line = f"{'':<60}<< {c2}"
                j += 1
            elif i < len(col1) and c1 not in set2:
                line = f">> {c1:<57}{''}"
                i += 1
            else:
                line = f"{c1:<60}{c2:<60}"
                i += 1
                j += 1

            f.write(line.rstrip() + "\n")

        f.write("-" * 120 + "\n")



# Exemplu de apelare (poți înlocui în compara_toate_fisierele)
# generate_raport_diferente(
#     r"...\Asset Client (ALL)-data-2025-11-03 12_48_57.csv",
#     r"...\Asset Client (ALL)-data-2025-11-06 11_08_56.csv",
#     "raport_diferente_ASSET.txt",
#     titlu="=== Asset Client ==="
# )


def compara_toate_fisierele(fisiere, raport="raport_diferente_ICTG_decembrie vs ianuarie.txt"):
    open(raport, "w").close()

    if len(fisiere) % 2 != 0:
        print("Lista trebuie sa contina perechi")
        return

    for i in range(0, len(fisiere), 2):
        generate_raport_diferente(
            fisiere[i],
            fisiere[i+1],
            raport,
            titlu=""
        )

    print("Raport generat:", raport)



fisiere = [
    #pclasificazione software
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-classificazione-software-20251219121352.csv",
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-classificazione-software-20260119093439.csv",

    #database oracle
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-database-oracle-20251219121001.csv",
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-database-oracle-20260115162315.csv",

    #inventario hardware
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-inventario-hardware-20251219121533.csv",
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere_ictg\ICTG-0-inventario-hardware-20260119093609.csv"

]

compara_toate_fisierele(fisiere)

#deocamndata hardcodat







