import subprocess

import os

comenzi = [
    "cd \License_Management",
   "cd \License_Management\Bin-2",
   "dir",
        "perl -w merge_bigfix.pl",
       "perl -w merge_vHost.pl",
       "perl -w merge_vInfo.pl",
      "perl -w merge_AD_cmdb.pl",
       "perl -w merge_AD_users.pl",
       "perl -w crea_tabella_hw.pl",
       "perl -w crea_tabella_sw.pl",
       "perl -w vrf_ctx.pl",
       "perl -w vrf_cmdb_err.pl",
      "perl -w vrf_dismessi.pl",
       "perl -w mostra_stat.pl",
       "perl -w mostra_stat.pl -f",
        "perl -w read_xlsx.pl -xlsx vms_citrix.xlsx",
      "perl -w crea_tab_db_oracle.pl",
    "perl -w merge_CTX_licenses.pl"
]

# Concatenăm comenzile cu " & " ca să fie rulate una după alta
comenzi_cmd = " & ".join(comenzi)

# /k = lasă CMD deschis după execuție, /c = îl închide
os.system(f'start cmd /k "{comenzi_cmd}"')