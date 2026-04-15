# Python classi dati BIGFIX

import Common as cm

#------------------------------------------------------------------------------
class c_BGFX:
    def __init__(self, nome, attributo):
        self.nome = nome
        self.dati = attributo



BGFX = []
BGFX_field = {"Stato": 0,
              "Nome computer": 1,
              "Sistema operativo": 2,
              "Nome DNS": 3,
              "AIX Full OS Level": 6,
              "Technology Level": 7,
              "NumeroCPU": 10,
              "NumeroSocket": 12,
              "License Type": 13,
              "Computer Type": 14,
              "Java Output": 15,
              "JavaPath": 16,
              "JavaVersion": 17,
              "Tipo di computer": 18,
              "Core partizione": 19,
              "Core server": 21,
              "Stringa marchio processore": 22,
              "Vendor": 23,
              "Marchio": 24,
              "Tipo": 25,
              "Modello": 26,
              "PVU per core": 27,
              "Valore PVU modificato": 28,
              "Valore PVU predefinito": 29,
              "Fattore core Oracle": 30,
              "Socket attivi del server": 33,
              "Domain": 34,
              "Nome cluster": 35,
              "Core cluster": 36,
              "CPU": 37,
              "Nome host padre": 38,
              "Last Report Time": 40,
              "Tipo di server": 41
             }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


print("Procedura per la elaborazione dei dati da BigFix.")

cm.check_outdir(cm.out_path)

#
# Cerco il file più recente in base al pattern indicato in Parametri.json
#
file_pattern = cm.pr["BGFX_Pattern"]
cm.list_files_scandir(cm.start_path, file_pattern, cm.pr["Extension_end"])

temp = sorted(cm.files, reverse=True)
print("Elaborazione file " + temp[0])

fc = open(temp[0], "r")

i = 0       # Questo contatore ho il solo scopo di visualizzare i susseguirsi dei record in elaborazione
j = 0       # Questo serve per poter scorrere la lista di oggetti per verficiare che non ce ne sia 
            # presente uno che contenga già le informazioni della riga in elaborazione.
t = []      # Lista che contiene la riga del file elaborata e con le informazioni elencate in CMDB_field
nomi = []   # Lista di appoggio per verificare se quel server è già stato elaborato.
nomi_doppi= [] 
mesg = "Elemento [{}]"
for x in fc:
    print('\r', mesg.format(i), end='', flush=True)
    if ( i < 1 ):
        i += 1
        continue
    separa = cm.trova_separa(x)
    tmp = cm.togli_apici(x, separa)
#
# Ora la riga non ha più il separatore di campo 
# che può essere confuso se all'interno di doppi apici
#
    y = tmp.split(cm.cs)
    t = []
    for c in BGFX_field:
         if c == "Nome computer": 
            t.append(str(y[BGFX_field[c]]).lower())
         else:
            t.append(y[BGFX_field[c]])
#
# La lista 't' contiene solo i campi che sono stati selezionati e 
# elencati in CMDB_field
#
    nome = t[BGFX_field["Nome computer"]].lower()

    if ( nome in nomi ):
        nomi_doppi.append(nome)
    else:
        nomi.append(nome)
        z = c_BGFX(nome, t)
#
# 'z' è l'oggetto che è stato istanziato dalla classe c_CMDB e che
# viene memorizzato nella lista di oggetti 'CMDB'
#
        BGFX.append(z)
    i += 1

#
# ------------------------------------------------------- fine ciclo sulle righe
#

#
# Scrittura del file ICTG-HW.csv
#

y = [cm.out_path, cm.pr["OUT_BGFX"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("sep=" + cm.cs + "\n")

print("\n\nScrittura file " + output_file)

riga = cm.cs.join(BGFX_field)

f.write(riga + "\n")

n = len(BGFX)
for j in range(0, n):
    print('\r', mesg.format(j), end='', flush=True)
    riga = cm.cs.join(map(str, BGFX[j].dati))
    f.write(riga + "\n")
f.close()

#
# Valutare se scrivere il file contenente i nomi doppi rilevati in Bigfix.
#

