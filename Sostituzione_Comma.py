import os
import glob
from Common import pr, start_path, dr

# --- original functtion ---
def inlocuire_comma(inputFile):
    print("**** loading csv file ****")
    print("replacing comma with semicolon in csv file")

    with open(inputFile, mode='r') as f:
        continut = f.read()

    continutNou = continut.replace(',', ';')

    with open(inputFile, mode='w') as f:
        f.write(continutNou)

    print("*** modificato --,-- con  --;-- nel file csv")


# ==========================================================
# 1) Detectăm automat cel mai nou folder RVTools
#  1) Rileviamo automaticamente la cartella RVTools più recente
# ==========================================================
def get_latest_rvtools_folder(base_dir):
    pattern = os.path.join(base_dir, "rvtools_*")
    folders = glob.glob(pattern)

    if not folders:
        raise Exception(f"Non ci sono directory in rvtools_* în: {base_dir}")

    latest = sorted(folders)[-1]
    date_str = os.path.basename(latest).replace("rvtools_", "")
    return latest, date_str


# ==========================================================
# 2) Generăm automat căile pentru RVTools (*.csv) pentru servere
# 2) Generiamo automaticamente percorsi RVTools (*.csv) per i server
# ==========================================================
def build_rvtools_paths(servers):
    latest_folder, date_str = get_latest_rvtools_folder(start_path)

    rv_files = [
        pr["RvTools_Host_Pattern"] + "." + pr["Extension_end"],
        pr["RvTools_Cluster_Pattern"] + "." + pr["Extension_end"],
        pr["RvTools_CPU_Pattern"] + "." + pr["Extension_end"],
        pr["RvTools_Info_Pattern"] + "." + pr["Extension_end"],
        pr["RvTools_Tools_Pattern"] + "." + pr["Extension_end"],
    ]

    all_paths = []

    for server in servers:
        server_folder = os.path.join(latest_folder, f"{server}_{date_str}")

        for f in rv_files:
            full_path = os.path.join(server_folder, f)
            all_paths.append(full_path)

    return all_paths


# ==========================================================
# 3) EXECUTIE
# ==========================================================

#  i nostri servers
servers = [
    "med-vvc-dg-0802",
    "med-vvc-pg-0801"
]

paths = build_rvtools_paths(servers)

for file in paths:
    print("Processing:", file)
    if os.path.exists(file):
        inlocuire_comma(file)
    else:
        print("!!! FIȘIER LIPSA -- NIENTE FILE:", file)
