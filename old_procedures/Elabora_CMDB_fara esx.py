import csv
import Common as cm


#3 in one, s-a integrat procedurele Extract_columns in 1, cu functie
# ----------------------------------------------------------
# normalizare   text (BOM + spatii) (este in toate Extract_columns _asset)  --: n
# !!nota-- : de incluis in exercitii
# --------------------------------------------------------------------------
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()

# --------------------------------------------- -- --    --------------------------------
# functie/metoda  pentru procesare fissiere
# --------------------------------------------------------------------------
def process_asset(name_class, fieldnames, file_pattern, main_field, output_file):
    class c_generic:
        def __init__(self, nome, dati):
            self.nome = nome
            self.dati = dati

    data = [] # pentru scirere sinc

    cm.check_outdir(cm.out_path)
    cm.files.clear()
    cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])
    temp = sorted(cm.files, reverse=True)
    if not temp:
        raise FileNotFoundError(f"Nu exista fisier {name_class}!")

    input_file = temp[0]
    print(f"Elaborare {name_class}:", input_file)

    with open(input_file, "r", encoding="utf-8") as f:
        delimiter = cm.cs
        header_line = None
#
        while True:
            pos = f.tell()
            line = f.readline()
            if not line:
                break
            clean = line.replace("\ufeff", "").strip() # stergem unde se gaseste BOM
            if clean.lower().startswith("sep="):
                delimiter = clean.split("=")[1]
                continue
            if main_field.lower() in clean.lower():
                header_line = clean
                f.seek(pos)
                break

        if not header_line:
            raise RuntimeError(f"Header {name_class} nu a fost gasit!")

        reader = csv.DictReader(f, delimiter=delimiter)
        reader.fieldnames = [norm(h) for h in reader.fieldnames]
        # aste un oarcare Debug
        print("Header detectat:", reader.fieldnames)

        for row in reader:
            row = {norm(k): v for k, v in row.items() if k is not None}
            nome = row.get(main_field, "").strip().lower()
            if not nome:
                continue
            data.append(c_generic(
                nome,
                [nome if field == main_field else row.get(field, "") for field in fieldnames]
            ))

    print(f"Record {name_class} citite:", len(data))

    # scriem in output
    out_path_file = cm.dr.join([cm.out_path, output_file])
    print("Scriere output:", out_path_file)
    with open(out_path_file, "w", encoding="utf-8", newline="") as f:
        f.write("sep=" + delimiter + "\n")
        f.write(delimiter.join(fieldnames) + "\n")
        for obj in data:
            f.write(delimiter.join(map(str, obj.dati)) + "\n")
    print(f"{name_class} finalizat ✔\n")
    return data

# ----------------------------------------------------------------
# Configurare la campuri asi files
# --------------------------------------------------------------------------
CMDB_field = ["Nome CI","OS","DNS","Domain Name","Is Virtual","Numero CPU","Numero Socket",
              "Processore","Modello","VM_Cluster","VM_Virtualcenter","VM_Host",
              "VMWare_LastReportDate","Bigfix_LastReportDate","Applicazioni (lista)",
              "Ruolo","Category","Type","Ambiente","Responsabile (Server)",
              "Used By","Contratto","server_iscloud","Ip_primary"]

DISS_field = ["server","datadismissione"]

PDL_field = ["Nome CI","Category","Type","Domain Name","Used By"]

# -------------------------------------------------------------
# prelucram pe toate
# -----------------------------------------------------------------
CMDB_data = process_asset("CMDB", CMDB_field, cm.pr["CMDB_Pattern"], "Nome CI", cm.pr["OUT_CMDB"])
DISS_data = process_asset("DISS", DISS_field, cm.pr["DISMESSI_Pattern"], "server", cm.pr["OUT_DISMESSI"])
PDL_data = process_asset("PDL", PDL_field, cm.pr["PDL_Pattern"], "Nome CI", cm.pr["OUT_PDL"])
