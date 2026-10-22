import pandas as pd
import os

# de facut comparatii si pentru randruri
# comparam 2 fisiere csv si afisam diferentele (intr-un fisier csv nou cred ca)
# C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere
# Asset Client
directory_pathFile1 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Client (ALL)-data-2025-11-03 12_48_57.csv'
directory_pathFile2 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Client (ALL)-data-2025-11-06 11_08_56.csv'
# Asset Software
directory_pathFile3 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Software (ALL - Selezionare il cliente in alto)-data-2025-11-03 15_10_12.csv'
directory_pathFile4 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Software (ALL - Selezionare il cliente in alto)-data-2025-11-24 11_45_42.csv'

#Asset Server
directory_pathFile5 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Server (ALL)-data-2025-11-03 12_55_30.csv'
directory_pathFile6 = r'C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Server (ALL)-data-2025-11-24 11_25_23.csv'


# denumirea fisierelor Asset Client
file_name_with_extention1 = os.path.basename(directory_pathFile1)
file_name_with_extention2 = os.path.basename(directory_pathFile2)
# denumirea fisierelor Asset Software
file_name_with_extention3 = os.path.basename(directory_pathFile3)
file_name_with_extention4 = os.path.basename(directory_pathFile4)
# denumirea fisierelor Asset Server
file_name_with_extention5 = os.path.basename(directory_pathFile5)
file_name_with_extention6 = os.path.basename(directory_pathFile6)


# Asset Client citirea CSV fisiere
dfA = pd.read_csv(directory_pathFile1, skiprows=1)
dfB = pd.read_csv(directory_pathFile2, skiprows=1)
# Asset Software citirea CSV fisiere
dfC = pd.read_csv(directory_pathFile3, skiprows=1)
dfD = pd.read_csv(directory_pathFile4, skiprows=1)
# Asset Server citirea CSV fisiere
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


def comparare_csv(firstFile_path, secondFile_path):
    try:
        if not os.path.exists(firstFile_path):
            print(f"Eroare: fisierul1 {firstFile_path} nu exista")
            return
        if not os.path.exists(secondFile_path):
            print(f"Eroare: fisierul2 {secondFile_path} nu exista")
            return

        try:
            df1 = pd.read_csv(firstFile_path, encoding='utf-8', sep=',')
            df2 = pd.read_csv(secondFile_path, encoding='utf-8', sep=',')
        except pd.errors.ParserError:
            print("Erore la parsare. Se incearca cu delimitator ; si encoding latin1")
            df1 = pd.read_csv(firstFile_path, encoding='latin1', sep=';')
            df2 = pd.read_csv(secondFile_path, encoding='latin1', sep=';')

        # extragem numele fisierelor pentru comparatie
        numeleFisier1 = os.path.basename(firstFile_path)
        numeleFisier2 = os.path.basename(secondFile_path)

        dfPrimul = pd.read_csv(firstFile_path, skiprows=1)
        dfAldoilea = pd.read_csv(secondFile_path, skiprows=1)

        # verificam lungimea nr de headeruri
        number_of_headersFile1 = len(dfPrimul.columns)
        number_of_headersFile2 = len(dfAldoilea.columns)

        # afisam headeruri
        print(f" headeruri cu list() de la fisier1 {numeleFisier1}", list(dfPrimul.columns))
        print(f" headeruri cu list() de la fisier2 {numeleFisier2}", list(dfAldoilea.columns))

        if number_of_headersFile1 != number_of_headersFile2:
            print("!!nr de headeruri se difera")
        else:
            print("!!nr de headeruri sunt egale")

        # afisam numar de headeruri
        print("numar de headeruri la fisier1 --->", number_of_headersFile1)
        print("numar de headeruri la fisier2 --->", number_of_headersFile2)

        # diferentierea de headeruri
        diferentiereDeHeaderuriA = list(set(dfAldoilea.columns) - set(dfPrimul.columns))
        print("diferente intre headeruri sunt -- headers din fisier2 dar nu-s in fisier1 -->", diferentiereDeHeaderuriA)

        diferentiereDeHeaderuriB = list(set(dfPrimul.columns) - set(dfAldoilea.columns))
        print("diferente intre headeruri sunt -- headers din fisier1 dar nu-s in fisier2 -->", diferentiereDeHeaderuriB)

        # verifica daca au aceleasi coloane - # afisam headeruri prin metoda a 2-a
        if list(dfPrimul.columns) != list(dfAldoilea.columns):
            print("coloanele sunt diferite!")
            print("file1", dfPrimul.columns.tolist())
            print("file2", dfAldoilea.columns.tolist())

#comparam nr de randruri
            print("!!!! comparam numarul de randuri")
            if dfPrimul.shape[0] != dfAldoilea.shape[0]:
                print("!! nr de randuri sunt diferite! ---")
                print(numeleFisier1,"are randrui si coloane")
                print(dfPrimul.shape) ## <---- poate asa va araa corect
                print(numeleFisier2,"are randrui si coloane")
                print(dfAldoilea.shape)
                print(f"{numeleFisier1}-->{dfPrimul.shape[0]} randuri vs{numeleFisier2}--->{dfAldoilea.shape[0]} randuri")

            else:
                print("!! nr de randuri sunt egale! ---")

            print("\n" + "=" * 120)
            print("!!!!*************!!! AFISARE COLOANE")
            print("\n" + "=" * 120)

            # ===================== afisarea headerurilor in 2 coloane ======================================
            print(
                f"afisare CLASICA headere in douoa coloane la fisier1 {numeleFisier1} si fisier2 {numeleFisier2}".center(
                    120))
            # cream coloanele
            # asiguram ca listele sunt de aceeasi lungime comletand cu string gol
            col1 = list(dfPrimul.columns)
            col2 = list(dfAldoilea.columns)

            # idk ce face
            max_len = max(len(col1), len(col2))
            col1 += [""] * (max_len - len(col1))
            col2 += [""] * (max_len - len(col2))

            # latimi de coloane
            width1 = 60
            width2 = 60

            # afisam
            print(f"{'Fisier1':<{width1}} {'Fisier2':<{width2}}")
            print("-" * 120)
            print("-" * (width1 + width2))

            for c1, c2 in zip(col1, col2):  # --- taman ciclu pentru sa arate coloanele -- in mod clasic
                print(f"{c1:<{width1}} {c2:<{width2}}")  # --- printam coloanele
            print("=" * 120)

            print(
                f"afisarea diferentelor intre headeruri DUPA CERINTA la fisiere *** {numeleFisier1} si *** {numeleFisier2}".center(
                    120))
            # cum se cere de la Claudio
            print(f"{'Fisier1':<{width1}} {'Fisier2':<{width2}}")
            print("-" * 120)
            print("-" * (width1 + width2))
            # listele originale
            col1 = list(dfPrimul.columns)
            col2 = list(dfAldoilea.columns)

            # seturi pentru comparație
            set1 = set(col1)
            set2 = set(col2)

            # pentru afișare în ordinea corectă:
            index1 = 0
            index2 = 0

            while index1 < len(col1) or index2 < len(col2):

                c1 = col1[index1] if index1 < len(col1) else ""
                c2 = col2[index2] if index2 < len(col2) else ""

                # cazul 1: aceeași coloană în ambele fișiere → afișare normală
                if index1 < len(col1) and index2 < len(col2) and c1 == c2:
                    print(f"{c1:<60}{c2:<60}")
                    index1 += 1
                    index2 += 1

                # cazul 2: coloană care există doar în fisier2 → apare cu "<<"
                elif index2 < len(col2) and c2 not in set1:
                    print(f"{'':<60}<< {c2:<57}")
                    index2 += 1

                # cazul 3: coloană care există doar în fisier1 → apare cu ">>"
                elif index1 < len(col1) and c1 not in set2:
                    print(f">> {c1:<57}{'':<60}")
                    index1 += 1

                else:
                    # fallback sigur
                    print(f"{c1:<60}{c2:<60}")
                    index1 += 1
                    index2 += 1

            print("-" * 120)
            #######################################################################
            # ******************************************
            ################################################################################3

            return  # <----- NU STERGEM!!
        # hz de ce acesta nu ni se arata ---------------------------
        # verifica daca au acelasi numar de randuri
        if dfPrimul.shape[0] != dfAldoilea.shape[0]:
            print(
                f"numar diferit de randuri {numeleFisier1}: {dfPrimul.shape[0]} vs {numeleFisier2}: {dfAldoilea.shape[0]}")
        else:
            print(f" numar egal de randuri: {dfPrimul.shape[0]} vs {dfAldoilea.shape[0]} ")
            # comparam continutul
        diferente = df1.compare(df2)
        if diferente.empty:
            print("fisiere sunt identice!")
        else:
            print("diferente gasite:\n", diferente)





    except FileNotFoundError as e:
        print(f"Eroare: Unul dintre fișiere nu a fost găsit: {e}")
    except pd.errors.ParserError as e:
        print(f"eroare la parsing csv: {e}. verifica delimitatorii sau encoding")
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

# apelam functia pentru Asset Client
print("apelarea functiei pentru Asset Client")
comparare_csv(directory_pathFile1, directory_pathFile2)
# apelam functia pentru Asset Software
print("apelarea functiei pentru Asset Software")
comparare_csv(directory_pathFile3, directory_pathFile4)
#apelam functia pentru Asset Servere
print("apelarea functiei pentru Asset Server")
comparare_csv(directory_pathFile5, directory_pathFile6)


#######################33*************###################33

#generam pentru TXT
def generate_raport_diferente(f1, f2, nume_report, titlu=""):
    import pandas as pd
    import os

    def load_csv_smart(path):
        try:
            return pd.read_csv(path, skiprows=1)
        except:
            try:
                return pd.read_csv(path, skiprows=1, encoding='latin1', sep=';')
            except:
                return pd.read_csv(path, skiprows=1, encoding='utf-8', on_bad_lines='skip')

    if not os.path.exists(f1) or not os.path.exists(f2):
        print("Eroare: unul din fișiere nu există!")
        return

    df1 = load_csv_smart(f1)
    df2 = load_csv_smart(f2)

    col1 = list(df1.columns)
    col2 = list(df2.columns)

    set1 = set(col1)
    set2 = set(col2)

    nume_f1 = os.path.basename(f1)
    nume_f2 = os.path.basename(f2)

    with open(nume_report, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 120 + "\n")
        if titlu:
            f.write(f"{titlu}\n")
        f.write(f"Comparare header-e:   {nume_f1:<50}  vs  {nume_f2}\n")
        f.write("-" * 120 + "\n")

        # titlu coloane
        f.write(f"{'Fisier vechi / precedent':<60} {'Fisier nou / actual':<60}\n")
        f.write("-" * 120 + "\n")

        # logica exactă ca în terminal
        index1 = 0
        index2 = 0

        while index1 < len(col1) or index2 < len(col2):
            c1 = col1[index1] if index1 < len(col1) else ""
            c2 = col2[index2] if index2 < len(col2) else ""

            if index1 < len(col1) and index2 < len(col2) and c1 == c2:
                # coloană identică în ambele
                line = f"{c1:<60}{c2:<60}"
                index1 += 1
                index2 += 1
            elif index2 < len(col2) and c2 not in set1:
                # coloană doar în fisierul 2 (nou)
                line = f"{'':<60}<< {c2}"
                index2 += 1
            elif index1 < len(col1) and c1 not in set2:
                # coloană doar în fisierul 1 (vechi)
                line = f">> {c1:<57}{'':<60}"
                index1 += 1
            else:
                # fallback - rar
                line = f"{c1:<60}{c2:<60}"
                index1 += 1
                index2 += 1

            f.write(line.rstrip() + "\n")   # rstrip() elimină spațiile inutile de la final

        f.write("-" * 120 + "\n\n")


# Exemplu de apelare (poți înlocui în compara_toate_fisierele)
# generate_raport_diferente(
#     r"...\Asset Client (ALL)-data-2025-11-03 12_48_57.csv",
#     r"...\Asset Client (ALL)-data-2025-11-06 11_08_56.csv",
#     "raport_diferente_ASSET.txt",
#     titlu="=== Asset Client ==="
# )


def compara_toate_fisierele(fisiere, raport="raport_diferente_ASSET.txt"):
    # curățăm raportul vechi
    open(raport, "w").close()

    # verificăm că există exact un număr par de fișiere
    if len(fisiere) % 2 != 0:
        print("Eroare: lista de fișiere trebuie să aibă un număr par (perechi).")
        return

    # comparăm în perechi: (0,1), (2,3), (4,5), ...
    for i in range(0, len(fisiere), 2):
        generate_raport_diferente(
            fisiere[i],
            fisiere[i+1],
            raport,
            titlu=""
        )

    print("Raport final generat:", raport)


fisiere = [
    #Asset Client
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Client (ALL)-data-2025-11-03 12_48_57.csv",
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Client (ALL)-data-2025-11-06 11_08_56.csv",

    #Asset Sofware
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Software (ALL - Selezionare il cliente in alto)-data-2025-11-03 15_10_12.csv",
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Software (ALL - Selezionare il cliente in alto)-data-2025-11-24 11_45_42.csv",

    #Asset Server
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Server (ALL)-data-2025-11-03 12_55_30.csv",
    r"C:\Users\crme240\OneDrive - ION\Desktop\comparare_fisiere\Asset Server (ALL)-data-2025-11-24 11_25_23.csv"
]

compara_toate_fisierele(fisiere)

#deocamndata hardcodat







