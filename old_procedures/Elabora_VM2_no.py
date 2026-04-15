# Python Classi dati server VM

import csv
import Common as cm

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class c_CPU:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


class c_TOOLS:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


class c_VM:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo


CPU = []
TOOLS = []
VM = []

CPU_field = {
    "VM": 0,
    "CPUs": 4,
    "Sockets": 5,
    "Cores p/s": 6
}

TOOLS_field = {
    "VM": 1,
    "VM Version": 5,
    "Tools": 6,
    "Tools Version": 7,
    "Required Version": 8,
    "Upgradeable": 9,
    "Upgrade Policy": 10
}

VM_field = {
    "VM": 0,
    "Powerstate": 1,
    "Template": 2,
    "SRM Placeholder": 3,
    "DNS Name": 4,
    "CPUs": 5,
    "Memory": 6,
    "Primary IP Address": 7,
    "HW version": 8,
    "Annotation": 9,
    "Datacenter": 10,
    "Cluster": 11,
    "Host": 12,
    "OS according to the configuration file": 13,
    "OS according to the VMware Tools": 14,
    "VM ID": 15,
    "VI SDK Server type": 16,
    "VI SDK API Version": 17,
    "VI SDK Server": 18,
    "Sockets": 19,
    "Cores p/s": 20,
    "Tools": 21,
    "Tools Version": 22,
    "Required Version": 23,
    "Upgradeable": 24,
    "Upgrade Policy": 25
}
n_VM_field = 19

# ------- Parole chiave ce indică excluderea
key_word = ["indismissione", "clone", "replica", "non_toccare", "test", "corrupt", "template", "issue_snap"]

# ---------------- Funcții auxiliare ----------------
def safe_open_csv(path):
    """Deschide CSV cu diferite encoding-uri posibile."""
    encodings = ['utf-8-sig', 'utf-8', 'latin1', 'cp1252']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.readlines(), enc
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Nu s-a putut citi fișierul {path} cu niciun encoding cunoscut.")


def find_vm_column(fieldnames):
    """Caută o coloană echivalentă cu 'VM' indiferent de formatare."""
    for f in fieldnames:
        if str(f).strip().lower() in ["vm", "vm name", "virtual machine", "nome vm"]:
            return f
    return None


# ---------------- START ----------------
print("Procedura per la elaborazione dei dati da RVTOOLS - tabvCPU.")
cm.check_outdir(cm.out_path)
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_CPU_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

# ------------------- CPU -------------------
for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")

    for c in CPU_field:
        CPU_field[c] = 0

    Linee, enc = safe_open_csv(w)
    print(f"[INFO] Encoding detectat pentru {w}: {enc}")

    separa = cm.trova_separa(Linee[0])
    tmp = cm.togli_apici(Linee[0], separa)
    y = tmp.split(cm.cs)
    n = len(y)
    i = 0
    for c in y:
        if c in CPU_field:
            CPU_field[c] = i
        i += 1
    del Linee[0]

    for i, linea in enumerate(Linee):
        print('\r', mesg.format(i), end='', flush=True)
        tmp = cm.togli_apici(linea, separa)
        y = tmp.split(cm.cs)
        nome = str(y[CPU_field["VM"]]).lower()
        t = [y[CPU_field[c]] for c in CPU_field]
        CPU.append(c_CPU(nome, t))

cm.scrivi_dati("OUT_CPU", CPU_field, CPU)

# ------------------- TOOLS -------------------
print("\nProcedura per la elaborazione dei dati da RVTOOLS - tabvTools.")
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Tools_Pattern"], cm.pr["Extension_end"])

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")

    Linee, enc = safe_open_csv(w)
    print(f"[INFO] Encoding detectat pentru {w}: {enc}")

    separa = cm.trova_separa(Linee[0])

    with open(w, mode='r', encoding=enc, errors="ignore") as file:
        TOOLS_righe = csv.DictReader(file, delimiter=separa, quotechar='"')
        vm_col = find_vm_column(TOOLS_righe.fieldnames)
        if vm_col is None:
            raise KeyError(f"Coloana 'VM' nu a fost găsită în {w}. Coloane disponibile: {TOOLS_righe.fieldnames}")
        for i, riga in enumerate(TOOLS_righe):
            nome = str(riga[vm_col]).lower()
            t = [riga.get(c, "") for c in TOOLS_field]
            TOOLS.append(c_TOOLS(nome, t))
            print('\r', mesg.format(i), end='', flush=True)

cm.scrivi_dati("OUT_TOOLS", TOOLS_field, TOOLS)

# ------------------- INFO -------------------
print("\nProcedura per la elaborazione dei dati da RVTOOLS - tabvInfo.csv")
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Info_Pattern"], cm.pr["Extension_end"])

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")

    Linee, enc = safe_open_csv(w)
    separa = cm.trova_separa(Linee[0])

    with open(w, mode='r', encoding=enc, errors="ignore") as file:
        VM_righe = csv.DictReader(file, delimiter=separa, quotechar='"')
        vm_col = find_vm_column(VM_righe.fieldnames)
        if vm_col is None:
            raise KeyError(f"Coloana 'VM' nu a fost găsită în {w}. Coloane disponibile: {VM_righe.fieldnames}")

        for i, riga in enumerate(VM_righe):
            print('\r', mesg.format(i), end='', flush=True)
            nome = str(riga[vm_col]).lower()

            if any(x in nome for x in key_word):
                continue

            l = list(VM_field.keys())
            t = [nome] + [riga.get(l[k], "") for k in range(1, n_VM_field)]
            z = c_VM(nome, t)

            # Join CPU 
            trovato = next((o for o in CPU if o.nome == nome), None)
            if trovato:
                z.dati[VM_field["CPUs"]] = trovato.dati[1]
                z.dati.append(trovato.dati[2])
                z.dati.append(trovato.dati[3])
            else:
                z.dati.extend([0, 0])

            # Join TOOLS
            trovato = next((o for o in TOOLS if o.nome == nome), None)
            if trovato:
                z.dati.extend(trovato.dati[2:7])
            else:
                z.dati.extend([0, 0, 0, 0, 0])

            if not any(v.nome == nome for v in VM):
                VM.append(z)

cm.scrivi_dati("OUT_VM", VM_field, VM)

print("\n+-----------------------------------------------------------+")
print("!   Procedura Elabora_VM completata             !")
print("+-----------------------------------------------------------+")
