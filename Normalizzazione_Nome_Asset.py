import os
import re
from Common import pr, start_path

def processa_nome_file(nome_file):
    # Cattura: 11_06_2025, 11_21_15 AM  (con o senza virgola, con U+202F)
    pattern = r'(\d{2})_(\d{2})_(\d{4})[\s\u202F]*,?[\s\u202F]*(\d{1,2})_(\d{2})_(\d{2})[\s\u202F]*([AP]M)'
    match = re.search(pattern, nome_file, re.IGNORECASE)
    
    if not match:
        return None

    mm, dd, yyyy, hh, mi, ss, ampm = match.groups()
    hh = int(hh)

    # Conversione da formato 12h → 24h
    if ampm:
        ampm = ampm.upper()
        if ampm == 'PM' and hh != 12:
            hh += 12
        if ampm == 'AM' and hh == 12:
            hh = 0

    ora_24h = f"{hh:02d}_{mi}_{ss}"
    data_iso = f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"

    # Sostituisce con formato ISO 24h
    nuovo_nome = re.sub(pattern, f"{data_iso} {ora_24h}", nome_file, flags=re.IGNORECASE)
    return nuovo_nome
    #return nuovo_nome + ".csv"


def rename_files_in_directory():
    renamed = 0
    print(f"\nRICERCA IN: {start_path}")
    print(f"CERCO FILE CON: 'Asset' e '.csv'\n")

    if not os.path.exists(start_path):
        print("ERRORE: La directory non esiste!")
        return

    for file in os.listdir(start_path):
        full_path = os.path.join(start_path, file)
        if not os.path.isfile(full_path):
            continue

        if not file.lower().endswith(".csv"):
            continue
        if "asset" not in file.lower():
            continue

        print(f"PROCESSO: {file}")
        nuovo_nome = processa_nome_file(file)

        if nuovo_nome is None:
            print("  → GIÀ IN FORMATO ISO 24h")
            continue

        dst = os.path.join(start_path, nuovo_nome)
        try:
            os.rename(full_path, dst)
            print(f"  RINOMINATO → {nuovo_nome}\n")
            renamed += 1
        except FileExistsError:
            print(f"  ESISTE GIÀ: {nuovo_nome}")
        except Exception as e:
            print(f"  ERRORE: {e}")

    print(f"\n{renamed} file rinominati nel formato ISO 24h!")


if __name__ == "__main__":
    rename_files_in_directory()
