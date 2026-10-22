# Verifica presenza di righe 'interrotte' nei report scaricati da CMDB e da BigFix.

import Common as cm
import sys

f_input = [
    "Asset Server (ALL)",  
    "Asset Software (ALL -", 
    "Asset Client (ALL)-", 
    "Asset ServerDismessi (ALL)-", 
    "Asset Database (ALL)-",
    "ICTG-0-classificazione-software-", 
    "ICTG-0-inventario-hardware-",
    "ICTG-0-database-oracle-"
]

for f in f_input:
    cm.files = []
    cm.list_files_scandir(cm.start_path, f, cm.pr["Extension_end"])

    temp = sorted(cm.files, reverse=True)
    print("Elaborazione file " + temp[0])

    fc = open(temp[0], "r")
    Linee = fc.readlines()
    fc.close()
    b = 0
    nLinee = len(Linee)
    j = 0
    while (j < nLinee):
        try:
            if len(Linee[j]) < 5:
                del Linee[j]
                nLinee = len(Linee)
                j += 1
                continue
        except:
            print(j)
            sys.exit()
        riga = Linee[j].rstrip('\n')
        l = list(riga)
        lriga = len(l)
        a = 0
        for i in range(0, lriga):
            if ( l[i] == '"' ):
                if ( a == 0):
                    a = 1
                else:
                    a = 0
        if ( a == 1 ):
            Linee[j] = riga + Linee[j+1]
            del Linee[j+1]
            nLinee = len(Linee)
            b = 1
        j += 1

    if b == 1:
        fm = temp[0]
        fc = open(fm, "w")
        for l in Linee:
            fc.write(l)
        fc.close()
        print("Riscritto il file:" + fm)

