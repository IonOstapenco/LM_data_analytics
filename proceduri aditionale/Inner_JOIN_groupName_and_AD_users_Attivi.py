#
# C:\License_Management\Report_202605\output-1
import csv
import os
import json

print("Procedura per incrocio utenti AD con gruppi PRO.")

# ==========================================================
# Citire Parametri.json
# ==========================================================

with open("Parametri.json", "r", encoding="utf-8") as f:
    pr = json.load(f)

# ==========================================================
# Construire path-uri
# ==========================================================

base_path = pr["Source_dir"]
report_dir = pr["Report_dir"]

input_ad = os.path.join(
    base_path,
    report_dir,
    "output-1",
    pr["AD_Users_Results_attivi"]
)

input_gruppi = os.path.join(
    base_path,
    report_dir,
    "all_in_one",
    "all-in-one_Gruppi_solo_PRD_EXCEPTIE _ctx_047_tta_ads_Unique Names.csv"
)

output_dir = os.path.join(
    base_path,
    report_dir,
    "incrocio"
)

# primul fisier csv
output_file = os.path.join(
    output_dir,
    "incrocio_results.csv"
)

#al doilea fisier csv
output_file_full = os.path.join(
    output_dir,
    "incrocio_results_FULL.csv"
)



# ==============================================---================
# Creare directory output daca nu exista
# ==========================================================

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ==========================================================
# Citire AD_Users_Results_attivi.csv
# Key = Name
# Value = OU_01 (Banche)
# ==========================================================

ad_users = {}

print("\nCaricamento file AD utenti...")
print(input_ad)

with open(input_ad, "r", encoding="utf-8-sig") as f:

    # eliminare prima linie "sep=|"
    first_line = f.readline()

    reader = csv.DictReader(f, delimiter="|")

    for row in reader:

        name = row.get("Name", "").strip().lower()
        #banche = row.get("OU_01", "").strip()

        if not name:
            continue

        # evitare duplicate
        if name not in ad_users:
            #ad_users[name] = banche
            ad_users[name] = row

print(f"Utenti AD caricati: {len(ad_users)}")

# ============================================================
# Citire grupe_name_samAccountName_FARA_DUPLICATE_PRO.csv
# ==========================================================

group_names = set()

print("\nCaricamento file gruppi...")
print(input_gruppi)

with open(input_gruppi, "r", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f, delimiter=";")

    for row in reader:

        name = row.get("Name", "").strip().lower()

        if not name:
            continue

        group_names.add(name)

print(f"Nomi gruppi caricati: {len(group_names)}")

# ==========================================================
# INNER JOIN
# ==========================================================

print("\nEsecuzione INNER JOIN...")

results = []
results_full = []

for name in sorted(group_names):

    if name in ad_users:

        ad_row = ad_users[name]

        banche = ad_row.get("OU_01", "").strip()

        # ======================================
        # OUTPUT SEMPLICE
        # ======================================

        results.append({
            "UsersAttivi": name,
            "Banche": banche
        })

        # ======================================
        # OUTPUT COMPLETO
        # ======================================

        full_row = ad_row.copy()

        full_row["InnerJoinName"] = name
        full_row["Banche"] = banche

        results_full.append(full_row)

print(f"Record trovati: {len(results)}")



# ========================================
#     DEBUG ==============================
#=======
print("\n=== GROUP NAMES ===")
for x in list(group_names)[:20]:
    print(repr(x))

print("\n=== AD NAMES ===")
for x in list(ad_users.keys())[:20]:
    print(repr(x))

# ==========================================================
# Scrittura output CSV
# ==========================================================

print("\nScrittura file output...")
print(output_file)

with open(output_file, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=["UsersAttivi", "Banche"],
        delimiter=";"
    )

    writer.writeheader()

    for row in results:
        writer.writerow(row)

print("\nProcedura completata con successo.")

# ==========================================================
# Scrittura output FULL CSV
# ==========================================================

print("\nScrittura file output FULL...")
print(output_file_full)

if results_full:

    fieldnames_full = list(results_full[0].keys())

    with open(output_file_full, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames_full,
            delimiter=";"
        )

        writer.writeheader()

        for row in results_full:
            writer.writerow(row)