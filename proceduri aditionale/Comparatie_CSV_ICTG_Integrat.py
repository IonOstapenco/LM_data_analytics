# compare_ictg_from_params.py
import os
import json
from pathlib import Path
import pandas as pd

# ================== CONFIGURAZIONE & PERCORSI ==================

def incarca_parametri(path_parametri: Path) -> dict:
    with open(path_parametri, "r", encoding="utf-8") as f:
        return json.load(f)

def asigura_folder(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def ext_din_parametri(cfg: dict) -> str:
    ext = cfg.get("Extension_end", "csv")
    return ext if ext.startswith(".") else f".{ext}"

def gaseste_ultimul_fisier(folder: Path, pattern: str, ext: str) -> Path | None:
    """
    Trova il file più "recente" in base al nome (ordinamento lessicografico)
    nella cartella `folder` che contiene `pattern` e termina con `ext`.
    """
    if not folder.is_dir():
        return None
    candidati = [
        p for p in folder.iterdir()
        if p.is_file() and pattern in p.name and p.name.lower().endswith(ext.lower())
    ]
    if not candidati:
        return None
    candidati.sort(key=lambda p: p.name)  # con timestamp nel nome, l'ultimo è il più recente
    return candidati[-1]

# ================== FUNZIONI ESISTENTI (leggermente adattate) ==================

def load_csv_auto(path: Path) -> pd.DataFrame:
    """
    Legge un CSV sia nel caso in cui la prima riga sia 'sep=,'
    sia nel caso in cui contenga direttamente l'header.
    """
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline().lower()

    sep = ','
    skip = 0
    if first_line.startswith('sep='):
        sep = first_line.strip().split('=')[1]
        skip = 1

    try:
        return pd.read_csv(path, sep=sep, skiprows=skip, encoding='utf-8')
    except Exception:
        return pd.read_csv(path, sep=sep, skiprows=skip, encoding='latin1', on_bad_lines='skip')

def comparare_csv(firstFile_path: Path, secondFile_path: Path):
    try:
        if not firstFile_path.exists():
            print(f"Errore: il file1 {firstFile_path} non esiste")
            return
        if not secondFile_path.exists():
            print(f"Errore: il file2 {secondFile_path} non esiste")
            return

        dfPrimul = load_csv_auto(firstFile_path)
        dfAldoilea = load_csv_auto(secondFile_path)

        numeleFisier1 = firstFile_path.name
        numeleFisier2 = secondFile_path.name

        print(f"\nHeader file1 {numeleFisier1}:")
        print(list(dfPrimul.columns))

        print(f"\nHeader file2 {numeleFisier2}:")
        print(list(dfAldoilea.columns))

        print("\nNumero di colonne:", len(dfPrimul.columns), "vs", len(dfAldoilea.columns))

        set1 = set(dfPrimul.columns)
        set2 = set(dfAldoilea.columns)

        print("\nColonne presenti solo nel file2 (<<):", list(set2 - set1))
        print("Colonne presenti solo nel file1 (>>):", list(set1 - set2))

        print("\nConfronto numero righe:")
        print(f"{numeleFisier1}: {dfPrimul.shape}")
        print(f"{numeleFisier2}: {dfAldoilea.shape}")

        print("\n================ VISUALIZZAZIONE ALLINEATA =================")

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
        print(f"Errore imprevisto: {e}")

def generate_raport_diferente(f1: Path, f2: Path, nume_report: Path, titlu: str = ""):
    if not f1.exists() or not f2.exists():
        print("Errore: uno dei file non esiste!")
        return

    df1 = load_csv_auto(f1)
    df2 = load_csv_auto(f2)

    col1 = list(df1.columns)
    col2 = list(df2.columns)

    set1 = set(col1)
    set2 = set(col2)

    nume_f1 = f1.name
    nume_f2 = f2.name

    with open(nume_report, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 120 + "\n")
        if titlu:
            f.write(titlu + "\n")

        f.write(f"{'File precedente / vecchio':<60}{'File attuale / nuovo':<60}\n")
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

def compara_toate_fisierele(fisiere: list[Path], raport: Path = Path("raport_diferente.txt")):
    # reset del report
    raport.write_text("", encoding="utf-8")
    if len(fisiere) % 2 != 0:
        print("La lista deve contenere coppie di file")
        return

    for i in range(0, len(fisiere), 2):
        generate_raport_diferente(
            fisiere[i],
            fisiere[i + 1],
            raport,
            titlu=""
        )

    print("Report generato:", raport)

# ================== OPZIONALE: DIFFERENZE DI RIGHE (colonne comuni) ==================
def scrie_diferente_randuri(f_vechi: Path, f_nou: Path, out_dir: Path, prefix: str):
    """
    Senza chiave esplicita — confronta l'insieme delle righe sulle colonne comuni (case-sensitive).
    Crea due file opzionali:
      - *_rows_added.csv
      - *_rows_removed.csv
    """
    df_old = load_csv_auto(f_vechi)
    df_new = load_csv_auto(f_nou)

    common = [c for c in df_old.columns if c in df_new.columns]
    if not common:
        print(f"[INFO] Nessuna colonna comune per {f_vechi.name} vs {f_nou.name} — confronto righe saltato.")
        return

    A = df_old[common].fillna("").astype(str)
    B = df_new[common].fillna("").astype(str)

    # conversione di ogni riga in una tupla per il set-diff
    setA = set(tuple(row) for row in A.to_numpy().tolist())
    setB = set(tuple(row) for row in B.to_numpy().tolist())

    added = list(setB - setA)
    removed = list(setA - setB)

    if added:
        pd.DataFrame(added, columns=common).to_csv(
            out_dir / f"{prefix}_rows_added.csv",
            index=False,
            encoding="utf-8"
        )
        print(f"[ROW-DIFF] Righe aggiunte: {len(added)} → {out_dir / (prefix + '_rows_added.csv')}")
    else:
        print(f"[ROW-DIFF] Nessuna riga aggiunta per {prefix}")

    if removed:
        pd.DataFrame(removed, columns=common).to_csv(
            out_dir / f"{prefix}_rows_removed.csv",
            index=False,
            encoding="utf-8"
        )
        print(f"[ROW-DIFF] Righe rimosse: {len(removed)} → {out_dir / (prefix + '_rows_removed.csv')}")
    else:
        print(f"[ROW-DIFF] Nessuna riga rimossa per {prefix}")

# ================== INTEGRAZIONE CON Parametri.json ==================

def pregateste_perechi_din_parametri(cfg: dict) -> tuple[list[tuple[Path, Path, str]], Path]:
    """
    Crea coppie (vecchio, nuovo, titolo) per:
     - Classificazione software
     - Database Oracle
     - Inventario hardware
    Utilizzando Source_dir + Former_dir / Report_dir + Output_dir.
    """
    SOURCE_DIR = Path(cfg["Source_dir"])
    REPORT_DIR = cfg["Report_dir"]
    FORMER_DIR = cfg["Former_dir"]

    # Allineato allo stile del progetto: output nel mese corrente
    OUTPUT_PATH = asigura_folder(SOURCE_DIR / REPORT_DIR / cfg["Output_dir"])

    current_root = SOURCE_DIR / REPORT_DIR
    former_root = SOURCE_DIR / FORMER_DIR
    ext = ext_din_parametri(cfg)

    mapping = [
        ("BFGX_SW_Pattern",         "=== Classificazione software ===", "clasificazione_software"),
        ("Oracle_Database_Pattern", "=== Database Oracle ===",          "database_oracle"),
        ("BGFX_Pattern",            "=== Inventario hardware ===",      "inventario_hardware"),
    ]

    perechi: list[tuple[Path, Path, str]] = []
    for key, titlu, _slug in mapping:
        pattern = cfg.get(key, "")
        if not pattern:
            print(f"[AVVISO] Chiave mancante nel config: {key}")
            continue

        f_vechi = gaseste_ultimul_fisier(former_root, pattern, ext)
        f_nou = gaseste_ultimul_fisier(current_root, pattern, ext)

        if not f_vechi:
            print(f"[ERRORE] File vecchio non trovato per pattern='{pattern}' in {former_root}")
        if not f_nou:
            print(f"[ERRORE] File nuovo non trovato per pattern='{pattern}' in {current_root}")

        if f_vechi and f_nou:
            perechi.append((f_vechi, f_nou, titlu))
            print(f"[OK] {titlu}\n    Vecchio: {f_vechi}\n    Nuovo : {f_nou}")

    raport_name = f"raport_diferente_{cfg['Former_dir']}_vs_{cfg['Report_dir']}.txt"
    raport_path = OUTPUT_PATH / raport_name

    return perechi, raport_path

def main(path_parametri: Path = Path("Parametri.json"), scrie_rowdiff: bool = False):
    cfg = incarca_parametri(path_parametri)
    perechi, raport_path = pregateste_perechi_din_parametri(cfg)

    # confronto in console (header & informazioni)
    for (f_vechi, f_nou, titlu) in perechi:
        print("\n" + titlu)
        comparare_csv(f_vechi, f_nou)

    # report consolidato
    fisiere: list[Path] = []
    for (f_vechi, f_nou, _titlu) in perechi:
        fisiere.extend([f_vechi, f_nou])

    if fisiere:
        compara_toate_fisierele(fisiere, raport=raport_path)
    else:
        print("Non esistono coppie valide per la generazione del report.")

    # opzionale: differenze di righe sulle colonne comuni (salvate in OUTPUT_PATH)
    if scrie_rowdiff:
        SOURCE_DIR = Path(cfg["Source_dir"])
        OUTPUT_PATH = asigura_folder(SOURCE_DIR / cfg["Report_dir"] / cfg["Output_dir"])
        for (f_vechi, f_nou, titlu) in perechi:
            # prefisso pulito per i file CSV di diff
            prefix = f"{f_vechi.stem}__vs__{f_nou.stem}"
            scrie_diferente_randuri(f_vechi, f_nou, OUTPUT_PATH, prefix)

if __name__ == "__main__":
    # modifica se Parametri.json si trova altrove:
    # main(Path(r"C:\License_Management\Parametri.json"), scrie_rowdiff=True)
    main()
