import os
import csv
import json
import pandas as pd
from openpyxl import Workbook
from pathlib import Path


#-------------------------------
# citirea fisierului parametri.json
with open("Parametri.json", encoding="utf-8") as f:
    config = json.load(f)


#mapele din parametri.json
SOURCE_DIR = config["Source_dir"]
REPORT_DIR = config["Report_dir"]
OUTPUT_PATH = Path(SOURCE_DIR) / REPORT_DIR / config["Output_dir"]  


#f-tia de gasire fisier din mape

