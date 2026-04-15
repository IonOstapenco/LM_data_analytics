# Python Classi dati della tabella WIN

import csv
import Common as cm


# ------------------------------------------------------------------------------
class c_WIN:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


WIN = {}
Software = {}
ClusterName = {}

print("Procedura per la elaborazione dei dati da Tabella HW.")

# Verifica directory output
cm.check_outdir(cm.out_path)

mesg = "Elemento [{}/{}]"

# ==============================================================================
# 1️⃣ CARICAMENTO HARDWARE (DictReader)
# ==============================================================================

y = [cm.out_path, cm.pr["OUT_Hardware_TAB"]]
input_file = cm.dr.join(y)

Hardware = {}

with open(input_file, newline='', encoding='utf-8') as f:
    f.readline()  # skip sep=;

    reader = csv.DictReader(f, delimiter=cm.cs)

    # normalizează header
    reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]

    for row in reader:
        row = {k.strip().lower(): v for k, v in row.items()}
        Hardware[row["nome"]] = row

# ==============================================================================
# 2️⃣ CARICAMENTO SOFTWARE (DictReader)
# ==============================================================================

file_pattern = cm.pr["OUT_Software_TAB"]
cm.list_files_scandir(cm.out_path, file_pattern, cm.pr["Extension_end"])

print("Elaborazione file " + cm.files[0])

with open(cm.files[0], newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=cm.cs)

    for row in reader:
        nome = row.get("nome", "")
        componente = row.get("nome componente", "").lower()

        if "windows server" in componente:
            if "datacenter" in componente:
                Software[nome] = "datacenter"
            elif "standard" in componente:
                Software[nome] = "standard"
            elif "enterprise" in componente:
                Software[nome] = "enterprise"

# ==============================================================================
# 3️⃣ COSTRUZIONE TABELLA WIN
# ==============================================================================

WIN_columns = [
    "nome",
    "powerstate",
    "virtuale",
    "tipo",
    "n_cpu",
    "n_core",
    "cluster_name",
    "cluster_cores",
    "cluster_numhosts",
    "cluster_n_vms_win",
    "cliente",
    "ambiente",
    "destinazione",
    "contratto",
    "nome_edizione",
    "standard_lic_number",
    "datacenter_lic_number"
]

for k, hw in Hardware.items():

    sysop = hw.get("operating_system", "").lower()

    if ("windows server" in sysop) or ("win20" in sysop):

        WIN[k] = {}

        for campo in WIN_columns:

            if campo in ["nome_edizione",
                         "standard_lic_number",
                         "datacenter_lic_number"]:
                continue

            valore = hw.get(campo, "")

            # gestione cluster_cores (solo una volta per cluster)
            if campo == "cluster_cores":
                cluster = hw.get("cluster_name", "")

                if cluster in ClusterName:
                    WIN[k][campo] = "0"
                else:
                    ClusterName[cluster] = valore
                    WIN[k][campo] = valore
            else:
                WIN[k][campo] = valore

        # nome_edizione
        if k in Software:
            WIN[k]["nome_edizione"] = Software[k]
        else:
            WIN[k]["nome_edizione"] = "-"

# ==============================================================================
# 4️⃣ CALCOLO LICENZE
# ==============================================================================

for c in WIN:

    n_core = int(WIN[c]["n_core"]) if str(WIN[c]["n_core"]).isnumeric() else 0
    z = int(n_core / 2)

    if WIN[c]["virtuale"] == "SI":

        n_vmwin = int(WIN[c]["cluster_n_vms_win"]) if str(WIN[c]["cluster_n_vms_win"]).isnumeric() else 0
        n_hosts = int(WIN[c]["cluster_numhosts"]) if str(WIN[c]["cluster_numhosts"]).isnumeric() else 1
        n_ccores = int(WIN[c]["cluster_cores"]) if str(WIN[c]["cluster_cores"]).isnumeric() else 0

        w = n_vmwin / n_hosts

        if w > 6:
            WIN[c]["standard_lic_number"] = 0
            WIN[c]["datacenter_lic_number"] = int(round(n_ccores / 2))
        else:
            minimo = int(cm.pr["Minimo_lic_Win_vm"])
            WIN[c]["standard_lic_number"] = minimo if z < minimo else z
            WIN[c]["datacenter_lic_number"] = 0
    else:

        minimo = int(cm.pr["Minimo_lic_Win_fs"])

        if WIN[c]["nome_edizione"] == "datacenter":
            WIN[c]["standard_lic_number"] = 0
            WIN[c]["datacenter_lic_number"] = minimo if z < minimo else z
        else:
            WIN[c]["standard_lic_number"] = minimo if z < minimo else z
            WIN[c]["datacenter_lic_number"] = 0

# ==============================================================================
# 5️⃣ SCRITTURA FILE WIN
# ==============================================================================

y = [cm.out_path, cm.pr["OUT_WIN_TAB"]]
output_file = cm.dr.join(y)

with open(output_file, "w", newline='', encoding='utf-8') as f:

    f.write("sep=" + cm.cs + "\n")

    print("\nScrittura file " + output_file)

    # header
    f.write(cm.cs.join(WIN_columns) + "\n")

    lnome = list(WIN.keys())
    n = len(WIN)

    for j, c in enumerate(lnome):
        print('\r', mesg.format(j, n), end='', flush=True)

        valori = [str(WIN[c].get(col, "")) for col in WIN_columns]
        f.write(cm.cs.join(valori) + "\n")

print("\n>-----------------------------------------------------------<")
print("+-----------------------------------------------------------+")
print("!   Procedura Elabora_Tabella - WIN completata              !")
print("+-----------------------------------------------------------+")