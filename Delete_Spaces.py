import csv
import json
import os


# === Lettura del file parametri.json ===
with open("parametri.json", "r", encoding="utf-8") as f:
    params = json.load(f)

# === Estrazione della directory sorgente ===
source_dir = params.get("Source_dir", "")
report_dir = params.get("Report_dir", "")
full_dir = os.path.join(source_dir, report_dir)

# === Raccogliamo tutti i file CSV presenti nella directory ===
input_paths = []
for file in os.listdir(full_dir):
    if file.endswith(".csv"):
        input_paths.append(os.path.join(full_dir, file))

# === Funzione per eliminare gli spazi ===
def deleteSpaces(input_path):
    print(f"🔹 Avvio della procedura di pulizia per: {os.path.basename(input_path)}")
    rows = []
    with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',', skipinitialspace=True)
        for row in reader:
            # Saltiamo le righe completamente vuote
            if not row or all(cell.strip() == "" for cell in row):
                continue
            # Rimuoviamo gli spazi da ogni cella
            clean_row = [cell.strip() for cell in row]
            rows.append(clean_row)

    # Sovrascriviamo il file con il contenuto ripulito
    with open(input_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)

    print(f"✅ File ripulito: {os.path.basename(input_path)}")

# === Eseguiamo la procedura per tutti i file trovati ===
if not input_paths:
    print("⚠️ Nessun file CSV trovato nella directory specificata.")
else:
    for path in input_paths:
        deleteSpaces(path)

print("\n🏁 Procedura di pulizia completata.")
