import pandas as pd
import os
import re
import Common as cm
import tempfile

def read_csv_safely(path):
    """
    Legge il CSV di ServiceNow (anche con 'sep=,' nella prima riga + qualsiasi encoding)
    """
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc, newline='', errors='ignore') as f:
                lines = f.readlines()

            # Rimuove la riga 'sep=,' se presente
            if lines and lines[0].strip().lower().startswith('sep='):
                lines = lines[1:]

            # Lettura dalla memoria
            from io import StringIO
            df = pd.read_csv(StringIO(''.join(lines)), sep=',', encoding=enc, low_memory=False)

            if len(df.columns) > 10:  # deve avere almeno 30-40 colonne reali
                print(f"Asset Server letto correttamente (encoding: {enc})")
                return df.fillna("")
        except:
            continue

    # Ultima soluzione (garantita)
    print("Fallback: lettura forzata con skiprows=1 e latin1")
    return pd.read_csv(path, sep=',', encoding='latin1', skiprows=1, on_bad_lines='skip', low_memory=False).fillna("")

def inner_join_cmdb_assetserver_columns():
    cm.check_outdir(cm.out_path)

    # ==================== 1. Lista_CMDB.xlsx ====================
    cm.files = []
    cm.list_files_scandir(cm.start_path, "Lista_CMDB", cm.pr["XLS_end"])
    lista_cmdb_files = sorted(cm.files, reverse=True)
    if not lista_cmdb_files:
        raise FileNotFoundError("Non ho trovato il file Lista_CMDB.xlsx")
    lista_cmdb_file = lista_cmdb_files[0]
    print(f"Lettura Lista_CMDB: {lista_cmdb_file}")

    cmdb_df = pd.read_excel(lista_cmdb_file, dtype=str).fillna("")
    prima_col = cmdb_df.columns[0]
    cmdb_df["CMDB_App"] = cmdb_df[prima_col].astype(str).str.strip().str.lower()
    cmdb_unique = cmdb_df[["CMDB_App"]].drop_duplicates().reset_index(drop=True)

    # ==================== 2. Asset Server ====================
    cm.files = []
    cm.list_files_scandir(cm.start_path, cm.pr["CMDB_Pattern"], cm.pr["Extension_end"])
    asset_server_files = sorted(cm.files, reverse=True)
    if not asset_server_files:
        raise FileNotFoundError("Non ho trovato il file Asset Server")
    asset_server_file = asset_server_files[0]
    print(f"Lettura Asset Server: {asset_server_file}")

    asset_srv_df = read_csv_safely(asset_server_file)
    print(f"Numero colonne rilevate: {len(asset_srv_df.columns)}")
    print(f"Prime 5 colonne: {list(asset_srv_df.columns[:5])}")

    # Troviamo la colonna delle applicazioni (può avere nomi diversi)
    applicazioni_col = None
    for col in asset_srv_df.columns:
        if "pplicazioni" in col.lower() and "(" in col and ")" in col:
            applicazioni_col = col
            break
    if applicazioni_col is None:
        print("Colonne disponibili:")
        for i, col in enumerate(asset_srv_df.columns):
            print(f"  [{i}] {col}")
        raise KeyError("ERRORE: Non ho trovato la colonna 'Applicazioni (lista)'!")

    print(f"Colonna delle applicazioni rilevata: '{applicazioni_col}'")

    # Costruiamo la mappatura: applicazione → lista di Nome_CI
    mapping_list = []
    for idx, row in asset_srv_df.iterrows():
        nome_ci = str(row["Nome CI"]).strip()
        apps_str = str(row[applicazioni_col])
        if pd.isna(apps_str) or apps_str == "nan" or apps_str == "":
            continue
        apps = [app.strip().lower() for app in apps_str.split(";") if app.strip()]
        for app in apps:
            if app:
                mapping_list.append({"Nome_CI": nome_ci, "Applicazione": app})

    mapping_df = pd.DataFrame(mapping_list)

    if mapping_df.empty:
        print("Non sono state trovate applicazioni nella colonna Applicazioni (lista)")
        asset_unique = pd.DataFrame({"Applicazione": []})
        inner_join_map = {}
    else:
        asset_unique = pd.DataFrame({"Applicazione": mapping_df["Applicazione"].unique()})
        inner_join_map = mapping_df.groupby("Applicazione")["Nome_CI"].apply(
            lambda x: ", ".join(sorted(set(x)))
        ).to_dict()

    # ==================== 3. Inner Join CMDB ↔ Asset Server ====================
    merged_values = pd.merge(
        cmdb_unique.rename(columns={"CMDB_App": "key"}),
        asset_unique.rename(columns={"Applicazione": "key"}),
        on="key",
        how="inner"
    )[["key"]].drop_duplicates()

    merged_values["Nome_CI"] = merged_values["key"].map(inner_join_map).fillna("")

    # ==================== 4. Asset Software → Oracle Database ====================
    cm.files = []
    cm.list_files_scandir(cm.start_path, cm.pr["CMDB_SW_Pattern"], cm.pr["Extension_end"])
    asset_software_files = sorted(cm.files, reverse=True)
    if not asset_software_files:
        raise FileNotFoundError("Non ho trovato il file Asset Software")
    asset_software_file = asset_software_files[0]
    print(f"Lettura Asset Software: {asset_software_file}")

    asset_sw_df = read_csv_safely(asset_software_file)
    asset_sw_df["server"] = asset_sw_df.iloc[:, 0].astype(str).str.strip()
    asset_sw_df["software"] = asset_sw_df.iloc[:, 4].astype(str).str.strip()

    all_servers = set(asset_sw_df["server"].dropna())
    software_per_server = asset_sw_df.groupby("server")["software"].apply(
        lambda x: ", ".join(pd.Series(x.unique()))
    ).to_dict()

    # Sheet 2: Server Software Mapping
    if not merged_values.empty and "Nome_CI" in merged_values.columns:
        sheet2 = merged_values[["Nome_CI"]].copy()
        sheet2["Nome_CI"] = sheet2["Nome_CI"].str.split(", ")
        sheet2 = sheet2.explode("Nome_CI").reset_index(drop=True)
        sheet2 = sheet2[sheet2["Nome_CI"].str.strip() != ""].copy()
    else:
        sheet2 = pd.DataFrame({"Nome_CI": []})

    sheet2["Inner_Join_Nome_CI_server"] = sheet2["Nome_CI"].apply(
        lambda x: x if x in all_servers else ""
    )

    def has_oracle(server):
        if not server:
            return "NO"
        sw = software_per_server.get(server, "")
        return "SI" if re.search(r'oracle\s+database', sw, re.IGNORECASE) else "NO"

    sheet2["Oracle_Database"] = sheet2["Inner_Join_Nome_CI_server"].apply(has_oracle)

    # Aggiungiamo tutti i server da Asset Software
    servers_list = pd.DataFrame({"server": list(all_servers)})
    max_rows = max(len(sheet2), len(servers_list))
    sheet2 = sheet2.reindex(range(max_rows)).fillna("")
    servers_list = servers_list.reindex(range(max_rows)).fillna("")
    sheet2["server"] = servers_list["server"].values

    sheet2 = sheet2[["Nome_CI", "server", "Inner_Join_Nome_CI_server", "Oracle_Database"]]

    # ==================== 5. Sheet principale ====================
    max_len = max(len(cmdb_unique), len(asset_unique) if 'asset_unique' in locals() else 0, len(merged_values))
    df_final = pd.DataFrame({
        "CMDB": cmdb_unique["CMDB_App"].reindex(range(max_len)).fillna(""),
        "Applicazione": (asset_unique["Applicazione"] if not asset_unique.empty else pd.Series()).reindex(range(max_len)).fillna(""),
        "Inner Join": merged_values["key"].reindex(range(max_len)).fillna(""),
        "Nome CI": merged_values["Nome_CI"].reindex(range(max_len)).fillna("")
    })

    # ==================== 6. Scrittura Excel ====================
    output_file = os.path.join(cm.out_path, "InnerJoinCMDBandAssetServer.xlsx")
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df_final.to_excel(writer, index=False, sheet_name="Inner Join CMDB vs Asset Server")
        sheet2.to_excel(writer, index=False, sheet_name="Server Software Mapping")

        ws1 = writer.sheets["Inner Join CMDB vs Asset Server"]
        ws1.set_column("A:A", 40)
        ws1.set_column("B:B", 40)
        ws1.set_column("C:C", 40)
        ws1.set_column("D:D", 80)

        ws2 = writer.sheets["Server Software Mapping"]
        for i in range(4):
            ws2.set_column(i, i, 25)

    print("FATTO! File generato:")
    print(f"   → {output_file}")
    print(f"   → Inner Join trovati: {len(merged_values)} applicazioni comuni")
    print(f"   → Server con Oracle rilevati: {sheet2['Oracle_Database'].eq('SI').sum()}")

if __name__ == "__main__":
    inner_join_cmdb_assetserver_columns()
