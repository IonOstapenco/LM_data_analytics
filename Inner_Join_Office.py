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

# Cerco il file software (ICTG) mai recente in base al pattern da Parametri.json
cm.files = []
cm.list_files_scandir(cm.start_path, cm.pr["AD_SW_Pattern"], cm.pr["Extension_end"])
temp_sw = sorted(cm.files, reverse=True)
assert len(temp_sw) > 0, "Nessun file ICTG trovato. Controlla AD_SW_Pattern e Extension_end."
ictgc_file = temp_sw[0]
print("Elaborazione file software (ICTG): " + ictgc_file)

farm_df = pd.read_excel(farm_file, sheet_name="DNSName_sec_group_evo") #< --- citim din al doilea
ictgc_df = pd.read_csv(ictgc_file)

# Elaboriamo DNSName, estraiamo solo la prima parte (prima del ".")
farm_df['DNSName_processed'] = farm_df['DNSName'].str.split('.').str[0].str.strip().str.upper()

# Puliamo e convertiamo in maiuscolo anche "Nome computer"
ictgc_df['Nome computer'] = ictgc_df['Nome computer'].str.strip().str.upper()

# Eliminiamo i duplicati mantenendo solo le colonne necesare
farm_df_unique = farm_df[['DNSName_processed', 'Gruppi di AD']].drop_duplicates()
ictgc_df_unique = ictgc_df[['Nome computer', 'Nome componente']].drop_duplicates()

# Eseguiamo inner join
#
merged_df = pd.merge(
    farm_df_unique,
    ictgc_df_unique,
    left_on='DNSName_processed',
    right_on='Nome computer',
    how='inner'
)

# Risultato base
result_df = merged_df[['DNSName_processed', 'Gruppi di AD', 'Nome componente']].drop_duplicates()
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
        r'\bCTX_\d{3}_[A-Z0-9_]+_(?:ADS|PRD)\b',  # CTX_121_XLCUBED_ADS, CTX_121_XLCUBED_PRD
        r'\bUtenti [a-zA-Z]+ \d{3}\b',  # Utenti CCM 099, Utenti Daisy 099
        r'\bUTENTI [A-Z]+ \d{3}\b',  # UTENTI SDB 099
        r'\bUtenti Zeb Interni \d{3}\b',  # Utenti Zeb Interni 099
        r'\bSap \d{2}\b'  # Sap 99
    ]
    for row in df['Gruppi di AD']:
        if pd.notna(row):
            text = str(row)
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                gruppi.extend([(match, source) for match in matches])
    return gruppi

# Extragem grupurile cu indicația sursei
#estraiamo gruppi con indicazione della fonte/source
gruppi_standard = estrai_gruppi_univoci_noua(standard_df, 'STD')
gruppi_professional = estrai_gruppi_univoci_noua(professional_df, 'PRO')

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
output_file = os.path.join(cm.out_path, "Gruppi_Std_Prof.xlsx")
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, sheet_name='Matching_Servers', index=False)
    standard_df.to_excel(writer, sheet_name='Office Standard', index=False)
    professional_df.to_excel(writer, sheet_name='Office Professional', index=False)
    standard_univoci_df.to_excel(writer, sheet_name='Office Standard Univoci', index=False)
    professional_univoci_df.to_excel(writer, sheet_name='Office Professional Univoci', index=False)

# --- Salvataggio in TXT ---
output_fileTXT = os.path.join(cm.out_path, "Lista gruppi Office.txt")
with open(output_fileTXT, "w", encoding="utf-8") as f:
    for gruppo, source in gruppi_standard_list:
        f.write(f"{gruppo}|{source}\n")
    f.write("\n")  # Linie goală între secțiuni 
    for gruppo, source in gruppi_professional_list:
        f.write(f"{gruppo}|{source}\n")


#salvaggio in start path
output_fileTXT = os.path.join(cm.start_path, "Lista gruppi Office.txt")
with open(output_fileTXT, "w", encoding="utf-8") as f:
    for gruppo, source in gruppi_standard_list:
        f.write(f"{gruppo}|{source}\n")
#    f.write("\n")  # Linie goală între secțiuni
    for gruppo, source in gruppi_professional_list:
        f.write(f"{gruppo}|{source}\n")

print(f"Risultati TXT salvati in {output_fileTXT}")

print(f"Risultati salvati in {output_file} con i seguenti fogli:\n"
      f"- Matching_Servers\n"
      f"- Office Standard\n"
      f"- Office Professional\n"
      f"- Office Standard Univoci\n"
      f"- Office Professional Univoci")