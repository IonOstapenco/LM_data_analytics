import pandas as pd
import os
import logging
import re

# ----------------------------------------------------------------------
# CONFIGURARE
# --------------------------------------------------

base_folder = r"C:\Users\crme240\OneDrive - ION\Desktop\rvtools_extract_TEST"


# input file1 med-vvc-dg-0802
input_filename = "med-vvc-dg-0802.gbm.lan_CASTELLAZZO_DR_RVTools_export_all_2026-01-07_11.19.29.xlsx"
input_file = os.path.join(base_folder, input_filename)




# input file2 med-vvc-pg-0801.gbm.lan-RVTools_export_all_2026-01-07_11.11.57.xlsx
input_filename_second = "med-vvc-pg-0801.gbm.lan-RVTools_export_all_2026-01-07_11.11.57.xlsx"
input_file_second = os.path.join(base_folder, input_filename_second)

#pentru ambele fisiere 
sheets_to_export = ["vCluster", "vCPU", "vHost", "vInfo", "vTools"]

# ------------------------------------------------+-+--+++++++++++++++++++++++++------------
# DETECTARE PREFIX DIN NUME FIle
# -------------------------------------------------*------

# scoate partea dinainte de primul punct la fisierul 1
prefix_match = re.match(r"^[^.]+", input_filename)
# scoatem partea dinainte de primul punct la fisierul 2
prefix_match_second = re.match(r"^[^.]+", input_filename_second)

# conditia p-u prefix la primul fisier
if not prefix_match:
    raise ValueError("Nu s-a putut  sa determinam prefix din numele la fisier")

prefix = prefix_match.group(0)

# conditia p-u prefix la al doilea fisier
if not prefix_match_second:
    raise ValueError("Nu s-a putut  sa determinam prefix din numele la fisier")

prefix_second = prefix_match_second.group(0)



# Folder output automat --- pentru fisier 1 --> med-vvc-dg-0802
output_folder = os.path.join(base_folder, prefix)
os.makedirs(output_folder, exist_ok=True)


# Folder output automat --- pentru fisier 2 --> med-vvc-pg-0801
output_folder_second = os.path.join(base_folder, prefix_second)
os.makedirs(output_folder_second, exist_ok=True)




# --------------------------------------------------------=--------
# SETUP LOGGING  (tipa bonus --doar pentr fisier1)
# ---------------------------------------------------

log_file = os.path.join(output_folder, "export_log.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== START EXPORT ===")
logging.info(f"Fisier1 input: {input_file}")
logging.info(f"Folder1 output: {output_folder}")





# --------------------------------------------------
# CITIRE LISTA SHEET-URI EXISTENTE --> fisier 1
# --------------------------------------------------

try:
    excel_file = pd.ExcelFile(input_file)
    existing_sheets = excel_file.sheet_names
except Exception as e:
    logging.error(f"Eroare la deschiderea fisierului: {e}")
    raise




# =================================================================
# --------------------------------------------------
# CITIRE LISTA SHEET-URI EXISTENTE --> fisier 2
# --------------------------------------------------

try:
    excel_file_second = pd.ExcelFile(input_file_second)
    existing_sheets = excel_file_second.sheet_names
except Exception as e:
    logging.error(f"Eroare la deschiderea fisierului: {e}")
    raise


# =======================================================================
# --------------------------------------------------
# EXPORT SELECTIV --- > pentru de la fisier 1
# --------------------------------------------------

for sheet_name in sheets_to_export:

    if sheet_name not in existing_sheets:
        logging.warning(f"Sheet inexistent: {sheet_name}") # --> de la logging
        print(f" Sheet inexistent: {sheet_name}")
        continue
# taman aici se citeste excel si se inscrie in output
    try:
        df = pd.read_excel(excel_file_second, sheet_name=sheet_name)

        output_filename = f"RVTools_tab{sheet_name}.csv"
        output_path = os.path.join(output_folder, output_filename)

        df.to_csv(output_path, index=False, sep=";")

        logging.info(f"Export reusit: {output_filename}")
        print(f"Creat: {output_filename}")

    except Exception as e:
        logging.error(f"Eroare la export sheet {sheet_name}: {e}")
        print(f"Eroare la {sheet_name}: {e}")

logging.info("=== END EXPORT for file no2 ===")
print("\n Export finalizat pentru mapa 2.")



# ==============================================================================

# --------------------------------------------------
# EXPORT SELECTIV --- > pentru de la fisier 2
# --------------------------------------------------

for sheet_name in sheets_to_export:

    if sheet_name not in existing_sheets:
        logging.warning(f"Sheet inexistent: {sheet_name}") # --> de la logging
        print(f" Sheet inexistent: {sheet_name}")
        continue

    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        output_filename = f"RVTools_tab{sheet_name}.csv"
        output_path = os.path.join(output_folder, output_filename)

        df.to_csv(output_path, index=False, sep=";")

        logging.info(f"Export reusit: {output_filename}")
        print(f"Creat: {output_filename}")

    except Exception as e:
        logging.error(f"Eroare la export sheet {sheet_name}: {e}")
        print(f"Eroare la {sheet_name}: {e}")

logging.info("=== END EXPORT ===")
print("\n Export finalizat.")



"""
for filename in input_filenames:
    export_excel_file(filename)
"""