"""Asset ServerDismessi
sep=,
server,stato,datadismissione,vmware_lastreportdate,bigfix_lastreportdate,category,type,item,isvirtual,ruolo,ambiente,applicazioni,processore,numerocpu,numerocore,ram,serial_number,vmware_virtualcenter,manufacturer,bigfix_computerid,bigfix_computername,site,line,rack,iscloud,sito,usedby,ip_primary,model,serverid
"""

import csv
import unicodedata
import Common as cm

# --------------------------------------------------------------------------
# Normalizare text (BOM + spatii)
# --------------------------------------------------------------------------
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()


# --------------------------------------------------------------------------
# Clasa DISS
# --------------------------------------------------------------------------
class c_DISS:
    def __init__(self, nome, dati):
        self.nome = nome
        self.dati = dati

#din input Asset Server  Dismessi
#Asset ServerDismessi
#sep=,
#server,stato,datadismissione,vmware_lastreportdate,
# bigfix_lastreportdate,category,type,item,
# isvirtual,ruolo,ambiente,applicazioni,processore,
# numerocpu,numerocore,ram,serial_number,vmware_virtualcenter,
# manufacturer,bigfix_computerid,bigfix_computername,site,
# line,rack,iscloud,sito,usedby,ip_primary,model,serverid

# --------------------------------------------------------------------------
# Campuri dorite in OUTPUT (si ordinea lor)
# --------------------------------------------------------------------------
DISS_field = [
    "server",
    "datadismissione"
]

DISS = []
nomi = set()

# --------------------------------------------------------------------------
# Identificare fisier DISS
# --------------------------------------------------------------------------
cm.check_outdir(cm.out_path)

cm.files.clear()
cm.list_files_scandir(cm.start_path, cm.pr["DISMESSI_Pattern"], cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)

if not temp:
    raise FileNotFoundError("Nu exista fisier DISMESSI")

input_file = temp[0]
print("Elaborare DISMESSI:", input_file)

# --------------------------------------------------------------------------
# Citire Dismessi cu DictReader (robust)
# --------------------------------------------------------------------------
with open(input_file, "r", encoding="utf-8") as f:
    delimiter = cm.cs
    header_line = None

    # citim pana gasim header-ul real
    while True:
        pos = f.tell()
        line = f.readline()
        if not line:
            break

        clean = line.replace("\ufeff", "").strip()

        # detectare separator
        if clean.lower().startswith("sep="):
            delimiter = clean.split("=")[1]
            continue

        # detectare header real
        if "server" in clean:
            header_line = clean
            f.seek(pos)
            break

    if not header_line:
        raise RuntimeError("Header DISS nu a fost gasit!")

    reader = csv.DictReader(f, delimiter=delimiter)

    # normalizare header
    reader.fieldnames = [h.replace("\ufeff", "").strip() for h in reader.fieldnames]

    print("Header detectat:", reader.fieldnames)

    for row in reader:
        #row = {k.replace("\ufeff", "").strip(): v for k, v in row.items()}
        row = {
    k.replace("\ufeff", "").strip(): v
    for k, v in row.items()
    if k is not None
}


        

        nome = row.get("server", "").strip().lower()
        if not nome:
            continue

        DISS.append(c_DISS(
            nome,
            [nome if field == "server" else row.get(field, "") for field in DISS_field]
        ))



print("Record DISS citite:", len(DISS))

# --------------------------------------------------------------------------
# Scriere output DISS
# --------------------------------------------------------------------------
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_DISMESSI"]])
print("Scriere output:", output_file)

with open(output_file, "w", encoding="utf-8", newline="") as f:
    f.write("sep=" + delimiter + "\n")
    f.write(delimiter.join(DISS_field) + "\n")

    for obj in DISS:
        f.write(delimiter.join(map(str, obj.dati)) + "\n")

print("DISS finalizat ")
