import os
import json
import pandas as pd
import time



"""
Cosa fa:

Filtra solo le VM in esecuzione.

Esclude le VM con sistema operativo RedHat o Sconosciuto.

Calcola le licenze per VM utilizzando la regola minimo 8 core → 1 licenza = 2 core.

Crea una colonna VM_Licensing_Report per ogni VM.

Aggrega per host (running_on) per il report finale, con:

Conteggio VM

Totale vCPU

Totale licenze

Minimo licenze

Esporta:

Report dettagliato per VM (VM_with_licenses.csv)

Report aggregato per host (Citrix_VM_Licensing_Report.csv)
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

input_file = os.path.join(Output_dir, VM_FILE)
output_folder = os.path.join(Source_dir, Output_dir)
output_file = os.path.join(Output_dir, "Citrix_VM_Licensing_Report.csv")


# --------------------------------------------------------------------------
# crea la cartella di output se non esiste

if not os.path.exists(output_folder):
    os.makedirs(output_folder)




# --------------------------------------------------------------------------------
# citim fisier VM Citrix
# lettura del file della macchina virtuale Citrix

df = pd.read_csv(input_file, sep = Separa_car, skiprows=1) # sarim peste un rand

#debug, colonne non lette
# visualizza le colonne rilevate prima della normalizzazione (la frequenza potrebbe non necessitare più di normalizzazione)
print("=== Coloane detectate în CSV (raw) / Colonne rilevate nel file CSV ===")
print(df.columns.tolist())


df.columns = [norm(c) for c in df.columns]

df["running_on"] = df["running_on"].str.upper().apply(norm)


# converti le CPU in valori numerici, per sicurezza
df["cpus"] = pd.to_numeric(df["cpus"], errors="coerce").fillna(0) # If 'coerce', then invalid parsing will be set as NaN.

#consideriamo solo le VM in modalità/stato di esecuzione
df_running = df[df["power_state"] == "Running"]


# ---------------------------------------------


#--------------------------------------------------------------
# filtraggio aggiuntivo

df_running = df_running[~df_running["operating_system"].str.contains("RedHat| Red Hat", case=False, na=False)]

# Numero di VM dopo il filtraggio

valid_vm = df_running.shape[0]
print(f"Numar VM valide (excluse RedHat): {valid_vm}")

#Calcolo del numero minimo di licenze: 4 per VM
# calcul licentee minim 4 per VM
licente_minime = valid_vm * 4
print(f"Licenzee minime pentru VM valide: {valid_vm} * 4 = {licente_minime}")



# ------- calcola dopo regola ----------------------------

def calc_licenze(core, vm=False):
    # core -- vCPU totali sull'host o sulla VM


    # vm --> se vero -- applica la regola Vm, altrimenti (se falso), applica la regola per l'host fisico
  
    # restituisce il numero di licenze (2 pacchetti principali)
  
    
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


report.to_csv(output_file, sep=Separa_car, index=False)

print("Report creato:", output_file)


print("Fisier:", input_file)
print("Ultima modificare:", time.ctime(os.path.getmtime(input_file)))