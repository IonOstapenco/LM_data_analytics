import os
import json
import pandas as pd
import time




"""
Ce face :

Filtru doar VM-urile Running.


Exclude VM-urile cu operating_system RedHat sau Unknown.

Calculeaza licentele per VM folosind regula minim 8 core → 1 licenta = 2 core.

Creeazaa coloana Licente_VM per VM.

Face agregarea per host (running_on) pentru raportul final, cu:

numar VM (VM_Count)

total vCPU (Total_vCPU)

total licente (Licente_minimie)

Exporteaza: 

raport detagliat per VM (VM_with_licenses.csv)

raport agregat per host (Citrix_VM_Licensing_Report.csv)
"""
# ───────────────────────────────────────────────
# Normalizare texte (fără BOM, spații inutile)
# ───────────────────────────────────────────────
def norm(s, lower=False):
    if s is None:
        return ""
    s = s.replace("\ufeff", "").strip()
    return s.lower() if lower else s


# ==========================================================
# 0. Leggere Parametri.json per INPUT e OUTPUT
# 0. Citire parametri.json pentru INPUT si OUTPUT
# ==========================================================

with open("parametri.json", "r", encoding="utf-8") as f:
    parametri = json.load(f)

Source_dir = parametri["Source_dir"]
#Output_dir = os.path.join(Source_dir, parametri["Output_dir"])  # "C:/License_Management/Report_202602/OutPut"
Output_dir = os.path.join(parametri["Source_dir"], parametri["Report_dir"], parametri["Output_dir"])
Separa_car = parametri["Separa_car"] # --- separator la output ca la input sa fie

# ------- 

VM_FILE = parametri["OUT_Vms_Citrix"]
MIN_VM_CORE = int(parametri["Minimo_lic_Win_vm"])

# --- "Minimo_lic_Win_vm": "4", ---> Penso che questo dovrebbe essere inserito nell'output, terza colonna
# ---  "Minimo_lic_Win_vm": "4", ---> cred ca asta de pus la output, a 3-a coloana
input_file = os.path.join(Output_dir, VM_FILE)
output_folder = os.path.join(Source_dir, Output_dir)
output_file = os.path.join(Output_dir, "Citrix_VM_Licensing_Report.csv")


# --------------------------------------------------------------------------
# crea la cartella di output se non esiste
# cream folder output daca nu este 

if not os.path.exists(output_folder):
    os.makedirs(output_folder)




# --------------------------------------------------------------------------------
# citim fisier VM Citrix
# lettura del file della macchina virtuale Citrix

df = pd.read_csv(input_file, sep = Separa_car, skiprows=1) # sarim peste un rand

#debug, colonne non lette
# visualizza le colonne rilevate prima della normalizzazione (la frequenza potrebbe non necessitare più di normalizzazione)
#debug , nu se citea coloanele
# afisam coloanele detectate inainte de normalizare (hz poate nu mai trebuie normalizare)
print("=== Coloane detectate în CSV (raw) / Colonne rilevate nel file CSV ===")
print(df.columns.tolist())


df.columns = [norm(c) for c in df.columns]

df["running_on"] = df["running_on"].str.upper().apply(norm)


# converti le CPU in valori numerici, per sicurezza
# convertire cpus la numeric, pentru orice eventualitate
df["cpus"] = pd.to_numeric(df["cpus"], errors="coerce").fillna(0) # If 'coerce', then invalid parsing will be set as NaN.

#consideriamo solo le VM in modalità/stato di esecuzione
#consideram numai VM in regim/stare de Running
df_running = df[df["power_state"] == "Running"]


"""

# !! punem pivot aici ------------------------------------
print("************************************\n")
df_os_summary = df[df["power_state"] == "Running"].copy()

os_summary = df_os_summary.groupby("operating_system").agg(
    VM_Count=("name", "count"),
    Total_vCPU=("cpus", "sum")
).reset_index()

print("************************************\n")
print(os_summary)
"""

# ---------------------------------------------


#--------------------------------------------------------------
# filtraggio aggiuntivo
# filtrare suplimentara
df_running = df_running[~df_running["operating_system"].str.contains("RedHat| Red Hat", case=False, na=False)]

# Numero di VM dopo il filtraggio
# numar VM dupa filtrare
valid_vm = df_running.shape[0]
print(f"Numar VM valide (excluse RedHat): {valid_vm}")

#Calcolo del numero minimo di licenze: 4 per VM
# calcul licentee minim 4 per VM
licente_minime = valid_vm * 4
print(f"Licenzee minime pentru VM valide: {valid_vm} * 4 = {licente_minime}")



# ------- calcola dopo regola ----------------------------

def calc_licenze(core, vm=False):
    # core -- vCPU totali sull'host o sulla VM
    # core -- total vCPU pe host sau vm

    # vm --> se vero -- applica la regola Vm, altrimenti (se falso), applica la regola per l'host fisico
    # vm --> if True -- se aplica regula Vm, else (daca False), se aplica regula pentru fizic(host)
    
    # restituisce il numero di licenze (2 pacchetti principali)
    # returneaza nr de licente (pachete de 2 core)
    
    if vm:
        # regula per VM
        if core <8:
            core_to_lic = 8   # minim 8 core per vm
        else:
            core_to_lic = core
    else: # regula per fizico 
        if core <16:
            core_to_lic = 16   # minimum 16 core per fizico
        else:
            core_to_lic = core

    #fiecare licente acopera 2 core
    #ogni licenza copre 2 core
    licenze = core_to_lic//2   # --> poate  de inmultit la  * 0.5
    return licenze   

df_running["Licente_VM"] = df_running["cpus"].apply(lambda x: calc_licenze(x, vm=True)) # cu expresia lambda, ca la java




# ==========================================================================
# PIVOT pe Operating System pentru VM cu licente (filtrate)
# =============================================================

os_summary_filtered = df_running.groupby("operating_system").agg(
    VM_Count=("name", "count"),
    Total_vCPU=("cpus", "sum"),
    Total_Licente=("Licente_VM", "sum")
).reset_index()

print("\n=== SUMAR OS (doar VM licentiate) ===")
print(os_summary_filtered)
# --------------- 

# !! Calcolo della VM per host
# !! Calcul VM per host

report = df_running.groupby("running_on").agg(   # ---> cred ca voi pune dupa agregare
    VM_Count=("name", "count"),
    Total_vCPU = ("cpus", "sum"),
    Licente_minimie = ("Licente_VM", "sum")
    
).reset_index()


# export detaliat per VM dupa filtrare 
df_running.to_csv(
    os.path.join(Output_dir, "VM_with_licenses.csv"),
    sep=Separa_car,
    index=False
)
print("Report creato (detaliat VM):", os.path.join(Output_dir, "VM_with_licenses.csv"))


# ----------------------------------------------------------------

# ---------------------------------------------------
# Salva il report
# Salvare raport

report.to_csv(output_file, sep=Separa_car, index=False)

print("Report creato:", output_file)



# ---------------------------------------------------------------

# PIVOT TABLES

# --------------------------------------------------------------------

# mai intai afisam suma la componente din Vms_Citrix_list

# -------------------------------------------------------
# Cedacri Section (unde coloanele doar produzione la funzione)
# --------------------------------------------------------------------------------

# sum la operating_system --> Unknown



# sum la operating_system --> Windows Server 2008 R2 Standard

# sum la operating_system --> Windows Server 2012 R2 Standard

# sum la operating_system --> Windows Server 2016 Standard

# afisare total 

# --------------------------w----------------------------------------------------

# -------------------------------------------------------
# Volterra, etica Section (unde coloanele doar produzione la funzione)
# --------------------------------------------------------------------------------

# sum la operating_system --> Windows Server 2019 Standard

# sum la operating_system --> Windows Server 2022 Standard

# afisare total 

# -----------------------------------------------------------------------------


### --------------------------

"""
### !!! DE MODIFICAT!!!! LUAT DIN procedura PIVOT ASSET MANCANZA

## SALVARE IN CSV


# ---- de salvat in output. txt

with open(output_path, 'w', encoding='utf-8') as f:

# s-a ccopiat de mai sus, in loc de print  -- f.write
    f.write(f"total la Ruolo este ")
    f.write(f"{tab1_tot}\n")
    f.write(f"---------------------------------------------\n") 
    #
    f.write(f"total este total la Ambiente este ")
    f.write(f"{tab2_tot}\n") 
    f.write(f"---------------------------------------------\n")    

    f.write(f"total la os este ")
    f.write(f"{tab3_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la Numero Socket este ")
    f.write(f"{tab4_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la Domain Name este ")
    f.write(f"{tab5_tot}\n")
    f.write(f"---------------------------------------------\n") 

    f.write(f"total la Numero CPU este ")
    f.write(f"{tab6_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la Used By este ")
    f.write(f"{tab7_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la Contratto este ")
    f.write(f"{tab8_tot}\n")
    f.write(f"---------------------------------------------\n") 
    

    f.write(f"total la Is Virtual este ")
    f.write(f"{tab9_tot}\n")
    f.write(f"---------------------------------------------\n") 


    f.write(f"total la Manufacturer este ")
    f.write(f"{tab10_tot}\n")
    f.write(f"---------------------------------------------\n")        

#tabela finala
    f.write("*********************************************-\n")
    f.write("\n")
    f.write("** tabela finala ***\n")
    f.write("=============================================\n")
    f.write("Category       | Servers (blank) | Percentage\n")
    f.write("---------------|-----------------|-----------\n")

    #ciclu
    for categorie, valoare in raport:
        procent = (valoare / suma_totala) * 100
        f.write(f"{categorie:<14} | {valoare:>15} | {procent:>9.2f}%\n")
        f.write("---------------|-----------------|-----------\n")

# Total final
    f.write(f"{'Total servers':<14} | {suma_totala:>15} | {100:>9.2f}%\n")
    f.write("---------------|-----------------|-----------")

print("fisier s-a sasalvat cu succes!")




"""

print("Fisier:", input_file)
print("Ultima modificare:", time.ctime(os.path.getmtime(input_file)))