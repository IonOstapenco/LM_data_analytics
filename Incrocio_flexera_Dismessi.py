import pandas as pd

# fisiere
file_dismessi = r"C:\License_Management\Report_202604\Asset ServerDismessi (ALL).csv"
file_flexera = r"C:\License_Management\Report_202604\flexera_software_devices.xlsx"

# citire
df_dismessi = pd.read_csv(file_dismessi, sep=',', dtype=str)
df_flexera = pd.read_excel(file_flexera, dtype=str)

# vezi coloanele (important!)
print(df_flexera.columns)

# normalizezi coloanele cheie
df_dismessi['server'] = df_dismessi['server'].str.strip().str.lower()
df_flexera['deviceName'] = df_flexera['deviceName'].str.strip().str.lower()

# optional: daca ai FQDN
#df_dismessi['server'] = df_dismessi['server'].str.split('.').str[0]
#df_flexera['deviceName'] = df_flexera['deviceName'].str.split('.').str[0]

# join
df_join = df_dismessi.merge(
    df_flexera,
    left_on='server',
    right_on='deviceName',
    how='inner'
)

# output
output_file = r"C:\License_Management\OutPut\Dismessi_in_Flexera.csv"
df_join.to_csv(output_file, sep=',', index=False)

print("Gata:", output_file)