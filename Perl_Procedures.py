import subprocess

import os

comenzi = [
    "cd \License_Management",
   "cd \License_Management\Bin-2",
   "dir",

 "perl -w merge_AD_users.pl"
]

## Concatena i comandi con " & " per eseguirli uno dopo l'altro
# Concatenăm comenzile cu " & " ca să fie rulate una după alta
comenzi_cmd = " & ".join(comenzi)

## /k = lascia CMD aperto dopo l'esecuzione, /c = chiudilo
# /k = lasă CMD deschis după execuție, /c = îl închide
os.system(f'start cmd /k "{comenzi_cmd}"')