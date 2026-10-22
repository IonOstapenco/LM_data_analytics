import subprocess

ps_script = r'''
# ================== TOATE GRUPURILE ==================
$groups = @(
# ==== PRD ====
"ctx_127_sdb_prd",
"ctx_093_sdb_prd",
"ctx_058_sdb_prd",
"ctx_003_sdb_prd",
"ctx_016_tta_prd",
"ctx_008_sdb_prd",
"ctx_015_sdb_prd",
"ctx_380_sdb_prd",
"ctx_015_opm_prd",
"ctx_015_daisy_prd",
"ctx_015_rdbcruffcg_prd",
"ctx_015_sdbtoolscg_prd",
"ctx_342_sdb_prd",
"ctx_016_sdb_prd",
"ctx_016_opm_prd",
"ctx_016_zeb_rec_prd",
"ctx_016_sdbtoolscg_prd",
"ctx_016_ccm_prd",
"ctx_016_zeb_cif_prd",
"ctx_016_zeb_cost_prd",
"ctx_016_zeb_egk_prd",
"ctx_019_sdb_prd",
"ctx_283_sdb_prd",
"ctx_023_ccm_prd",
"ctx_023_sdb_prd",
"ctx_813_sdb_prd",
"ctx_883_sdb_prd",
"ctx_023_opm_prd",
"ctx_026_sdb_prd",
"ctx_392_sdb_prd",
"ctx_029_sdb_prd",
"ctx_029_tta_prd",
"ctx_539_zeb_egk_prd",
"ctx_539_opm_prd",
"ctx_539_ccm_prd",
"ctx_539_preccm_prd",
"ctx_352_sdb_prd",
"ctx_366_sdb_prd",
"ctx_388_sdb_prd",
"ctx_743_sdb_prd",
"ctx_575_sdb_prd",
"ctx_712_sdb_prd",
"ctx_874_sdb_prd",
"ctx_737_sdb_prd",
"ctx_078_sdb_prd",
"ctx_075_sdb_prd",
"ctx_079_sdb_prd",
"ctx_270_sdb_prd",
"ctx_320_sdb_prd",
"ctx_691_sdb_prd",
"ctx_832_sdb_prd",
"ctx_297_rdbcruffcg_prd",
"ctx_297_sdbtoolscg_prd",
"ctx_688_rdbcruffcg_prd",
"ctx_688_sdbtoolscg_prd",
"ctx_782_rdbcruffcg_prd",
"ctx_034_sdb_prd",
"ctx_036_sdb_prd",
"ctx_041_sdb_prd",
"ctx_045_sdb_prd",
"ctx_046_cam_prd",
"ctx_046_sdb_prd",
"ctx_046_obj_prd",
"ctx_046_ccm_prd",
"ctx_046_preccm_prd",
"ctx_047_sdb_prd",
"ctx_047_opm_prd",
"ctx_102_sdb_prd",
"ctx_818_sdb_prd",
"ctx_048_sdb_prd",
"ctx_058_ccm_prd",
"ctx_319_sdb_prd",
"ctx_058_tta_prd",
"ctx_072_sdb_prd",
"ctx_074_tta_prd",
"ctx_074_ccm_prd",
"ctx_074_sdb_prd",
"ctx_509_zeb_cost_prd",
"ctx_509_zeb_egk_prd",
"ctx_074_daisy_prd",
"ctx_075_opm_prd",
"ctx_079_obj_prd",
"ctx_088_opm_prd",
"ctx_088_sdb_prd",
"ctx_088_ccm_prd",
"ctx_089_opm_prd",
"ctx_089_sdb_prd",
"ctx_093_ccm_prd",
"ctx_103_sdb_prd",
"ctx_103_tta_prd",
"ctx_105_sdb_prd",
"ctx_110_rdbcruffcg_prd",
"ctx_110_sdbtoolscg_prd",
"ctx_121_sdb_prd",
"ctx_121_preccm_prd",
"ctx_121_xlcubed_prd",
"ctx_121_zeb_egk_prd",
"ctx_121_argo_prd",
"ctx_122_xlcubed_prd",
"ctx_122_sdb_prd",
"ctx_127_preccmdataentry_prd",
"ctx_127_preccmscrivanie_prd",
"ctx_203_sdb_prd",
"ctx_351_sdb_prd",
"ctx_269_sdb_prd",
"ctx_270_opm_prd",
"ctx_711_sdbtoolscg_prd",
"ctx_320_web_prd",
"ctx_347_sdb_prd",
"ctx_352_opm_prd",
"ctx_346_newlife_prd",
"ctx_366_ccm_prd",
"ctx_368_sdb_prd",
"ctx_372_sdb_prd",
"ctx_377_sdb_prd",
"ctx_379_sdb_prd",
"ctx_380_opm_prd",
"ctx_384_tta_prd",
"ctx_384_sdb_prd",
"ctx_395_sdb_prd",
"ctx_750_sdb_prd",
"ctx_399_ccm_prd",
"ctx_399_sdb_prd",
"ctx_399_tta_prd",
"ctx_523_preccmscrivanie_prd",
"ctx_523_sdb_prd",
"ctx_529_obj_prd",
"ctx_529_ccm_prd",
"ctx_529_preccm_prd",
"ctx_539_sdb_prd",
"ctx_567_sdb_prd",
"ctx_578_sdbtoolscg_prd",
"ctx_586_sdbtoolscg_prd",
"ctx_689_sdbtoolscg_prd",
"ctx_691_preccm_prd",
"ctx_711_rdbcruffcg_prd",
"ctx_725_rdbcruffcg_prd",
"ctx_725_sdbtoolscg_prd",
"ctx_737_preccmdataentry_prd",
"ctx_737_preccmscrivanie_prd",
"ctx_743_ccm_prd",
"ctx_759_sdb_prd",
"ctx_767_sdb_prd",
"ctx_782_sdbtoolscg_prd",
"ctx_785_rdbcruffcg_prd",
"ctx_785_sdbtoolscg_prd",
"ctx_789_rdbcruffcg_prd",
"ctx_789_sdbtoolscg_prd",
"ctx_798_rdbcruffcg_prd",
"ctx_798_sdbtoolscg_prd",
"ctx_808_rdbcruffcg_prd",
"ctx_808_sdbtoolscg_prd",
"ctx_818_ccm_prd",
"ctx_832_tta_prd",
"ctx_834_rdbcruffcg_prd",
"ctx_834_sdbtoolscg_prd",
"ctx_836_rdbcruffcg_prd",
"ctx_836_sdbtoolscg_prd",
"ctx_840_rdbcruffcg_prd",
"ctx_840_sdbtoolscg_prd",
"ctx_840_ccmcg_prd",
"ctx_851_rdbcruffcg_prd",
"ctx_842_sdb_prd",
"ctx_850_sdbtoolscg_prd",
"ctx_850_rdbcruffcg_prd",
"ctx_851_sdbtoolscg_prd",
"ctx_857_rdbcruffcg_prd",
"ctx_857_sdbtoolscg_prd",
"ctx_873_sdb_prd",
"ctx_874_preccm_prd",
"ctx_879_zeb_cost_prd",
"ctx_879_zeb_egk_prd",
"ctx_879_zeb_rec_prd",
"ctx_879_sipert_prd",
"ctx_879_sdb_prd",
"ctx_879_tta_prd",
"ctx_881_sdb_prd",
"ctx_881_ccm_prd",
"ctx_881_tta_prd",
"ctx_881_sdbtoolscg_prd",
"ctx_883_zeb_cif_prd",
"ctx_883_zeb_cost_prd",
"ctx_883_zeb_egk_prd",
"ctx_883_zeb_rec_prd",
"ctx_893_sdbtoolscg_prd",
"ctx_918_rdbcruffcg_prd",
"ctx_918_sdbtoolscg_prd",
"ctx_921_sdbtoolscg_prd",

# ==== COL ====
"ctx_015_opm_col","ctx_016_opm_col","ctx_539_opm_col",
"ctx_074_daisy_col","ctx_088_opm_col","ctx_089_opm_col",
"ctx_270_opm_col","ctx_346_newlife_col",

# ==== ADS ====
"ctx_127_sdb_ads",
"ctx_015_opm_ads",
"ctx_016_tta_ads",
"ctx_016_opm_ads",
"ctx_016_sdb_ads",
"ctx_023_sdb_ads",
"ctx_023_opm_ads",
"ctx_029_sdb_ads",
"ctx_029_tta_ads",
"ctx_539_opm_ads",
"ctx_078_sdb_ads",
"ctx_047_opm_ads",
"ctx_047_sdb_ads",
"ctx_047_tta_ads",
"ctx_058_tta_ads",
"ctx_058_sdb_ads",
"ctx_074_tta_ads",
"ctx_075_opm_ads",
"ctx_079_sdb_ads",
"ctx_088_opm_ads",
"ctx_088_sdb_ads",
"ctx_089_opm_ads",
"ctx_089_sdb_ads",
"ctx_093_sdb_ads",
"ctx_103_sdb_ads",
"ctx_103_tta_ads",
"ctx_121_sdb_ads",
"ctx_121_preccm_ads",
"ctx_121_xlcubed_ads",
"ctx_122_sdb_ads",
"ctx_122_xlcubed_ads",
"ctx_270_opm_ads",
"ctx_270_sdb_ads",
"ctx_352_opm_ads",
"ctx_380_sdb_ads",
"ctx_380_opm_ads",
"ctx_399_tta_ads",
"ctx_399_sdb_ads",
"ctx_523_sdb_ads",
"ctx_539_sdb_ads",
"ctx_567_sdb_ads",
"ctx_575_sdb_ads",
"ctx_832_tta_ads",
"ctx_857_sdbtoolscg_ads",
"ctx_879_sdb_ads",
"ctx_879_tta_ads",
"ctx_881_sdb_ads",
"ctx_881_tta_ads"

)

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
# ================================================
# reconstruim lista FINALĂ de grupuri
$groups = foreach ($base in $validBases) {

    # excepție specială
    if ($base -eq "ctx_047_tta") {
        "${base}_ads"
    }
    else {
        "${base}_prd"
    }
}
# ================== PATH ==================
$basePath   = "C:\License_Management\Report_202605" # fisier de baza
$outputPath = "C:\License_Management\Report_202605\all_in_one" # mapa de output
$outFile    = Join-Path $outputPath "Licenze Office STD (solo_PRD_EXCEPTIE _ctx_047_tta_ads).csv"
$outFile2   = Join-Path $outputPath "Licenze Office STD (solo_PRD_EXCEPTIE _ctx_047_tta_ads)_Unique Names.csv"
$outFile3   = Join-Path $outputPath "Licenze Office STD_(solo_PRD_EXCEPTIE _ctx_047_tta_ads)_Unique SamAccountNames.csv"


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
                    SourceFile     = $currentFile   #  util pentru debug
                }
            }
        }
    }
}

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
$cleanResults |
    Export-Csv $outFile -NoTypeInformation -Delimiter ";"

$cleanResultsName |
    Export-Csv $outFile2 -NoTypeInformation -Delimiter ";"

$cleanResultsSamAccountName |
    Export-Csv $outFile3 -NoTypeInformation -Delimiter ";"  


Write-Host " Gata! Fisier generat: $outFile"
Write-Host " Gata! Fisier generat: $outFile2"
Write-Host " Gata! Fisier generat: $outFile3"
'''

# Creeaza fisierul PS1
with open("run_me_STD.ps1", "w", encoding="utf-8") as f:
    f.write(ps_script)

# Ruleaza scriptul PowerShell


subprocess.run([
    "powershell.exe",
    "-ExecutionPolicy", "Bypass",
    "-File", "run_me_STD.ps1"
])

# Run the created PowerShell file
# Use -ExecutionPolicy Bypass to ensure the script runs regardless of local restrictions
#subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "run_me.ps1"])