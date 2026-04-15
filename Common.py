
import os
import json
import sys


#
# Caricamente dei parametri di funzionamento.
#

with open('Parametri.json') as f: 
    data = f.read() 
pr = json.loads(data) 

#
# Definizione di alcune variabili globali
#

cs = pr["Separa_car"]  # Carattere separatori dei campi per i file in output
dr = pr["Separa_dir"]  # Carattere separatore per la creazione dei nomi completi dei file

start_path = pr["Source_dir"] + pr["Separa_dir"] + pr["Report_dir"] 
out_path = start_path + dr + pr["Output_dir"]
exc_path = pr["Source_dir"] + pr["Separa_dir"] + pr["Exclude_dir"]

Minimo_lic_Win_vm = int(pr.get("Minimo_lic_Win_vm", 1))
Minimo_lic_Win_fs = int(pr.get("Minimo_lic_Win_fs", 1))
Minimo_lic_SQL_vm = int(pr.get("Minimo_lic_SQL_vm", 1))
Minimo_lic_SQL_fs = int(pr.get("Minimo_lic_SQL_fs", 1))

files = []

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def list_files_scandir(path, file_pattern, end):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                t = entry.name.lower()
                ndx = t.find(file_pattern.lower()) 
                if ( ndx > -1 ):
                    e = len(end)
                    if ( entry.name[-e:] == end ):
                        files.append(entry.path)
            elif entry.is_dir():
                list_files_scandir(entry.path, file_pattern, end)

#------------------------------------------------------------------------------

def togli_apici(frase, sep):
    t = list(frase)
    lt = len(t)
    cs = pr["Separa_car"]
    z = 0
    for x in range(0, lt):
        if ( t[x] == '"' ):
            if ( z == 0 ):
                z = 1
            else:
                z = 0
        else:
            if ( (t[x] == sep) and (z == 0) ):
                t[x] = cs
    return ''.join(t)

#------------------------------------------------------------------------------

def togli_dominio(nomesrv):
    x = nomesrv.find('.')
    if ( x == -1 ):
        return [nomesrv, '']
    l = []
    l.append(nomesrv[:x])
    l.append(nomesrv[x + 1:])
    return l

#------------------------------------------------------------------------------

def carica_dati(input_file, dati, posizione):
    
    mesg = "Elemento [{}]"
    mes1 = "File in caricamento: [{}]"

#    y = [out_path, file]
#    input_file = dr.join(y)
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(input_file))
    print("----------------------------------------------------------------\n")
    f = open(input_file, "r")
    Linee = f.readlines() 
    i = 0

    del Linee[0]
    del Linee[0]
    for linea in Linee:
        print('\r', mesg.format(i), end='', flush=True)
        a = str(linea).rstrip('\n')
        y = a.split(cs)
        nome = y[posizione]
        dati[nome] = y
        i += 1 
    print("\n")

#------------------------------------------------------------------------------

def scrivi_dati(outfile, lista_campi, lista):

    mesg = "Elemento [{}]"
    mes1 = "File in caricamento: [{}]"

    y = [out_path, pr[outfile]]
    output_file = dr.join(y)
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(output_file))
    print("----------------------------------------------------------------\n")
    f = open(output_file, "w")
    f.write("sep=" + cs + "\n")
    print("\n\nScrittura file " + output_file)
    riga = cs.join(list(lista_campi.keys()))
    f.write(riga + "\n")

    n = len(lista)
    for j in range(0, n):
        print('\r', mesg.format(j), end='', flush=True)
        riga = cs.join(map(str, lista[j].dati))
        f.write(riga + "\n")
    f.close()
    print ("\n>-----------------------------------------------------------<\n")

#------------------------------------------------------------------------------

def cerca_elemento(elenco, token, modo, case, start):

#
# Cerca, solo stringhe, token all'interno del vettore:
#   --> modo =-1 almeno un elemento dell'elenco deve essere contenuto nel token
#   --> modo = 0 ricerca esatta: il token deve corrispondere ad almeno un elemento dell'elenco; 
#   --> modo = 1 contenuto: il token deve essere contenuto in almeno un elemento dell'elenco.
#
#   --> case = 0 confronto case sensitive
#   --> case = 1 confronto case insensitive
#
#   --> start = -1 parte la ricerca dall'inizio
#   --> start = <numero> : parte la ricerca da quell'indice.
#
# Ritorna l'indice al quale è stato trovato il token secondo il modo indicato. 
# Ritorna -1 se il token non è stato trovato.

    n_elenco = len(elenco)

    if start < 0:
        start = 0
    
    if start >= n_elenco:
        return -1
    
    if case:
        tkn = token.lower()
    else:
        tkn = token

    if modo == 0:       # Ricerca esatta: il token deve corrispondere ad almeno un elemento dell'elenco
        for i in range(start, n_elenco):
            if case:
                str = elenco[i].lower()
            else:
                str = elenco[i]
            if tkn == str:
                return i

    if modo == 1:        # il token deve essere contenuto in almeno un elemento dell'elenco.
        for i in range(start, n_elenco):
            if case:
                str = elenco[i].lower()
            else:
                str = elenco[i]
            if str.find(tkn) >= 0:
                return i

    if modo == -1:
        for i in range(start, n_elenco):
            if case:
                str = elenco[i].lower()
            else:
                str = elenco[i]
            if str.find(';') >= 0:
                tmp = str.split(';')
                trova = 1
                for s in tmp:
                    if tkn.find(s) < 0:     # E' sufficiente che una sola parola dell'elemento dell'elenco[i] non sia presente in tkn
                        trova = 0           #    per far sì che tkn sia considerato 'NON TROVATO'
                        break
                if trova == 1:
                    return i
            else:
                if tkn.find(str) >= 0:
                    return i
    return -1

#------------------------------------------------------------------------------

def check_outdir(directory_name):  # --> functia de verificarea existentei mapei de output, si creaza daca nu este
    try:
        os.makedirs(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def trova_separa(riga):
    if riga.find(',') > -1:
        return ','
    if riga.find(';') > -1:
        return ';'
    return '|'

# --------------------------------------------------------------------
# functia de stergere BOM si uteff -- funzione di normalizazzione i input file

# funzione per rimuovere il BOM dalle stringhe
# f-tie de stergere BOM
def norm(s):
    if s is None:
        return ""
    return s.replace("\ufeff", "").strip()