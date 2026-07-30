import subprocess

ps_script = r'''

# ==========================================
# modificari pentru integrare
# DECLARARE MAPE 
# ===================================================
$config = Get-Content "Parametri.json" -Raw | ConvertFrom-Json

$rootDir = $config.Source_dir
$reportDir = $config.Report_dir
$outputDir = $config.Output_dir

# ==================================================
$basePath = Join-Path $rootDir $reportDir # se unesc mapele C:\\License_Management" si Report_202606
# ================================================================================

# Citire GRUPURI din fisierul FLEXERA _Lista gruppi Office.txt
# ==========================================================

# de facut criterii de extragere-- 
# dupa PRD, COL, ADS

# fisier de grupuri
$groupFile  = Join-Path `
    (Join-Path $basePath $outputDir) `
    "FLEXERA_Lista gruppi Office.txt"

# daca nu este flexera -- se afiseaza mseaj    
if (-not (Test-Path $groupFile)) {
    Write-Error "Nu gaseste fisierul: $groupFile"
    exit 1
}    

# obtinerea grupelor din Flexera Lista gruppi Office
$groups = Get-Content $groupFile |
    ForEach-Object {
        $parts = $_ -split "\|"

    # conditia de sortare -- > intram doar acolo unde este STD
        if ($parts.Count -ge 2 -and $parts[1].Trim().ToUpper() -eq "STD") {

            $grp = $parts[0].Trim().ToLower()

            #normalizare  ---> optional -- transformam din prod in prd
            $grp  = $grp -replace "_prod$", "_prd" 
            $grp # un fel de return grp ca in java
        }
} | 
Sort-Object -Unique

# ---------------------------
# ==== BLOC cu regula veche
# ================== IDENTIFICARE GRUPURI MIXTE DIN LISTA ORIGINALĂ ==================

$groupMap = @{}

foreach ($g in $groups) {

    $g = $g.Trim().ToLower()

    if ($g -match "^(.*)_(prd|ads|col)$") {

        $base = $matches[1]
        $type = $matches[2]

        if (-not $groupMap.ContainsKey($base)) {
            $groupMap[$base] = New-Object System.Collections.Generic.HashSet[string]
        }

        $groupMap[$base].Add($type) | Out-Null
    }
}

# EXCEPTII care trebuie păstrate
$exceptions = @(
    "ctx_047_tta"
)

# păstrăm:
# - bazele care au exclusiv PRD
# - SAU cele din lista de excepții
$validBases = $groupMap.GetEnumerator() |
    Where-Object {

        ($_.Value.Count -eq 1 -and $_.Value.Contains("prd")) -or
        ($exceptions -contains $_.Key)

    } |
    Select-Object -ExpandProperty Key


# =============================================
# reconstruim lista FINALĂ de grupuri --- > poate de lasat sau modificat si integrat in nmetoda noua
$groups = foreach ($base in $validBases) {

    # excepție specială
    if ($base -eq "ctx_047_tta") {
        "${base}_ads"
    }
    else {
        "${base}_prd"
    }
}



# --- ? 


$outputPath = Join-Path $basePath "gruppi" # in mapa Report_202606 se va crea mapa gruppi


# prima varianta pentru citirea AD_Users_Results_attivi
$adUsersFile = Join-Path `
        (Join-Path $basePath "output-1") `
        $config.AD_Users_Results_attivi

        
New-Item -ItemType Directory -Path $outputPath -Force | Out-Null

# ================== CITIRE FILE ==================
$files = Get-ChildItem $basePath -Recurse -Filter AD-usersAndGroupsResult.csv


# adaugat
# ================== AD USERS / BANCHE ==================

# prima linie este "sep=|", o ignorăm
$adUsers = Get-Content $adUsersFile | Select-Object -Skip 1 | ConvertFrom-Csv -Delimiter "|"

$bancheMap = @{}

foreach ($u in $adUsers) {

    if ([string]::IsNullOrWhiteSpace($u."Principal Name")) {
        continue
    }

    # AG00924@ced.it -> AG00924
    $sam = ($u."Principal Name".Split("@")[0]).Trim().ToUpper()

    if (-not $bancheMap.ContainsKey($sam)) {

        $bancheMap[$sam] = $u.OU_01
    }
}

#pentru debug
#Write-Host "Banche caricate:" $bancheMap.Count
#=======================


#  =================== NORMALIZARE ============================

function Normalize-Name {
    param([string]$Name)

    if ([string]::IsNullOrWhiteSpace($Name)) {
        return $Name
    }

    $n = $Name.Trim()

    # elimină ?, _, -, . la final
    $n = $n -replace '[?_.-]+$',''

    # elimină cifrele de la final
    $n = $n -replace '\s+\d+$',''

    # elimină _1, _2, _3 etc.
    $n = $n -replace '[_ ]+\d+$',''

    # elimină spații multiple
    $n = $n -replace '\s+',' '

    # elimina cuvantul bis din nume
    $n = $n -replace '(?i)\s+bis$',''

    return $n.Trim()
}


###
#=============

# ====================================

# ================== PROCESARE ==================
# Aici se extrag efectiv utilizatorii din toate fișierele Active Directory. 
$allResults = foreach ($file in $files) {

    $currentFile = $file.FullName
# AICI DE SCHIMBAT  K E GREU!!!!
    foreach ($group in $groups) {

        Select-String -Path $currentFile -Pattern $group -CaseSensitive:$false |
        ForEach-Object {

            $cols = $_.Line -split ";"

            if ($cols.Count -ge 6) {
			
                [PSCustomObject]@{
                    Group          = $group
                    Name           = Normalize-Name $cols[4]
                    SamAccountName = $cols[5]
                    SourceFile     = $currentFile   #  util pentru debug
                }
            }
        }
    }
}

# ============ scoatem cuvantul Test, nu se inscriu acelea unde este Test in coloana Name 

# elimina toate care contin TEST

$allResults = $allResults |
    Where-Object {
        $_.Name -notmatch '(?i)\btest\b'
    }

# ===================================================
# ================== ELIMINARE LOGIN DIN NAME ==================

# CAM TOT CAM GREU!!!! 
$allResults = $allResults | Where-Object {

    $currentSam  = $_.SamAccountName.Trim().ToUpper()
    $currentName = $_.Name.Trim().ToUpper()

    # dacă Name este diferit de SamAccountName -> păstrăm
    if ($currentName -ne $currentSam) {
        return $true
    }

    # căutăm dacă există alt record cu același SamAccountName
    # dar cu un nume diferit
    $hasRealName = $allResults | Where-Object {

        $_.SamAccountName.Trim().ToUpper() -eq $currentSam -and
        $_.Name.Trim().ToUpper() -ne $currentSam

    } | Select-Object -First 1

    return (-not $hasRealName)
}

# ===============================================================---

# ================== CLEAN DUPLICATES ==================
$cleanResults = $allResults |
    Sort-Object Group, Name, SamAccountName -Unique

$cleanResultsName = $allResults |
	Sort-Object Name -Unique

$cleanResultsSamAccountName = $allResults |
	Sort-Object SamAccountName -Unique    

# ================== UNIQUE NAMES ==================
$cleanResultsName = $cleanResults |
    Select-Object -ExpandProperty Name |
    Sort-Object -Unique |
    ForEach-Object {

        [PSCustomObject]@{
            Name = $_
        }
    }

# ===========================================
# ================== FILE 4 - CU BANCHE ==================

$cleanResultsWithBanche = $cleanResults | ForEach-Object {

    $sam = ""

    if ($_.SamAccountName) {
        $sam = $_.SamAccountName.Trim().ToUpper()
    }

    $banche = ""

    if ($bancheMap.ContainsKey($sam)) {
        $banche = $bancheMap[$sam]
    }

    [PSCustomObject]@{
        Group          = $_.Group
        Name           = $_.Name
        SamAccountName = $_.SamAccountName
        SourceFile     = $_.SourceFile
        Banche         = $banche
    }
}
# ==========================    
    
# ================ UNIQUE SamAccountName  ===================
$cleanResultsSamAccountName = $cleanResults |
    Select-Object -ExpandProperty SamAccountName |
    Sort-Object -Unique |
    ForEach-Object {

        [PSCustomObject]@{
            SamAccountName = $_
        }
    }    


# ================== EXPORT =====================
$result = @{
    Dettaglio     = @($cleanResults)
    UniqueNames   = @($cleanResultsName)
    UniqueSAM     = @($cleanResultsSamAccountName)
    NamesBanche   = @($cleanResultsWithBanche)
}

$result | ConvertTo-Json -Depth 10 -Compress

'''

# Creeaza fisierul PS1
with open("gruppi_standard.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

# Ruleaza scriptul PowerShell




# Run the created PowerShell file
# Use -ExecutionPolicy Bypass to ensure the script runs regardless of local restrictions
#subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "run_me.ps1"])

# CREARE FISIER EXCEL!!!!

import subprocess
import pandas as pd
import json
import os

# ... aici tot codul actual ...

result = subprocess.run(
    [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-File", "gruppi_standard.ps1"
    ],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

"""
# verificare dac citeste json powershell
print("Return code:", result.returncode)
print("STDOUT length:", len(result.stdout) if result.stdout else 0)
print("STDERR:")
print(result.stderr)
"""

# -------------------- 
if result.returncode != 0:
    raise Exception(result.stderr)

# Citirea JSON
data = json.loads(result.stdout)


# ceva debug 

#print(data.keys())


# Crearea DataFrame-urilor
detail_df = pd.DataFrame(data["Dettaglio"])

unique_names_df = pd.DataFrame(data["UniqueNames"])

unique_sam_df = pd.DataFrame(data["UniqueSAM"])

names_banche_df = pd.DataFrame(data["NamesBanche"])


# =====================================================
# # CREARE EXCEL DIRECT DIN DATELE RETURNATE DE POWERSHELL
# =====================================================

with open("Parametri.json", encoding="utf-8") as f:
    config = json.load(f)

basePath = os.path.join(
    config["Source_dir"],
    config["Report_dir"]
)

outputPath = os.path.join(
    basePath,
    "gruppi"
)

#-----
adUsersFile = os.path.join(
    basePath,
    "output-1",
    config["AD_Users_Results_attivi"]
)
# -----

excelFile = os.path.join(
    outputPath,
    "Licenze_Office_STD_AD_RESULTS_ATTIVI E UNIQUE NAMES e Match AD.xlsx"
)

#---------------------
# ==========================================
# MATCH UNIQUE NAMES vs AD USERS
# ==========================================

unique_names_df = pd.DataFrame(data["UniqueNames"])

ad_users_df = pd.read_csv(
    adUsersFile,
    sep="|",
    skiprows=1      # ignoră linia sep=|
)

# normalizare pentru comparare fără diferență de registru
unique_names_df["Name_norm"] = (
    unique_names_df["Name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

ad_users_df["Name_norm"] = (
    ad_users_df["Name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

# LEFT JOIN (echivalent VLOOKUP)
match_df = unique_names_df.merge(
    ad_users_df[
        ["Name_norm", "Principal Name", "OU_01"]
    ],
    on="Name_norm",
    how="inner"
)

match_df["FoundInAD"] = match_df["Principal Name"].notna()

match_df = match_df[match_df["FoundInAD"] == True]

# redenumim coloana OU_01
match_df.rename(
    columns={"OU_01": "Banche"},
    inplace=True
)

# stergem coloana FoundInAD
match_df.drop(
     columns=["FoundInAD"],
     inplace=True
)


# eliminăm coloana tehnică
match_df.drop(columns=["Name_norm"], inplace=True)
# ---------------------------

with pd.ExcelWriter(excelFile, engine="openpyxl") as writer:

    detail_df.to_excel(
        writer,
        sheet_name="Dettaglio",
        index=False
    )

    unique_names_df.to_excel(
        writer,
        sheet_name="Unique Names",
        index=False
    )

    unique_sam_df.to_excel(
        writer,
        sheet_name="Unique SAM",
        index=False
    )

    names_banche_df.to_excel(
        writer,
        sheet_name="Names Banche",
        index=False
    )

    match_df.to_excel(
        writer,
        sheet_name="Match AD",
        index=False
    )

print(f"Excel generat: {excelFile}")
