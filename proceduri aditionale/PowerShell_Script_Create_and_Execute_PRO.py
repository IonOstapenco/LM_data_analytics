import subprocess

ps_script = r'''
# ================== TOATE GRUPURILE ==================
$groups = @(
# ==== PRD ====
"ctx_581_cgl_fondpens_prd",
# ==== COL ====
# ==== ADS ====
"ctx_581_cgl_fondpens_ads"
)

# ================== PATH ==================
$basePath   = "C:\License_Management\Report_202606"
$outputPath = "C:\License_Management\Report_202606\all_in_one_test"
$outFile    = Join-Path $outputPath "grupe_name_samAccountName_FARA_DUPLICATE_PRO.csv"

New-Item -ItemType Directory -Path $outputPath -Force | Out-Null

# ================== CITIRE FILE ==================
$files = Get-ChildItem $basePath -Recurse -Filter AD-usersAndGroupsResult.csv

# ================== PROCESARE ==================
$allResults = foreach ($file in $files) {

    $currentFile = $file.FullName

    foreach ($group in $groups) {

        Select-String -Path $currentFile -Pattern $group -CaseSensitive:$false |
        ForEach-Object {

            $cols = $_.Line -split ";"

            if ($cols.Count -ge 6) {
                [PSCustomObject]@{
                    Group          = $group
                    Name           = $cols[4]
                    SamAccountName = $cols[5]
                    SourceFile     = $currentFile
                }
            }
        }
    }
}

# ================== CLEAN DUPLICATES ==================
$cleanResults = $allResults |
    Sort-Object Group, Name, SamAccountName -Unique

# ================== EXPORT ==================
$cleanResults |
    Export-Csv $outFile -NoTypeInformation -Delimiter ";"

Write-Host "Gata! Fisier generat: $outFile"
'''

# Creeaza fisierul PS1
with open("run_me_PRO.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

# Ruleaza scriptul PowerShell


subprocess.run([
    "powershell.exe",
    "-ExecutionPolicy", "Bypass",
    "-File", "run_me.ps1"
])

# Run the created PowerShell file
# Use -ExecutionPolicy Bypass to ensure the script runs regardless of local restrictions
#subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "run_me.ps1"])