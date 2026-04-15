"""Asset Client
Asset Client
sep=,
Nome CI,Stato,Category,Type,Item,OS,Domain Name,Numero CPU,Processore,Ram,Serial Number,Manufacturer,Modello,Is Virtual,DNS,server_numerocore,Sala,Used By,Indirizzi IP,Data censimento in CMDB,ReconciliationIdentity-Server

   CÂMPURI FOLOSITE (PDL_field):
   - Nome CI
   - Category
   - Type
   - Domain Name
   - Used By

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
# Clasa PDL
# --------------------------------------------------------------------------
class c_PDL:
    def __init__(self, nome, dati):
        self.nome = nome
        self.dati = dati

#din input Asset CLient
#Asset Client
#sep=,
#Nome CI,Stato,Category,Type,Item,OS,Domain Name,Numero CPU,
# Processore,Ram,Serial Number,Manufacturer,Modello,
# Is Virtual,DNS,server_numerocore,Sala,Used By,Indirizzi IP,
# Data censimento in CMDB,ReconciliationIdentity-Server


# PDL_field sarà impostato dinamicamente dall’header
#PDL_field = {"Nome CI": 0, "Category": 2, "Type": 3, "Domain Name": 7, "Used By": 19}


# --------------------------------------------------------------------------
# Campuri dorite in OUTPUT (si ordinea lor)
# --------------------------------------------------------------------------
PDL_field = [
    "Nome CI",
    "Category",
    "Type",
    "Domain Name",
    "Used By"

]

PDL = []
nomi = set()

# --------------------------------------------------------------------------
# Identificare fisier PDL
# --------------------------------------------------------------------------
cm.check_outdir(cm.out_path)

cm.files.clear()
cm.list_files_scandir(cm.start_path, cm.pr["PDL_Pattern"], cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)

if not temp:
    raise FileNotFoundError("Nu exista fisier PDL * asset client!")

input_file = temp[0]
print("Elaborare PDL:", input_file)

# --------------------------------------------------------------------------
# Citire PDL cu DictReader (robust)
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
        raise RuntimeError("Header PSL nu a fost gasit!")

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


        

        nome = row.get("Nome CI", "").strip().lower()
        if not nome:
            continue

        PDL.append(c_PDL(
            nome,
            [nome if field == "server" else row.get(field, "") for field in PDL_field]
        ))



print("Record PDL citite:", len(PDL))

# --------------------------------------------------------------------------
# Scriere output PDL
# --------------------------------------------------------------------------
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_PDL"]])
print("Scriere output:", output_file)

with open(output_file, "w", encoding="utf-8", newline="") as f:
    f.write("sep=" + delimiter + "\n")
    f.write(delimiter.join(PDL_field) + "\n")

    for obj in PDL:
        f.write(delimiter.join(map(str, obj.dati)) + "\n")

print("PDL finalizat ")
