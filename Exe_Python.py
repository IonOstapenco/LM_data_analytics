# Esecuzione delle procedure per la creazione delle 
#   tabelle HW, SW, WIN, SQL, Red Hat, JBoss, Rapid7
import json
import os
import sys
from datetime import datetime

now = datetime.now()
oggi = now.strftime("%Y-%m-%d %H:%M:%S")

with open('Sequenza.json') as f: 
    data = f.read() 
js = json.loads(data) 

continua = 0
nover = 0
start = 0
help = 0
if len(sys.argv) > 1:
    if ("[help]" in sys.argv):
        help = 1
        sys.argv.remove('[help]')
    if ("help" in sys.argv):
        help = 1
        sys.argv.remove('help')
    if ("noverifica" in sys.argv):
        nover = 1                       # Deve essere tralasciata la parte di verifica
        sys.argv.remove('noverifica')
    if ("[noverifica]" in sys.argv):
        nover = 1                       # Deve essere tralasciata la parte di verifica
        sys.argv.remove('[noverifica]')
    if ("[continua]" in sys.argv):      
        continua = 1
        sys.argv.remove('[continua]')
    if ("continua" in sys.argv):      
        continua = 1
        sys.argv.remove('continua')
    if ("[tutte]" in sys.argv):
        continua = 0
        sys.argv.remove('[tutte]')
    if ("tutte" in sys.argv):
        continua = 0
        sys.argv.remove('tutte')
    n = len(sys.argv)
    if n > 1:                           # Presuppongo che mi siano stati dati nomi di procedure da eseguire.
        continua = 1
        for x in range(1, n):
            if sys.argv[x] not in js:
                print("ERRORE: Procedura non presente in elenco: ", sys.argv[x])
                sys.exit(1)
            js[sys.argv[x]] = "X"
else:
    help = 1
if help:
    print(">vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv<")
    print(">                                                                               <")
    print("> Procedura per l'esecuzione delle elaborazioni Python                          <")
    print(">                                                                               <")
    print("> C:\\Python Exe_Python.py [parametri]                                          <")
    print(">                                                                               <")
    print("> Parametri: <nessuno>                                                          <")
    print(">             [help]   Visualizzazione della presente indicazione di aiuto      <")
    print(">                                                                               <")
    print("> Parametri: [tutte]: Esecuzione di tutte le procedure elencate nel file        <")
    print(">                     'Sequenza.json'. L'ordine di esecuzione è quello          <")
    print(">                     indicato nel file 'Sequesnza.json'                        <")
    print(">                                                                               <")
    print(">          [noverifica]: non viene eseguita la procedura di verifica dei report <")
    print(">                        estratti da CMDB e da BigFix. ('Verifica_report.py')   <")
    print(">                        L'esecuzione procede come per il parametro [tutte]     <")
    print(">                                                                               <")
    print(">          [continua]: la procedura tiene traccia dell'esecuzione delle         <")
    print(">                      procedure Python e, in caso di errore, riprende          <")
    print(">                      l'esecuzione dalla procedura che aveva rilevato l'errore <")
    print(">                                                                               <")
    print("> [Nome procedura, ...]: possono essere elencate le procedure per le quali      <")
    print(">                        debba essere necessario la riesecuzione. Possono       <")
    print(">                        essere elencate in qualsiasi ordine; saranno, comunque,<")
    print(">                        eseguite nell'ordine indicato in 'Sequenza.json'       <")
    print(">                                                                               <")
    print("> Se sono indicati nomi di procedure e viene, allo stesso tempo, indicato anche <")
    print("> il parametro [continua], i nomi delle procedure indicate saranno ignorati.    <")
    print(">                                                                               <")
    print("> Il parametro [noverifica] può essere indicato anche con uno degli altri       <")
    print("> parametri.                                                                    <")
    print(">                                                                               <")
    print("> Il file 'Sequenza.json' deve essere nella stessa directory in cui si trova    <")
    print("> 'Exe_Python.py'.                                                              <")
    print(">                                                                               <")
    print("> Esempio: Python Exe_Python.py noverifica                                      <")
    print(">                                                                               <")
    print(">          Questo comando esegue tutte le procedure elencate in 'Sequenza.json' <")
    print(">          evitando l'esecuzione della procedura di verifica dei report.        <")
    print(">                                                                               <")
    print(">^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<")
    sys.exit()

#
# ritengo che debbano essere rieseguite tutte le procedure dell'elenco.
#

l = list(js.keys())

if continua == 0:
    n = len(l)
    if nover > 0:
        js[l[0]] = "NO RUN"
        start = 1
    for j in range(start, n):
        js[l[j]] = "X"

for j in l:
    if js[j] != "X":
        continue
    cmd = "Python " + j
    print("\n+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+")
    print("  ===>> Eseguo " + cmd)
    print("+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+\n")
    err = os.system(cmd)
    print("\n+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+-=-+\n")
    if err > 0:
        print("Err: " + str(err))
        break
    js[j] = "Eseguito! [" + oggi + "]"

#with open("Sequenza.json", 'w') as jw:
#    json.dump(js, jw)

jw = open("Sequenza.json", 'w')
l = list(js.keys())
riga = "{\n"
jw.write(riga)
n = len(l) - 1
for k in range(0, n):
    riga = '"' + l[k] + '": "' + js[l[k]] + '",' + '\n'
    jw.write(riga)
riga = '"' + l[n] + '": "' + js[l[n]] + '"' + '\n'
jw.write(riga)
riga = "}\n"
jw.write(riga)
jw.close()