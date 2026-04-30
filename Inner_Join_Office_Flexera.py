import pandas as pd
import os
import re
# Python classi dati BIGFIX

import Common as cm

print("Procedura per la elaborazione dei dati da BigFix.")

cm.check_outdir(cm.out_path)

# Cerco il file gruppi (Farm) più recente in base al pattern da Parametri.json
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["AD_Group_Pattern"], cm.pr["XLS_end"])
temp_group = sorted(cm.files, reverse=True)
assert len(temp_group) > 0, "Nessun file Farm-MT trovato. Controlla AD_Group_Pattern e XLS_end."
farm_file = temp_group[0]
print("Elaborazione file gruppi (Farm): " + farm_file)

# Cerco il file software FLEXERA più recente
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["FLEXERA_SW_Pattern"], cm.pr["XLS_end"])
temp_sw = sorted(cm.files, reverse=True)
assert len(temp_sw) > 0, "Nessun file FLEXERA trovato. Controlla FLEXERA_SW_Pattern e XLS_end."
flexera_file = temp_sw[0]
print("Elaborazione file software (FLEXERA): " + flexera_file)

flexera_df = pd.read_excel(flexera_file)

# farm_df = pd.read_excel(farm_file, sheet_name="DNSName_sec_group_evo") #< --- citim din al doilea

sheets = pd.read_excel(farm_file, sheet_name=["DNSName_sec_group", "DNSName_sec_group_evo"])

df1 = sheets["DNSName_sec_group"]
df2 = sheets["DNSName_sec_group_evo"]

# curățăm coloanele (foarte important)
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# combinăm
farm_df = pd.concat([df1, df2], ignore_index=True)



# Elaboriamo DNSName, estraiamo solo la prima parte (prima del ".")
farm_df['DNSName_processed'] = farm_df['DNSName'].str.split('.').str[0].str.strip().str.upper()

# sau
#flexera_df['deviceName'] = flexera_df['deviceName'].str.split('.').str[0]



# Eliminiamo i duplicati mantenendo solo le colonne necesare
farm_df_unique = farm_df[['DNSName_processed', 'Gruppi di AD']].drop_duplicates()


# Curățare date Flexera
# flexera_df['deviceName'] = flexera_df['deviceName'].str.strip().str.upper() # --> varianta mai veche 

flexera_df['deviceName'] = (
    flexera_df['deviceName']
    .str.split('.').str[0]   # elimină domeniul
    .str.strip()
    .str.upper()
)

# Filtrăm doar Office Standard și Professional Plus
flexera_df = flexera_df[
    flexera_df['name'].str.contains('Office Standard|Professional Plus', case=False, na=False)
]

# Selectăm coloanele necesare
flexera_df_unique = flexera_df[['deviceName', 'name']].drop_duplicates()

# Eseguiamo inner join
#
merged_df = pd.merge(
    farm_df_unique,
    flexera_df_unique,
    left_on='DNSName_processed',
    right_on='deviceName',
    how='inner'
)

# ========================================================================
# differencies
# --- DIFFERENZE: server presenti in FARM ma NON in FLEXERA (Office) ---

# care sunt in farm, dar nu sunt in flexera 
differences_df = pd.merge(
    farm_df_unique,
    flexera_df_unique,
    left_on='DNSName_processed',
    right_on='deviceName',
    how='left',
    indicator=True
)



# Păstrăm doar ce NU are match în Flexera
differences_df = differences_df[differences_df['_merge'] == 'left_only']

# Selectăm coloanele relevante
differences_df = differences_df[['DNSName_processed', 'Gruppi di AD']].drop_duplicates()
differences_df.columns = ['Nome Server', 'Gruppi di AD']


# --- DIFFERENZE: server presenti in FLEXERA ma NON in FARM ---

missing_in_farm_df = pd.merge(
    flexera_df_unique,
    farm_df_unique,
    left_on='deviceName',
    right_on='DNSName_processed',
    how='left',
    indicator=True
)

# Păstrăm doar ce NU are match în FARM
missing_in_farm_df = missing_in_farm_df[missing_in_farm_df['_merge'] == 'left_only']

# Selectăm coloanele relevante
missing_in_farm_df = missing_in_farm_df[['deviceName', 'name']].drop_duplicates()
missing_in_farm_df.columns = ['Nome Server', 'Nome componente']

# Risultato base
result_df = merged_df[['DNSName_processed', 'Gruppi di AD', 'name']].drop_duplicates()
result_df.columns = ['Nome Server', 'Gruppi di AD', 'Nome componente']


#masini de excludere de pe data de 29 /10/2025
#adaugat pe data de 29/10/2025

macchine_excluse = ["XA02MB2C", "XA11MA2C"]
# Filtriamo result_df rimuovendo le macchine escluse
result_df = result_df[~result_df['Nome Server'].isin(macchine_excluse)]

#ceva nu merge
#mexxhine_excluse = ["XA02MB2C", "XA11MA2C"]
#filtering
#result_df = result_df[~result_df['Nome']]




# Filtri separati per Office Standard e Professional
standard_df = result_df[
    result_df['Nome componente'].str.contains('Office Standard', case=False, na=False)
][['Nome Server', 'Gruppi di AD', 'Nome componente']].drop_duplicates()

professional_df = result_df[
    result_df['Nome componente'].str.contains('Professional Plus', case=False, na=False)
][['Nome Server', 'Gruppi di AD', 'Nome componente']].drop_duplicates()

# --- LISTE GRUPPI UNIVOCI ---
def estrai_gruppi_univoci_noua(df, source):
    gruppi = []
    patterns = [
        #r'\bCTX_\d{3}_[A-Z0-9_]+_(?:ADS|PRD)\b',  # CTX_121_XLCUBED_ADS, CTX_121_XLCUBED_PRD
        #r'\bCTX_\d{3}_[A-Z0-9_]+_(?:ADS|PRD)(?:\s+[A-Z0-9]+)*' # --> registru nou1
        #r'\bCTX_\d{3}_[A-Z0-9_]+_(?:ADS|PRD)(?:\s+[A-Z0-9]+)*\b' # --> registru nou2
        
        #r'\bCTX_\d{3}_[A-Z0-9_]+_(?:ADS|PRD)(?:\s+[A-Z0-9]+)*\b', # --> registru nou 3 - pentru grupe pro
        #r'\bUtenti [a-zA-Z]+ \d{3}\b',  # Utenti CCM 099, Utenti Daisy 099
        #r'\bUTENTI [A-Z]+ \d{3}\b',  # UTENTI SDB 099
        #r'\bUtenti Zeb Interni \d{3}\b',  # Utenti Zeb Interni 099
        #r'\bSap \d{2}\b'  # Sap 99


        r'\bCR\d{5}\b',  # CR00758, CR00972, CR10223
        r'\bCRE\d{4}\b',  # CRE1738
        r'\bCREN\d{3}\b',  # CREN102
        r'\bCRTSTCX\d*\b',  # CRTSTCX3
        r'\bCTX_\d{3}_[A-Z0-9_]+(?:_ADS|_PRD|_COL|_SVL|_BTU)?\b',  # CTX_099_DAISY, CTX_099_TTA_ADS
        
        r'\bUtenti [a-zA-Z]+ \d{3}\b',  # Utenti Daisy 099, Utenti CCM 099
        r'\bUTENTI [A-Z]+ \d{3}\b',  # UTENTI SDB 099
        r'\bUtenti Zeb Interni \d{3}\b',  # Utenti Zeb Interni 099
        r'\bSap \d{2}\b'  # Sap 99
    ]
    for row in df['Gruppi di AD']:
        if pd.notna(row):
            text = str(row)

            #DEBUG
            #print("DEBUG RAW:", repr(text))

            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                gruppi.extend([(match, source) for match in matches])
    return gruppi

# Extragem grupurile cu indicația sursei
#estraiamo gruppi con indicazione della fonte/source
gruppi_standard = estrai_gruppi_univoci_noua(standard_df, 'STD')
gruppi_professional = estrai_gruppi_univoci_noua(professional_df, 'PRO')

#debug
print("DEBUG !!! --> EXTRASE PRO:", gruppi_professional)

# Separăm grupurile pentru STD și PRO, eliminând duplicatele
# Separiamo i gruppi per STD e PRO, rimuovendo i duplicati
gruppi_standard_unique = {}
gruppi_professional_unique = {}
for gruppo, source in gruppi_standard:
    gruppi_standard_unique[gruppo] = source
for gruppo, source in gruppi_professional:
    gruppi_professional_unique[gruppo] = source

# Gestionăm grupurile care apar în ambele (prioritizăm PRO)
# Gestiamo gruppi che compaiono in entrambi (diamo priorità a PRO)
gruppi_standard_list = [(gruppo, source) for gruppo, source in gruppi_standard_unique.items()
                       if gruppo not in gruppi_professional_unique]
gruppi_professional_list = [(gruppo, source) for gruppo, source in gruppi_professional_unique.items()]
gruppi_standard_list.sort(key=lambda x: x[0].lower())
gruppi_professional_list.sort(key=lambda x: x[0].lower())

# --- ELENCO ESCLUSIONI ---
keywords_exclude = ["TOOL", "YHC0062", "SAP"]  # Adăugăm SAP la excluderi  // Aggiungiamo SAP all ' elenco delle esclusioni

def exclude_keywords(gruppi, exclude_keywords):
    """
Rimuove dall'elenco gli elementi che contengono una parola da exclude_keywords
come parola separata (non incollata in altro testo).
    """
    exclude_patterns = [
        re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)
        for k in exclude_keywords
    ]
    return [
        (gruppo, source) for gruppo, source in gruppi
        if not any(p.search(gruppo) for p in exclude_patterns)
    ]

# Aplicăm filtrul de excludere
# Applica il filtro di esclusione
gruppi_standard_list = exclude_keywords(gruppi_standard_list, keywords_exclude)
gruppi_professional_list = exclude_keywords(gruppi_professional_list, keywords_exclude)

# Debugging: Afișăm grupurile selectate
# Debug: Visualizzazione dei gruppi selezionati
print("\nGruppi Standard Univoci (după filtrare):")
for gruppo, source in gruppi_standard_list:
    print(f"{gruppo}|{source}")
print("\nGruppi Professional Univoci (după filtrare):")
for gruppo, source in gruppi_professional_list:
    print(f"{gruppo}|{source}")

# Pentru sheet-urile Excel, folosim funcția anterioară fără filtrul PRD/ADS/Utenti
# Per i fogli Excel, utilizziamo la funzione precedente senza il filtro PRD/ADS/Utenti
def estrai_gruppi_univoci_noua_excel(df):
    gruppi = []
    patterns = [
        r'\bCR\d{5}\b',  # CR00758, CR00972, CR10223
        r'\bCRE\d{4}\b',  # CRE1738
        r'\bCREN\d{3}\b',  # CREN102
        r'\bCRTSTCX\d*\b',  # CRTSTCX3
        r'\bCTX_\d{3}_[A-Z0-9_]+(?:_ADS|_PRD|_COL|_SVL|_BTU)?\b',  # CTX_099_DAISY, CTX_099_TTA_ADS
        
        r'\bUtenti [a-zA-Z]+ \d{3}\b',  # Utenti Daisy 099, Utenti CCM 099
        r'\bUTENTI [A-Z]+ \d{3}\b',  # UTENTI SDB 099
        r'\bUtenti Zeb Interni \d{3}\b',  # Utenti Zeb Interni 099
        r'\bSap \d{2}\b'  # Sap 99
    ]
    for row in df['Gruppi di AD']:
        if pd.notna(row):
            text = str(row)
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                gruppi.extend(matches)
    return sorted(set(gruppi), key=str.lower)



gruppi_standard_univoci = estrai_gruppi_univoci_noua_excel(standard_df)
gruppi_professional_univoci = estrai_gruppi_univoci_noua_excel(professional_df)

# Aplicăm filtrul de excludere pentru sheet-urile Excel (fără SAP)
# Applichiamo il filtro di esclusione per i fogli Excel (senza SAP)
gruppi_standard_univoci = exclude_keywords([(g, 'STD') for g in gruppi_standard_univoci], ["TOOL", "YHC0062"])
gruppi_standard_univoci = [g for g, _ in gruppi_standard_univoci]
gruppi_professional_univoci = exclude_keywords([(g, 'PRO') for g in gruppi_professional_univoci], ["TOOL", "YHC0062"])
gruppi_professional_univoci = [g for g, _ in gruppi_professional_univoci]

standard_univoci_df = pd.DataFrame(gruppi_standard_univoci, columns=['Gruppi di AD (Standard)'])
professional_univoci_df = pd.DataFrame(gruppi_professional_univoci, columns=['Gruppi di AD (Professional)'])

# Salvataggio in Excel con fogli multipli
output_file = os.path.join(cm.out_path, "FLEXERA_Gruppi_Std_Prof.xlsx")

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='Matching_Servers', index=False)
    differences_df.to_excel(writer, sheet_name='Missing_in_Flexera', index=False)
    missing_in_farm_df.to_excel(writer, sheet_name='Missing_in_Farm_MT', index=False)  # !! NOU
    standard_df.to_excel(writer, sheet_name='Office Standard', index=False)
    professional_df.to_excel(writer, sheet_name='Office Professional', index=False)
    standard_univoci_df.to_excel(writer, sheet_name='Office Standard Univoci', index=False)
    professional_univoci_df.to_excel(writer, sheet_name='Office Professional Univoci', index=False)

# --- Salvataggio in TXT ---
output_fileTXT = os.path.join(cm.out_path, "FLEXERA_Lista gruppi Office.txt")

with open(output_fileTXT, "w", encoding="utf-8") as f:
    for gruppo, source in gruppi_standard_list:
        f.write(f"{gruppo}|{source}\n")
    f.write("\n")  # Linie goală între secțiuni
    for gruppo, source in gruppi_professional_list:
        f.write(f"{gruppo}|{source}\n")


#salvaggio in start path
output_fileTXT = os.path.join(cm.start_path, "Lista gruppi Office_FLEXERA.txt")
with open(output_fileTXT, "w", encoding="utf-8") as f:
    for gruppo, source in gruppi_standard_list:
        f.write(f"{gruppo}|{source}\n")
#    f.write("\n")  # Linie goală între secțiuni
    for gruppo, source in gruppi_professional_list:
        f.write(f"{gruppo}|{source}\n")
print(f"Risultati TXT salvati in {output_fileTXT}")

output_diff_txt = os.path.join(cm.out_path, "FLEXERA_Missing_Servers.txt")

with open(output_diff_txt, "w", encoding="utf-8") as f:
    for server in differences_df['Nome Server']:
        f.write(f"{server}\n")

# ast apentru 
output_missing_farm_txt = os.path.join(cm.out_path, "FLEXERA_Missing_in_Farm_MT.txt")

with open(output_missing_farm_txt, "w", encoding="utf-8") as f:
    for server in missing_in_farm_df['Nome Server']:
        f.write(f"{server}\n")




print(f"Risultati TXT salvati in {output_missing_farm_txt}")



print(f"Risultati TXT salvati in {output_diff_txt}")


print(f"Risultati salvati in {output_file} con i seguenti fogli:\n"
      f"- Missing_in_flexERA\n"
      f"- Matching_Servers\n"
      f"- Office Standard\n"
      f"- Office Professional\n"
      f"- Office Standard Univoci\n"
      f"- Office Professional Univoci")