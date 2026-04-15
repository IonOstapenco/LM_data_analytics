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
# Clasa CMDB
# --------------------------------------------------------------------------
class c_CMDB:
    def __init__(self, nome, dati):
        self.nome = nome
        self.dati = dati

#din input Asset Server 
#sep=,
#Nome CI,Stato,Category,Type,Item,Ruolo,Ambiente,OS,Applicazioni (lista),
# Responsabile (Server),Applicazione,Responsabile (Applicazione),
# Domain Name,Uptime,Numero Socket,
# Numero CPU,Processore,Ram,Serial Number,
# VM_Cluster,VMWare_LastReportDate,VM_Host,VM_VMID,VM_VMName,
# VM_PowerState,VM_Virtualcenter,Manufacturer,Modello,Is Virtual,
# Bigfix_ComputerID,bigfix_computername,DNS,Bigfix_LastReportDate,server_numerocore,server_iscloud,Sito,Sala,Fila,Rack,Used By,Contratto,Ip_primary,Indirizzi IP,Data censimento in CMDB,ReconciliationIdentity-Server

# --------------------------------------------------------------------------
# Campuri dorite in OUTPUT (si ordinea lor)
# --------------------------------------------------------------------------
CMDB_field = [
    "Nome CI",
    "OS",
    "DNS",
    "Domain Name",
    "Is Virtual",
    "Numero CPU",
    "Numero Socket",
    "Processore",
    "Modello",
    "VM_Cluster",
    "VM_Virtualcenter",
    "VM_Host",
    "VMWare_LastReportDate",
    "Bigfix_LastReportDate",
    "Applicazioni (lista)",
    "Ruolo",
    "Category",
    "Type",
    "Ambiente",
    "Responsabile (Server)", #--> poate sa numim doar Responsabile
    "Used By",
    "Contratto",
    "server_iscloud",
    "Ip_primary"
]

CMDB = []
nomi = set()

# --------------------------------------------------------------------------
# Identificare fisier CMDB
# --------------------------------------------------------------------------
cm.check_outdir(cm.out_path)

cm.files.clear()
cm.list_files_scandir(cm.start_path, cm.pr["CMDB_Pattern"], cm.pr["Extension_end"])
temp = sorted(cm.files, reverse=True)

if not temp:
    raise FileNotFoundError("Nu exista fisier CMDB")

input_file = temp[0]
print("Elaborare CMDB:", input_file)

# --------------------------------------------------------------------------
# Citire CMDB cu DictReader (robust)
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
        if "Nome CI" in clean:
            header_line = clean
            f.seek(pos)
            break

    if not header_line:
        raise RuntimeError("Header CMDB nu a fost gasit!")

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

        CMDB.append(c_CMDB(
            nome,
            [nome if field == "Nome CI" else row.get(field, "") for field in CMDB_field]
        ))



print("Record CMDB citite:", len(CMDB))

# --------------------------------------------------------------------------
# Scriere output CMDB
# --------------------------------------------------------------------------
output_file = cm.dr.join([cm.out_path, cm.pr["OUT_CMDB"]])
print("Scriere output:", output_file)

with open(output_file, "w", encoding="utf-8", newline="") as f:
    f.write("sep=" + delimiter + "\n")
    f.write(delimiter.join(CMDB_field) + "\n")

    for obj in CMDB:
        f.write(delimiter.join(map(str, obj.dati)) + "\n")

print("CMDB finalizat ")
