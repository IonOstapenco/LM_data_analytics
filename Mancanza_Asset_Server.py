import pandas as pd
import csv
import openpyxl
import win32com.client as win32
#!! MAI INTAI TRANSFORMARE din CSV in XLSX!!
#pe umra voi integra in LM 
# Define the input and output file paths
csv_file_path = r'C:\Users\crme240\OneDrive - ION\Desktop\manca\Asset Server (ALL)-data-2026-02-02 09_52_41.csv'
excel_file_path = r'C:\Users\crme240\OneDrive - ION\Desktop\manca\MANCANZA_Server_FEBRAIO.xlsx'

"""
# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

print(f"Successfully converted {csv_file_path} to {excel_file_path}")

"""
csv_data = []
with open(csv_file_path)as file_obj:
    reader = csv.reader(file_obj)
    for row in reader:
        csv_data.append(row)


wb = openpyxl.Workbook()
sheet = wb.active
for row in csv_data:
    sheet.append(row)


wb.save(excel_file_path)


#================================\
# incercam sa facem un riepilogo 
#====================================