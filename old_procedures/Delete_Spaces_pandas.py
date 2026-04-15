import json
import os
import pandas as pd
import csv

with open("parametri.json", "r", encoding="utf-8") as f:
    params = json.load(f)

source_dir = params.get("Source_dir", "")
report_dir = params.get("Report_dir", "")

full_dir = os.path.join(source_dir, report_dir)

input_paths = [
    os.path.join(full_dir, f)
    for f in os.listdir(full_dir)
    if f.endswith(".csv")
]

def deleteSpaces(file_path):

    print(f"🔹 Curățare: {os.path.basename(file_path)}")

    # citim prima linie
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()

    has_sep = first_line.lower().startswith("sep=")

    # citire CSV
    df = pd.read_csv(
        file_path,
        dtype=str,
        keep_default_na=False,
        skiprows=1 if has_sep else 0,
        engine="python"
    )

    # curățare spații
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    with open(file_path, "w", encoding="utf-8", newline="") as f:

        # scriem sep doar daca exista in original
        if has_sep:
            f.write("sep=,\n")

        df.to_csv(
            f,
            index=False,
            quoting=csv.QUOTE_MINIMAL
        )

    print(f"✅ File ripulito: {os.path.basename(file_path)}")

for path in input_paths:
    deleteSpaces(path)

print("🏁 Procedura completata.")