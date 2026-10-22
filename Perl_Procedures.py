import subprocess

import os

comenzi = [
    "cd \License_Management",
   "cd \License_Management\Bin-2",
   "dir",

 r"C:\Strawberry\perl\bin\perl.exe -w merge_AD_users.pl"
]

## Concatena i comandi con " & " per eseguirli uno dopo l'altro

comenzi_cmd = " & ".join(comenzi)

## /k = lascia CMD aperto dopo l'esecuzione, /c = chiudilo
os.system(f'start cmd /k "{comenzi_cmd}"')