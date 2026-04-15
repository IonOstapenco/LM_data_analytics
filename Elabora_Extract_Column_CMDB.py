import pandas as pd
import os
import re
# Classi Python per gestione dati BIGFIX

import Common as cm


print("Procedura per l’estrazione di una colonna da un file Excel, in particolare dal file: 20220125_Cedacri Standard Operating Model_v7 (working).xlsx")

# Assicuriamo l’esistenza della directory di output
cm.check_outdir(cm.out_path)

# Definiamo il pattern per il file Lista_CMDB
lista_cmdb_pattern = "Lista_CMDB"
lista_cmdb_ext = cm.pr["XLS_end"]  # ".xlsx"

# Ricerca del file Lista_CMDB
cm.files = []
cm.list_files_scandir(cm.start_path, lista_cmdb_pattern, lista_cmdb_ext)
lista_cmdb_files = sorted(cm.files, reverse=True)
assert len(lista_cmdb_files) > 0, f"Nessun file Lista_CMDB trovato. Controllare il pattern e l’estensione."
lista_cmdb_file = lista_cmdb_files[0]
print("Elaborazione del file Lista_CMDB: " + lista_cmdb_file)
