import os
import csv
import json
import pandas as pd
from openpyxl import Workbook

# Citim parametri.json
with open("parametri.json", encoding="utf-8") as f:
    config = json.load(f)

SOURCE_DIR   = config["Source_dir"]
REPORT_DIR   = config["Report_dir"]
AD_SUBFOLDER = r"Active Directory Results - SERVIZICED - 2.12.2025-151753\ServiziCed.local"  # momentan hardcodat aici, hz cum sa pun in parametri.json

root_folder = os.path.join(SOURCE_DIR, REPORT_DIR, AD_SUBFOLDER)

output_file = os.path.join(SOURCE_DIR, REPORT_DIR, "usersAndGroupsResultFinale.csv")
output_file_xlsx = os.path.join(SOURCE_DIR, REPORT_DIR, "usersAndGroupsResultFinale.xlsx")

input_cn_file = os.path.join(SOURCE_DIR, REPORT_DIR, "output-4", config["AD_Users_Results_attivi"])

keywords_exclude = ["CR", "AX", "FI", "FJ"]  # 

# ... restul codului cum am scris inainte




# ---------------------
# citim fisiere AD-usersAndGroupsResult.csv
users = set()  # (UserName, SamAccountName)

for root, dirs, files in os.walk(root_folder):
    for file in files:
        if file == "AD-usersAndGroupsResult.csv":
            file_path = os.path.join(root, file)
            try:
                with open(file_path, newline="", encoding="utf-16") as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=";")

                    if "UserName" not in reader.fieldnames or "SamAccountName" not in reader.fieldnames:
                        print(f"[atenzione!] Coloana UserName lipseste in {file_path}")
                        continue

                    for row in reader:
                        username = row["UserName"].strip()
                        sam = row["SamAccountName"].strip()

                        #adaugam excpludere
                        if sam and any(sam.upper().startswith(prefix) for prefix in keywords_exclude):
                            continue # sarim, adica nu luam in consideratie

                        if username or sam:
                            users.add((username, sam))
            except Exception as e:
                print(f"[ERROR] {file_path} -> {e}")

# ---------------------
# scriem CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["UserName", "SamAccountName"])
    for username, sam in sorted(users):
        writer.writerow([username, sam])

print(f"Fisier CSV generat: {output_file}")
print(f"Total UserName unicale: {len(users)}")

# ---------------------
# scriem Excel
wb = Workbook()

# sheet principal
ws_main = wb.active
ws_main.title = "AD-usersAndGroupsResultFinale"
ws_main.append(["UserName", "SamAccountName"])
for username, sam in sorted(users):
    ws_main.append([username, sam])

# autosize la coloane
for col in ws_main.columns:
    max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
    ws_main.column_dimensions[col[0].column_letter].width = max_length + 2

# ---------------------
# sheet Results cu coloanele CN_00, UserName si InnerJoin
ws_results = wb.create_sheet(title="Results")
# header
ws_results.append(["CN_00", "UserName", "InnerJoin"])

# ---------------------
# citim CN_00
cn_list = []
try:
    cn_df = pd.read_csv(
        input_cn_file,
        sep="|",
        encoding="utf-8",
        skiprows=1,
        dtype=str
    ).fillna("")

    if "CN_00" not in cn_df.columns:
        print("[ERROR] Coloana CN_00 nu exista in fisierul sursa!")
        cn_df = pd.DataFrame(columns=["CN_00"])
    else:
        cn_list = [cn.strip() for cn in cn_df["CN_00"] if cn.strip()]
        cn_df = pd.DataFrame({"CN_00": cn_list})

except Exception as e:
    print(f"[ERROR] Citire CN_00 -> {e}")
    cn_df = pd.DataFrame(columns=["CN_00"])

# luam doar UserName din setul users
username_list = [username.strip() for username, _ in sorted(users) if username.strip()]
users_df = pd.DataFrame({"UserName": username_list})



#adaugam pentru normalizare -- ducem la litere minuscule
cn_df["CN_00_norm"] = cn_df["CN_00"].str.strip().str.lower()
users_df["UserName_norm"] = users_df["UserName"].str.strip().str.lower()




# ---------------------!!! AICI TAMAN INNER JOIN !! ------------
# facem inner join intre CN_00 si UserName --- am copiat de la proiectul trevut
#varianta veche
#merged_df = pd.merge(cn_df, users_df, left_on="CN_00", right_on="UserName", how="inner")

#varianta noua -- din cauza case senzitive
merged_df = pd.merge(cn_df, users_df, left_on="CN_00_norm", right_on="UserName_norm", how="inner")

#adaugam counter
innerjoin_count = len(merged_df)

#taman aici aratam cate sunt in inner_join
print(f"Numar recorduri INNER JOIN: {innerjoin_count}")
# ---------------------
# completam randuri pentu Excel
max_len = max(len(cn_list), len(username_list))
for i in range(max_len):
    cn_val = cn_list[i] if i < len(cn_list) else ""
    username_val = username_list[i] if i < len(username_list) else ""
    # verific dac CN_00 esste în merged_df -> scrim în InnerJoin
    inner_val = cn_val if cn_val in merged_df["CN_00"].values else ""
    # verific dac CN_00 esste în merged_df -> scrim în InnerJoin
    #varianta noua cu normalizare --> CN_00_norm
    inner_val = cn_val if cn_val.lower() in merged_df["CN_00_norm"].values else ""

    ws_results.append([cn_val, username_val, inner_val])



# autosize la coloane Results
for col in ws_results.columns:
    max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
    ws_results.column_dimensions[col[0].column_letter].width = max_length + 2

# ---------------------
# salvare Excel
wb.save(output_file_xlsx)
print(f"Fisier Excel generat: {output_file_xlsx}")

