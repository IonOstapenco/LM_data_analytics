import pandas as pd

file_ps = r"C:\License_Management\Report_202610\gruppi\Licenze_Office_STD_AD_RESULTS_ATTIVI E UNIQUE NAMES e Match AD.xlsx" # --> powershewll
file_py = r"C:\License_Management\Report_202610\gruppi\Licenze_Office_STD_AD_RESULTS_ATTIVI E UNIQUE NAMES e Match AD_TEST_PY.xlsx" # --> cu python, mai recent


columns = ["Name", "Principal Name", "Banche"]

ps = pd.read_excel(file_ps, sheet_name="Match AD")
py = pd.read_excel(file_py, sheet_name="Match AD")

for df in (ps, py):
    for col in columns:
        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )

# Comparăm rândurile, inclusiv eventualele duplicate
ps_counts = ps.groupby(columns).size().rename("PowerShell")
py_counts = py.groupby(columns).size().rename("Python")

comparison = pd.concat(
    [ps_counts, py_counts],
    axis=1
).fillna(0).astype(int)

print("\nRânduri diferite între rezultate:")
print(comparison[comparison["PowerShell"] != comparison["Python"]])

print("\nTotal PowerShell:", len(ps))
print("Total Python:", len(py))