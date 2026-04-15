import pandas as pd
import os
import Common as cm

def read_csv_safely(path):
    """Citește CSV și găsește header-ul automat"""
    encodings = ["utf-8", "latin1", "cp1252"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as f:
                lines = [line.strip() for line in f.readlines()]
            break
        except:
            continue
    else:
        raise ValueError("Nu s-a putut citi fișierul cu niciun encoding.")

    # Găsim rândul cu header-ul
    header_row = None
    for i, line in enumerate(lines):
        if "Nome CI" in line and "Applicazione" in line:
            header_row = i
            break
    if header_row is None:
        raise ValueError("Nu s-a găsit header-ul cu 'Nome CI' și 'Applicazione'")

    # Citim de la header în jos
    df = pd.read_csv(path, skiprows=header_row, encoding=enc, dtype=str).fillna("")
    return df

def main():
    # ------------------- 1. Căi -------------------
    start_path = os.path.join(cm.pr["Source_dir"], cm.pr["Report_dir"])
    out_path = os.path.join(start_path, cm.pr["Output_dir"])
    cm.check_outdir(out_path)

    # ------------------- 2. Citim Macchine_Integrare.csv -------------------
    input_file = os.path.join(start_path, cm.pr["Input_Macchine"])
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Nu s-a găsit: {input_file}")

    print(f"Citim: {input_file}")
    df_macchine = pd.read_csv(input_file, usecols=[0], header=0, dtype=str).fillna("")
    df_macchine.columns = ["Macchina"]
    df_macchine["Macchina"] = df_macchine["Macchina"].str.strip()
    macchine_list = df_macchine["Macchina"].drop_duplicates().tolist()
    print(f"Servere de procesat: {len(macchine_list)}")

    # ------------------- 3. Căutăm Asset Server în tot folderul -------------------
    asset_file = None
    pattern = cm.pr["CMDB_Pattern"]
    for root, _, files in os.walk(start_path):
        for file in files:
            if file.lower().startswith(pattern.lower()) and file.endswith(cm.pr["Extension_end"]):
                asset_file = os.path.join(root, file)
                break
        if asset_file:
            break

    if not asset_file:
        raise FileNotFoundError(f"Nu s-a găsit fișierul cu '{pattern}' în {start_path}")

    print(f"Citim Asset Server: {asset_file}")
    df_asset = read_csv_safely(asset_file)

    if "Nome CI" not in df_asset.columns or "Applicazione" not in df_asset.columns:
        raise ValueError(f"Coloane lipsă. Găsite: {list(df_asset.columns)}")

    df_asset["Nome_CI"] = df_asset["Nome CI"].astype(str).str.strip()
    df_asset["Applicazione"] = df_asset["Applicazione"].astype(str).str.strip()

    # Mapare: server → aplicații
    app_map = (
        df_asset.groupby("Nome_CI")["Applicazione"]
        .apply(lambda x: ", ".join(sorted([a for a in x.unique() if a and a not in ["", "nan"]])))
        .to_dict()
    )

    # ------------------- 4. Output -------------------
    output_data = []
    for mac in macchine_list:
        app = app_map.get(mac, "-")
        output_data.append([mac, app])

    output_df = pd.DataFrame(output_data, columns=["Macchina", "Applicazione"])

    # ------------------- 5. Scriem -------------------
    output_file = os.path.join(out_path, cm.pr["Output_Macchine"])
    output_df.to_csv(output_file, index=False, sep="|", encoding="utf-8")

    print(f"Fișier generat: {output_file}")
    print(f"   → {len(output_df)} rânduri")
    print("\nPrimele 5:")
    print(output_df.head().to_string(index=False))

if __name__ == "__main__":
    main()