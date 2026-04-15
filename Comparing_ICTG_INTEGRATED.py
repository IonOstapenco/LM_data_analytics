import os
import csv
import json
import pandas as pd
from openpyxl import Workbook
from pathlib import Path

# ---------------------
# lettura del file parametri.json
with open("Parametri.json", encoding="utf-8") as f:
    config = json.load(f)

SOURCE_DIR = config["Source_dir"]
REPORT_DIR = config["Report_dir"]
OUTPUT_PATH = Path(SOURCE_DIR) / REPORT_DIR / config["Output_dir"]



# f-tie de cautare fisier dupa pattern
def gaseste_fisier(report_subdir, pattern, extensie=".csv"):
    """
    cauta primul fisier csv care contine pattern
    in folder Source_dir / report_subdir
    """
    base_path = SOURCE_DIR / report_subdir

    if not base_path.exists():
        print(f"[EROARE] folder does'nt exists: {base_path}")
        return None
    
    for root, _, files in os.walk(base_path):
        for file in files:
            if pattern in file and file.lower().endswith(extensie):
                return os.path.join(root, file)
            
    print(f)    
