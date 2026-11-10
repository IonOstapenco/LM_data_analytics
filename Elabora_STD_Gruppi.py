
import os
import re
import json
import pandas as pd


# ============================================================----
# 1. LETTURA PARAMETRI
# 1. CITESTE PARAMETRI
# =========================================================

with open(
    "Parametri.json",
    "r",
    encoding="utf-8-sig" # !! --> uneori poate sa fie utf-16 !!! 
) as f:
    config = json.load(f)


base_path = os.path.join( # --> pathul de baza
    config["Source_dir"],
    config["Report_dir"]
)

output_dir = config["Output_dir"] # --> directory di output

group_file = os.path.join(
    base_path,
    output_dir,
    config["OUT_Lista_Gruppi"]  # --> se citeste FLEXERA_Lista gruppi Office.txt 
)

ad_users_file = os.path.join(
    base_path,
    "output-1",
    config["AD_Users_Results_attivi"] # --> se citeste fisier cu userii activi / utenze attive
)

output_path = os.path.join( # ---> se creaza mapa de output "gruppi"
    base_path,
    "gruppi"
)

os.makedirs(output_path, exist_ok=True)


# ===============================================-=================
# 2. VERIFICAM FISIERE DE INPUT
# 2. VERIFICA FILE INPUT
# ======================================================--===

if not os.path.isfile(group_file):
    raise FileNotFoundError( # --> va afisa daca nu s-a gasit fisier FLEXERA_Lista gruppi Office.txt
        f"File gruppi Flexera non trovato: {group_file}"
    )

if not os.path.isfile(ad_users_file):
    raise FileNotFoundError(
        f"File AD utenti attivi non trovato: {ad_users_file}"
    )


# =========================================================
#
# 3. LETTURA GRUPPI OFFICE STD DA FLEXERA
# 3. CITIRE GRUPPI OFFICE STD de la FLEXERA
# =========================================================

groups = set()

with open(
    group_file,
    "r",
    encoding="utf-8-sig",
    errors="replace"
) as f:

    for line in f:

        parts = line.rstrip("\r\n").split("|")

        if (
            len(parts) >= 2
            and parts[1].strip().upper() == "STD" # standard
        ):

            group = parts[0].strip().lower()

            # Normalizzazione: _prod -> _prd
            group = re.sub(r"_prod$", "_prd", group) # --> production

            groups.add(group)


print(f"Gruppi STD iniziali: {len(groups)}")


# =========================================================
# 4. IDENTIFICAZIONE deii GRUPPI MISTI PRD / ADS / COL
# 4. IDENTIFICAREA grupelor mixte PRD / ADS / COL
# =========================================================

group_map = {}

for group in groups:

    group = group.strip().lower()

    match = re.match(
        r"^(.*)_(prd|ads|col)$",
        group
    )

    if match:

        base = match.group(1)
        group_type = match.group(2)

        if base not in group_map:
            group_map[base] = set()

        group_map[base].add(group_type)

# EXCEPTII pentru mentinere!
# Eccezioni da mantenere
exceptions = {
    "ctx_047_tta"
}


# Manteniamo:
# -- bazele cu excluderi PRD
# - basi con esclusivamente PRD
# -- baze prezente la exceptii
# - basi presenti nelle eccezioni

valid_bases = {
    base
    for base, types in group_map.items()
    if (
        (types == {"prd"})
        or (base in exceptions)
    )
}


# =========================================================---=-=======
# 5. RECONSTRUCTIA LISTEI FINALE DE GRUPE
# 5. RICOSTRUZIONE LISTA FINALE DEI GRUPPI
# =========================================================

groups = [] # ---> grupuri/ grupe

for base in sorted(valid_bases):

    # Eccezione speciale
    if base == "ctx_047_tta": # --- > exceptii speciaele
        groups.append(f"{base}_ads") # --> se dadauga la ADS

    else:
        groups.append(f"{base}_prd") # --> se adauga in _prd


print(f"Gruppi STD finali: {len(groups)}") # --> grupe STD finale


# =====================================================----------====
# 6. LETTURA AD USERS ATTIVI
# 6. CITIREA AD USERS ATTIVI 
# =======================================================

#Il file contiene la prima riga "sep=|".
# La saltiamo perr leggere correttamente header.

# Fisierul contine primul rand "sep=|".
# il sarim pentru citirea corecta a headerului / antetului



ad_users_df = pd.read_csv(
    ad_users_file,
    sep="|",
    skiprows=1,
    dtype=str,
    encoding="utf-8-sig"
)

# Pulizia delle headers
# curatirea headerurilor
ad_users_df.columns = (
    ad_users_df.columns
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)


# verificarea coloanelor obligatorii!!
# Verifica delle colonne obbligatorie
required_columns = {
    "Name",
    "Principal Name",
    "OU_01"
}

missing_columns = ( # ---> coloane care lipsesc
    required_columns - set(ad_users_df.columns)
)

if missing_columns:
    raise ValueError(
        "Colonne mancanti nel file AD: "
        f"{sorted(missing_columns)}"
    )


# ========================================================------==
# 7. NORMALIZARE SAMACCOUNTNAME 
# 7.   NORMALIZAZIONE SAMACCOUNTNAME
# =========================================================

def normalize_sam(value):

    if pd.isna(value):
        return ""

    #  Esempio: AG00924@ced.it -> AG00924
    # Exemplu: AG00924@ced.it -> AG00924
    return str(value).split("@")[0].strip().upper()


# Cream o coloana tehnica pentru comparare
# Creieamo una colona tehnica per il confronto
ad_users_df["SAM_norm"] = (
    ad_users_df["Principal Name"]
    .apply(normalize_sam)
)


# ======================================================--====
# 8. CREAREA MAP SAMACCOUNTNAME -> BANCHE
# 8. CREAZIONE MAP SAMACCOUNTNAME -> BANCHE
# =========================================================

banche_map = {}

for _, row in ad_users_df.iterrows():

    sam = row["SAM_norm"]

    if not sam:
        continue

    # Pastram primul OU_01 (organizational Username) pentru fiecare SAM,
    # tot asa, cum la procedura PowerShell original.    

    # Conserviamo il primo OU_01 per ogni SAM, come nella procedura PowerShell originale.

    if sam not in banche_map:

        banche_map[sam] = (
            row["OU_01"]
            if pd.notna(row["OU_01"])
            else ""
        )


print(f"Utenti AD caricati: {len(ad_users_df)}")
print(f"SAM presenti nella mappa banche: {len(banche_map)}")


# ============================================================
# 9. NORMALIZAREA la NAM=
# 9. NORMALIZZAZIONE NOMI
# =========================================================

def normalize_name(name):

    if pd.isna(name) or not str(name).strip():
        return ""

    name = str(name).strip()


    # Stergerea # Rimuove ?, _, -, . de la capat
    # Rimuove ?, _, -, . alla fine
    name = re.sub(r"[?_.-]+$", "", name)

    # Eliminarea numerelir finale, precedate de spatii
    # Rimuoverea numeri finali preceduti da spazi
    name = re.sub(r"\s+\d+$", "", name)

    # Stergerea sufixelor cum ar fi _1, _2, _3
    # Rimuove suffissi come essere _1, _2, _3
    name = re.sub(r"[_ ]+\d+$", "", name)

    # Reduce spatiile multiple
    # Riduce gli spazi multipli
    name = re.sub(r"\s+", " ", name)

    # Elimina cuvantul "bis" de la capat
    # Rimuove la parola bis alla fine
    name = re.sub(
        r"\s+bis$",
        "",
        name,
        flags=re.IGNORECASE
    )

    return name.strip()



# ===================---==============================================
# 10. CAUTAREA GRUPURI IN FISIERELE ACTIVE DIRECTORY
# 10. RICERCA GRUPPI NEI FILE ACTIVE DIRECTORY
# =========================================================

all_results = [] # --> lista, strucutra de date,seamana ca in Java

# Normalizam grupurile pentru comparare
# Normalizziamo i gruppi per il confronto
groups_set = {
    group.strip().casefold()
    for group in groups
}

for root, _, filenames in os.walk(base_path):

    for filename in filenames:

        if filename != "AD-usersAndGroupsResult.csv":
            continue

        current_file = os.path.join(root, filename)

        # Citirea CSV cu separator ;
        # Leggere CSV con separator ;
        ad_groups_df = pd.read_csv(
            current_file,
            sep=";",
            dtype=str,
            encoding="utf-16", # !!! atentie la ENCODING, in fiecare luna poate sa se schimbe!
            keep_default_na=False
        )


        # Curatirea headers
        #Pulizia headers
        ad_groups_df.columns = (
            ad_groups_df.columns
            .str.replace("\ufeff", "", regex=False)
            .str.strip()
        )

        required_ad_columns = {
            "GroupName",
            "UserName",
            "SamAccountName"
        }

        missing = required_ad_columns - set(
            ad_groups_df.columns
        )

        if missing:
            raise ValueError(
                f"Colonne mancanti in {current_file}: "
                f"{sorted(missing)}"
            )

        # Normalizzazione GroupName
        ad_groups_df["_GROUP_NORM"] = (
            ad_groups_df["GroupName"]
            .str.strip()
            .str.casefold()
        )

        # Pastram doar recorduri ale grupelor gasite
        # Conserviamo solo i record dei gruppi cercati
        matched_df = ad_groups_df[
            ad_groups_df["_GROUP_NORM"].isin(groups_set)
        ].copy()

        print(
            f"File: {filename} | "
            f"Righe lette: {len(ad_groups_df)} | "
            f"Righe corrispondenti: {len(matched_df)}"
        )

        for _, row in matched_df.iterrows():

            all_results.append({
                "Group": row["GroupName"].strip(),
                "Name": normalize_name(row["UserName"]),
                "SamAccountName": row["SamAccountName"].strip(),
                "SourceFile": current_file
            })


# Crearea DataFrame
#Creazione DataFrame
result_columns = [
    "Group",
    "Name",
    "SamAccountName",
    "SourceFile"
]

all_results_df = pd.DataFrame(
    all_results,
    columns=result_columns
)

print(
    "Record trovati prima della pulizia: "
    f"{len(all_results_df)}"
)



# =================================-===============================
# 11. ELIMINAREA USERILOR TEST
# 11.  ELIMINAZIONE USERS TEST
# =========================================================

all_results_df = all_results_df[
    ~all_results_df["Name"].str.contains(
        r"\btest\b",
        case=False,
        na=False,
        regex=True
    )
].copy()


# ================================================================
# 12. STERGERE LOGIN FOLOSITE CA NAME
# 12. ELIMINAZIONE LOGIN USATI COME NOMI
# =========================================================

all_results_df["_SAM"] = (
    all_results_df["SamAccountName"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

all_results_df["_NAME"] = (
    all_results_df["Name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

# Pentru fiecare SAM verificam daca exista cel putin o inregistrare cu un alt nume decat acel de login.
# Per ogni SAM controlliamo se esiste almeno  un record con un nome diverso dal login

has_real_name = (
    all_results_df["_NAME"]
    != all_results_df["_SAM"]
).groupby(
    all_results_df["_SAM"]
).transform("any")



# Daca exista un nume real pentru acelasi SAM, 
# stergem inregistrarile in care Name se potriveste cu datele de login

# Se esiste un nome reale per lo stesso SAM, 
# eliminiamo i record in cui Name coincide con il login.

all_results_df = all_results_df[
    (
        all_results_df["_NAME"]
        != all_results_df["_SAM"]
    )
    | (~has_real_name)
].copy()

all_results_df.drop(
    columns=["_SAM", "_NAME"],
    inplace=True
)


# =============================--==============================
# 13. ELIMINAREA DUPLICATELOR
# 13. ELIMINAZIONE dei DUPLICATI
# =========================================================


# Unicitatea bazata pe Group, Name si SamAccountName.
# !!!! SourceFile nu participa la criteriul de unicitate

# Unicità basata su Group, Name e SamAccountName.
# SourceFile non partecipa al criterio di unicità.

clean_results = (
    all_results_df
    .drop_duplicates(
        subset=[
            "Group",
            "Name",
            "SamAccountName"
        ]
    )
    .sort_values(
        ["Group", "Name", "SamAccountName"],
        kind="stable"
    )
    .reset_index(drop=True)
)


# ================================================================
# 14. UNIQUE NAMES
# =========================================================

clean_results_name = (
    clean_results[["Name"]]
    .drop_duplicates()
    .sort_values("Name", kind="stable")
    .reset_index(drop=True)
)


# =========================================================
# 15. UNIQUE SAMACCOUNTNAME
# ==========================================================

clean_results_sam = (
    clean_results[["SamAccountName"]]
    .drop_duplicates()
    .sort_values("SamAccountName", kind="stable")
    .reset_index(drop=True)
)


# =========================================================
# 16. NAMES BANCHE
# =========================================================

clean_results_with_banche = clean_results.copy()

clean_results_with_banche["Banche"] = (
    clean_results_with_banche["SamAccountName"]
    .apply(normalize_sam)
    .map(banche_map)
    .fillna("")
)



# =========================================================
# 17. MATCH UNIQUE NAMES VS AD USERS
# 17. MATCH CON SAMACCOUNTNAME E CN_00
# =========================================================

# Normalizarea account: 
# YAE1189@rev.ced.it -> YAE1189
# Normalizzazione account:
# YAE1189@rev.ced.it -> YAE1189

def normalize_account(value):

    if pd.isna(value) or not str(value).strip():
        return ""

    return str(value).strip().upper().split("@", 1)[0]


# Normalizarea numelor pentru comparare
# Normalizzazione nomi per il confronto

def normalize_text(value):

    if pd.isna(value):
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value).strip()
    ).upper()


# ------------------------------------------------------------
# 17.1 CREAREA MAP PRINCIPAL NAME -> AD USER
# 17.1 CREAZIONE MAP PRINCIPAL NAME -> AD USER
# ---------------------------------------------------------

ad_by_account = {}
ad_by_name = {}

for _, row in ad_users_df.iterrows():

    principal = normalize_account(
        row["Principal Name"]
    )

    cn_name = normalize_text(
        row["CN_00"]
    )


    # Pastram primul record pentru account
    # Conserviamo il primo record per account

    if principal and principal not in ad_by_account:

        ad_by_account[principal] = row

    # Pastram primul record pentru CN_00 
    #Conserviamo il primo record per CN_00

    if cn_name and cn_name not in ad_by_name:

        ad_by_name[cn_name] = row


# -------------------------------------------------------------
# 17.2 MATCH CU PRIORITATEA SAMACCOUNTNAME
# 17.2 MATCH CON PRIORITA' SAMACCOUNTNAME
# ---------------------------------------------------------

match_results = []

match_sam_count = 0
match_name_count = 0

for _, item in clean_results.iterrows():

    sam = normalize_account(
        item["SamAccountName"]
    )

    name = normalize_text(
        item["Name"]
    )

    # PRIMA METODA:
    # SamAccountName = Principal Name normalizat
    # PRIMA METODO:
    # SamAccountName = Principal Name normalizzato

    matched_user = ad_by_account.get(sam)

    if matched_user is not None:

        match_sam_count += 1

    else:

        # A DOUA METODA:
        # Name = CN_00
        # SECONDO METODO:
        # Name = CN_00

        matched_user = ad_by_name.get(name)

        if matched_user is not None:

            match_name_count += 1

    # Daca nu exista nici o corespundere
    # nu-l inseram recodul.
    # Se non existe nessuna corrispondenza,
    # non inseriamo il record.

    if matched_user is None:
        continue

    match_results.append({

        "Name": item["Name"],

        "Principal Name":
            matched_user["Principal Name"],

        "Banche":
            matched_user["OU_01"]
    })


# ---------------------------------------------------------=--
# 17.3 CREAREA DATAFRAME FINAL
# 17.3 CREAZIONE DATAFRAME FINALE
# ---------------------------------------------------------

match_df = pd.DataFrame(
    match_results,
    columns=[
        "Name",
        "Principal Name",
        "Banche"
    ]
)


# ---------------------------------------------------------
# 17.4 ELIMINREA DUPLICATELOR
# 17.4 ELIMINAZIONE DUPLICATI
# ---------------------------------------------------------

print(
    "Match AD prima dei duplicati:",
    len(match_df)
)

for col in ["Name", "Principal Name", "Banche"]:

    match_df[col] = (
        match_df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )


match_df = (
    match_df
    .drop_duplicates(
        subset=[
            "Name",
            "Principal Name",
            "Banche"
        ]
    )
    .reset_index(drop=True)
)


print(
    "Match AD dopo i duplicati:",
    len(match_df)
)

print(
    "Match tramite SamAccountName:",
    match_sam_count
)

print(
    "Match tramite Name / CN_00:",
    match_name_count
)


# ------------------------

# ===============================--===============================
#  18. CREARE EXCEL FISIER
#  18. CREAZIONE EXCEL FILE
# =========================================================

excel_file = os.path.join(
    output_path,
    "Office_STANDARD_Gruppi_AD_RESULTS_ATTIVI "
    "E UNIQUE NAMES e Match AD.xlsx"
)

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    clean_results.to_excel(
        writer,
        sheet_name="Dettaglio",
        index=False
    )

    clean_results_name.to_excel(
        writer,
        sheet_name="Unique Names",
        index=False
    )

    clean_results_sam.to_excel(
        writer,
        sheet_name="Unique SAM",
        index=False
    )

    clean_results_with_banche.to_excel(
        writer,
        sheet_name="Names Banche",
        index=False
    )

    match_df.to_excel(
        writer,
        sheet_name="Match AD",
        index=False
    )


# =========================================================----====
# 19. REZUMATUL EXECUTIEI
# 19. RIEPILOGO ESECUZIONE
# =========================================================

print("\n========== RISULTATO ELABORAZIONE ==========")

print(f"Gruppi STD finali: {len(groups)}")
print(f"Record Dettaglio: {len(clean_results)}")
print(f"Nomi unici: {len(clean_results_name)}")
print(f"SAM unici: {len(clean_results_sam)}")
print(f"Record Names Banche: {len(clean_results_with_banche)}")
print(f"Match AD: {len(match_df)}")

print(f"\nExcel generato: {excel_file}")
