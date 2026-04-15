import pandas as pd 
import os
import re
import Common as cm
import csv

def read_csv_safely(path):
    """Legge il CSV con codifica di fallback e skiprows=1 per Asset Server"""
    try:
        df = pd.read_csv(path, sep=",", encoding="utf-8", skiprows=1)
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep=",", encoding="latin1", skiprows=1)
    return df

def inner_join_cmdb_assetserver_columns():
    # -------------------- 1️⃣ Garantiamo la directory di output --------------------
    cm.check_outdir(cm.out_path)
    
    # -------------------- 2️⃣ Leggiamo Lista_CMDB.xlsx --------------------
    cm.files = []
    cm.list_files_scandir(cm.start_path, "Lista_CMDB", cm.pr["XLS_end"])
    lista_cmdb_files = sorted(cm.files, reverse=True)
    if not lista_cmdb_files:
        raise FileNotFoundError("❌ Non è stato trovato il file Lista_CMDB.xlsx in start_path")
    lista_cmdb_file = lista_cmdb_files[0]
    print(f"📂 Lettura Lista_CMDB: {lista_cmdb_file}")
    cmdb_df = pd.read_excel(lista_cmdb_file, dtype=str).fillna("")
    prima_col = cmdb_df.columns[0]
    cmdb_df["CMDB_App"] = cmdb_df[prima_col].astype(str).str.strip().str.lower()
    cmdb_unique = cmdb_df[["CMDB_App"]].drop_duplicates().reset_index(drop=True)
    
    # -------------------- 3️⃣ Leggiamo Asset Server --------------------
    cm.files = []
    cm.list_files_scandir(cm.start_path, cm.pr["CMDB_Pattern"], cm.pr["Extension_end"])
    asset_server_files = sorted(cm.files, reverse=True)
    if not asset_server_files:
        raise FileNotFoundError("❌ Non è stato trovato il file Asset Server in start_path")
    asset_server_file = asset_server_files[0]
    print(f"📂 Lettura Asset Server: {asset_server_file}")
    asset_srv_df = read_csv_safely(asset_server_file).fillna("")
    if len(asset_srv_df.columns) < 11:
        raise ValueError("❌ Il file Asset Server non contiene la colonna K (indice 10)")
    # Colonna K = indice 10
    asset_srv_df["Applicazione"] = asset_srv_df.iloc[:, 10].astype(str).str.strip().str.lower()
    asset_srv_df["Nome_CI"] = asset_srv_df.iloc[:, 0].astype(str).str.strip()
    asset_unique = asset_srv_df[["Applicazione"]].drop_duplicates().reset_index(drop=True)
    
    # -------------------- 4️⃣ Inner join per i valori comuni (senza vuoti) --------------------
    merged_values = pd.merge(
        cmdb_unique.rename(columns={"CMDB_App": "CMDB"}),
        asset_unique.rename(columns={"Applicazione": "Applicazione"}),
        left_on="CMDB",
        right_on="Applicazione",
        how="inner"
    )[["CMDB"]]  # manteniamo solo il valore comune
    # Escludiamo le voci vuote nella colonna C
    merged_values["CMDB"] = merged_values["CMDB"].astype(str).str.strip().str.lower()
    merged_values = merged_values[merged_values["CMDB"] != ""].reset_index(drop=True)
    
    # -------------------- 5️⃣ Mappatura Inner Join → Nome CI (per la colonna D) --------------------
    inner_join_map = (
        asset_srv_df.groupby("Applicazione")["Nome_CI"]
        .apply(lambda x: ", ".join(pd.Series(x.unique()).astype(str)))
        .to_dict()
    )
    merged_values["Nome_CI"] = merged_values["CMDB"].map(inner_join_map).fillna("")
    
    # -------------------- 6️⃣ Leggiamo Asset Software per il nuovo foglio --------------------
    cm.files = []
    cm.list_files_scandir(cm.start_path, cm.pr["CMDB_SW_Pattern"], cm.pr["Extension_end"])
    asset_software_files = sorted(cm.files, reverse=True)
    if not asset_software_files:
        raise FileNotFoundError("❌ Non è stato trovato il file Asset Software in start_path")
    asset_software_file = asset_software_files[0]
    print(f"📂 Lettura Asset Software: {asset_software_file}")
    asset_sw_df = read_csv_safely(asset_software_file).fillna("")
    asset_sw_df["server"] = asset_sw_df.iloc[:, 0].astype(str).str.strip()  # Colonna server (indice 0)
    asset_sw_df["software"] = asset_sw_df.iloc[:, 4].astype(str).str.strip()  # Colonna software (indice 4)
    
    # Log di esempio per debug
    print("Esempi Nome_CI:", merged_values["Nome_CI"].dropna()[:5].tolist())
    print("Esempi server (Asset Software):", asset_sw_df["server"].dropna().unique()[:5].tolist())
    print("Esempi software (Asset Software):", asset_sw_df["software"].dropna().unique()[:5].tolist())
    
    # Creiamo dataframe per il foglio “Server Software Mapping”
    # Colonna A: suddividiamo Nome_CI in singoli server
    server_software_df = merged_values[["Nome_CI"]].copy()
    server_software_df["Nome_CI"] = server_software_df["Nome_CI"].str.split(", ")
    server_software_df = server_software_df.explode("Nome_CI").reset_index(drop=True)
    server_software_df = server_software_df[server_software_df["Nome_CI"] != ""].dropna(subset=["Nome_CI"])
    
    # Colonna B: tutti i server grezzi da Asset Software
    asset_servers = asset_sw_df["server"].dropna().unique()
    asset_df = pd.DataFrame({"server": asset_servers})
    
    # Combiniamo Nome_CI e i server di Asset Software
    max_len = max(len(server_software_df), len(asset_df))
    server_software_df = server_software_df.reindex(range(max_len)).fillna("")
    asset_df = asset_df.reindex(range(max_len)).fillna("")
    server_software_df["server"] = asset_df["server"]
    
    # Colonna C: Inner join tra Nome_CI e tutti i server di Asset Software
    all_asset_servers = set(asset_sw_df["server"].dropna().unique())  # Set di tutti i server
    server_software_df["Inner_Join_Nome_CI_server"] = server_software_df["Nome_CI"].apply(
        lambda x: x if x in all_asset_servers and x != "" else ""
    )
    
    # Colonna D: verifichiamo se il software associato al server nella C contiene “Oracle Database” o “oracle db”
    # Creiamo un dizionario server -> software da Asset Software
    server_software_map = asset_sw_df.groupby("server")["software"].apply(
        lambda x: ", ".join(pd.Series(x.unique()).astype(str))
    ).to_dict()
    
    server_software_df["Oracle_Database"] = server_software_df["Inner_Join_Nome_CI_server"].apply(
        lambda x: "SÌ" if x and any(re.search(r'\b(?:Oracle Database|oracle db)\b', sw, re.IGNORECASE) for sw in server_software_map.get(x, "").split(", ")) else "NO"
    )
    
    print(f"Numero di righe in Server Software Mapping: {len(server_software_df)}")
    print("Esempi Inner_Join_Nome_CI_server:", server_software_df["Inner_Join_Nome_CI_server"].dropna().unique()[:5].tolist())
    print("Esempi Oracle_Database:", server_software_df["Oracle_Database"].dropna().unique()[:5].tolist())
    
    # -------------------- 7️⃣ Creiamo il foglio finale mantenendo A e B INALTERATI --------------------
    A = cmdb_unique["CMDB_App"].reset_index(drop=True)
    B = asset_unique["Applicazione"].reset_index(drop=True)
    C = merged_values["CMDB"].reset_index(drop=True)
    D = merged_values["Nome_CI"].reset_index(drop=True)
    max_len = max(len(A), len(B), len(C), len(D))
    df_final = pd.DataFrame({
        "CMDB": A.reindex(range(max_len)).fillna(""),
        "Applicazione": B.reindex(range(max_len)).fillna(""),
        "Inner Join": C.reindex(range(max_len)).fillna(""),
        "Nome CI": D.reindex(range(max_len)).fillna("")
    })
    
    # -------------------- 8️⃣ Scriviamo nel file Excel --------------------
    output_file = os.path.join(cm.out_path, "InnerJoinCMDBandAssetServer.xlsx")
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df_final.to_excel(writer, index=False, sheet_name="Inner Join CMDB vs Asset Server")
        server_software_df.to_excel(writer, index=False, sheet_name="Server Software Mapping")
        # Impostiamo la larghezza delle colonne per leggibilità
        workbook = writer.book
        worksheet1 = writer.sheets["Inner Join CMDB vs Asset Server"]
        worksheet1.set_column("A:A", 35)
        worksheet1.set_column("B:B", 35)
        worksheet1.set_column("C:C", 35)
        worksheet1.set_column("D:D", 60)
        worksheet2 = writer.sheets["Server Software Mapping"]
        worksheet2.set_column("A:A", 60)
        worksheet2.set_column("B:B", 60)
        worksheet2.set_column("C:C", 60)
        worksheet2.set_column("D:D", 20)
    
    print(f"✅ File generato: {output_file}")
    print(f"- Colonna A (Inner Join): Elenco CMDB (valori unici) = {len(cmdb_unique)}")
    print(f"- Colonna B (Inner Join): Elenco Applicazione (valori unici) = {len(asset_unique)}")
    print(f"- Colonna C (Inner Join): Valori comuni (senza vuoti) = {len(merged_values)}")
    print(f"- Colonna D (Inner Join): Nome CI associati ai valori in C")
    print(f"- Foglio 'Server Software Mapping': {len(server_software_df)} righe (Nome_CI, server, Inner_Join_Nome_CI_server, Oracle_Database)")

# ========================= MAIN =========================
if __name__ == "__main__":
    inner_join_cmdb_assetserver_columns()
