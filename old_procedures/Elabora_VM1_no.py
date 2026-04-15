# Python Classi dati server VM

from sys import exit
import csv
import Common as cm
import chardet

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class c_CPU:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

CPU = []
CPU_field = { "VM": 0,
               "CPUs": 4,
               "Sockets": 5,
               "Cores p/s": 6
              }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_TOOLS:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

TOOLS = []
TOOLS_field = {"VM": 1,              
                 "VM Version": 5,      
                 "Tools": 6,           
                 "Tools Version": 7,   
                 "Required Version": 8,
                 "Upgradeable": 9,     
                 "Upgrade Policy": 10  
                }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class c_VM:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo

VM = []
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

key_word = ["indismissione", "clone", "replica", "non_toccare", "test", "corrupt", "template", "issue_snap"]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da RVTOOLS - tabvCPU.")

cm.check_outdir(cm.out_path)

cm.list_files_scandir(cm.start_path, cm.pr["RvTools_CPU_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
    for c in CPU_field:
        CPU_field[c] = 0
    try:
        fc = open(w, "r", encoding='latin1')
        Linee = fc.readlines()
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
        i = 0
        for linea in Linee:
            print('\r', mesg.format(i), end='', flush=True)
            tmp = cm.togli_apici(linea, separa)
            y = tmp.split(cm.cs)
            nome = str(y[CPU_field["VM"]]).lower()
            t = []
            for c in CPU_field:
                t.append(y[CPU_field[c]])
            z = c_CPU(nome, t)
            CPU.append(z)
            i += 1
        fc.close()
    except Exception as e:
        print(f"Eroare la procesarea {w}: {e}")
        continue

cm.scrivi_dati("OUT_CPU", CPU_field, CPU)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da RVTOOLS - tabvTools.")

cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Tools_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
    for c in TOOLS_field:
        TOOLS_field[c] = 0

    # Detectează encoding-ul
    try:
        with open(w, 'rb') as f:
            result = chardet.detect(f.read(10000))
            encoding = result['encoding'] or 'latin1'
            print(f"Encoding detectat: {encoding}")
    except Exception as e:
        print(f"Eroare la detectarea encoding-ului pentru {w}: {e}")
        encoding = 'latin1'

    # Citește antetul și forțează delimitatorul ';'
    try:
        with open(w, 'r', encoding=encoding) as f:
            first_line = f.readline().strip()
            separa = ';'  # Forțăm delimitatorul pe baza antetului
            print(f"Antet: {first_line}")
            print(f"Coloane detectate (brut): {first_line.split(separa)}")
    except Exception as e:
        print(f"Eroare la citirea antetului pentru {w}: {e}")
        continue

    # Verifică antetul și rândurile
    try:
        with open(w, 'r', encoding=encoding) as file:
            reader = csv.DictReader(file, delimiter=separa, quotechar='"')
            print(f"Coloane mapate de DictReader: {reader.fieldnames}")
            if not reader.fieldnames:
                print(f"Eroare: Antetul nu a fost citit corect în {w}. Verifică fișierul!")
                continue
            if "VM" not in reader.fieldnames:
                print(f"Eroare: Coloana 'VM' nu există în {w}. Coloane disponibile: {reader.fieldnames}")
                continue
            if not all(field in reader.fieldnames for field in TOOLS_field):
                missing = [f for f in TOOLS_field if f not in reader.fieldnames]
                print(f"Eroare: Următoarele coloane lipsesc în {w}: {missing}")
                continue

            i = 0
            for riga in reader:
                print('\r', mesg.format(i), end='', flush=True)
                if len(riga) < len(reader.fieldnames):
                    print(f"\nRând corupt {i+2}: Număr insuficient de coloane. Rând: {riga}")
                    continue
                try:
                    nome = str(riga["VM"].strip()).lower()
                    if not nome:
                        print(f"\nRând {i+2}: Coloana 'VM' este goală. Rând: {riga}")
                        continue
                except KeyError:
                    print(f"\nEroare: Coloana 'VM' lipsește în rândul {i+2}. Rând: {riga}")
                    continue
                t = []
                for c in TOOLS_field:
                    t.append(riga.get(c.strip(), ""))
                z = c_TOOLS(nome, t)
                TOOLS.append(z)
                i += 1
    except Exception as e:
        print(f"Eroare la procesarea {w}: {e}")
        continue

cm.scrivi_dati("OUT_TOOLS", TOOLS_field, TOOLS)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da RVTOOLS - tabvInfo.csv")

cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["RvTools_Info_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")

    try:
        with open(w, 'rb') as f:
            result = chardet.detect(f.read(10000))
            encoding = result['encoding'] or 'latin1'
            print(f"Encoding detectat: {encoding}")

        with open(w, 'r', encoding=encoding) as f:
            first_line = f.readline().strip()
            separa = ';'  # Forțăm delimitatorul

        with open(w, 'r', encoding=encoding) as file:
            i = 0
            VM_righe = csv.DictReader(file, delimiter=separa, quotechar='"')
            if not VM_righe.fieldnames:
                print(f"Eroare: Antetul nu a fost citit corect în {w}. Verifică fișierul!")
                continue
            if "VM" not in VM_righe.fieldnames:
                print(f"Eroare: Coloana 'VM' nu există în {w}. Coloane disponibile: {VM_righe.fieldnames}")
                continue

            for riga in VM_righe:
                print('\r', mesg.format(i), end='', flush=True)
                if len(riga) < len(VM_righe.fieldnames):
                    print(f"\nRând corupt {i+2}: Număr insuficient de coloane. Rând: {riga}")
                    continue
                try:
                    nome = str(riga["VM"].strip()).lower()
                    if not nome:
                        print(f"\nRând {i+2}: Coloana 'VM' este goală. Rând: {riga}")
                        continue
                except KeyError:
                    print(f"\nEroare: Coloana 'VM' lipsește în rândul {i+2}. Rând: {riga}")
                    continue

                trovato = 0
                for x in key_word:
                    if nome.find(x) >= 0:
                        trovato = 1
                if trovato == 1:
                    continue
                l = list(VM_field.keys())
                t = []
                t.append(nome)
                for k in range(1, n_VM_field):
                    t.append(riga.get(l[k].strip(), ""))

                z = c_VM(nome, t)
                trovato = next((o_g for o_g in CPU if o_g.nome == nome), None)
                try:
                    z.dati[VM_field["CPUs"]] = trovato.dati[1]
                    z.dati.append(trovato.dati[2])
                    z.dati.append(trovato.dati[3])
                except:
                    z.dati.append(0)
                    z.dati.append(0)

                trovato = next((o_g for o_g in TOOLS if o_g.nome == nome), None)
                try:
                    z.dati.append(trovato.dati[2])
                    z.dati.append(trovato.dati[3])
                    z.dati.append(trovato.dati[4])
                    z.dati.append(trovato.dati[5])
                    z.dati.append(trovato.dati[6])
                except:
                    z.dati.append(0)
                    z.dati.append(0)
                    z.dati.append(0)
                    z.dati.append(0)
                    z.dati.append(0)

                trovato = 0
                n = len(VM)
                for x in range(0, n):
                    if VM[x].nome == nome:
                        trovato = 1
                        break
                if trovato == 1:
                    continue

                VM.append(z)
                i += 1
    except Exception as e:
        print(f"Eroare la procesarea {w}: {e}")
        continue

cm.scrivi_dati("OUT_VM", VM_field, VM)

print("+-----------------------------------------------------------+")
print("!   Procedura Elabora_VM completata                         !")
print("+-----------------------------------------------------------+")
