# 
# Elabora_CTX_User.py
#
# Procedura per la valutazione delle utenze abilitate al sistema Citrix suddividendole per cliente.
#
# Struttura del file contenente le informazioni degli utenti abilitati "ConteggioMensileCitrix_AAAAMMGG.csv"
#
# User ID,Cliente               ,Data ultima connessione
# BB01925,BANCA POPOLARE DI BARI,2025-01-23 07:27:30.000
#
# Se la data di ultima connessione è precedente a 90 giorni rispetto alla data di estrazione dei dati
# l'utenza viene eliminata.
#

import csv
import datetime as dt
import Common as cm

CTX_User = {}
CTX_field = {"User ID": 0,
             "Dominio": 1,
             "Last Logon": 2
            }

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Esecuzione procedura per il conteggio delle utenze abilitate al sistema Citrix")

cm.check_outdir(cm.out_path)

cm.list_files_scandir(cm.start_path, cm.pr["CTX_Users_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}]"
mes1 = "FILE:[{}]"

temp = sorted(cm.files, reverse=True)

fc = open(temp[0], 'r')

print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print(mes1.format(temp[0]))
print("----------------------------------------------------------------\n")

#
# Ricavo la data di estrazione dei dati dal nome del file
#

d_estrazione = temp[0][-12:-4]
a_estrazione = int(d_estrazione[:4])
m_estrazione = int(d_estrazione[4:6])
g_estrazione = int(d_estrazione[-2:])

data_estrazione = dt.datetime(a_estrazione, m_estrazione, g_estrazione)

n_citrix_users = 0
n_citrix_active = 0
i = 0
for riga in fc:
    print('\r', mesg.format(i), end='', flush=True)
    y = riga.split(',')
    u = y[CTX_field["User ID"]].lower()
    d = y[CTX_field["Dominio"]].lower()
    l = y[CTX_field["Last Logon"]]
    a_user = int(l[:4])
    m_user = int(l[5:7])
    g_user = int(l[8:10])

    data_user = dt.datetime(a_user, m_user, g_user)

    giorni_logon = data_estrazione - data_user
    n_giorni = giorni_logon.days


#daca mai putin de 90 zile, il atasam, inscriem, daca nu -- nu-l scriem
    if ( n_giorni <= 90 ):
        if ( d not in CTX_User ): 
            CTX_User[d] = []
        CTX_User[d].append(u)
        n_citrix_active += 1 # creste nr de useri activi

    n_citrix_users += 1 # creste nr de conturi citrix
    i += 1

# 
# FINE elaborazione righe
#

d_ctx = {}

for x in CTX_User:
    d_ctx[x] = len(CTX_User[x])

#
# scrittura file OUT_CTX_Users: "STAT_CTX_Users.txt"
#

y = [cm.out_path, cm.pr["OUT_CTX_Users"]]

output_file = cm.dr.join(y)

f = open(output_file, "w")

f.write("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><> CITRIX (SPLA)\n")
s = "{:,}".format(n_citrix_users)
s = s.replace(',', '.')
txt = f"Risultano definite {s} utenze con accesso all'infrastruttura Citrix.\n"
f.write(txt)

s = "{:,}".format(n_citrix_active)
s = s.replace(',', '.')
txt = f"Per il conteggio delle SAL Windows Remote Desktop risultano\n\n -> {s}\n\n utenze attive (Last Logon inferiore a 90 giorni)\n"
f.write(txt)

txt = "Per le utenze che risultano attive di seguito l'elenco dettagliato\n"
f.write(txt)
txt = "+--------+--------------------------------------------------------------+\n"
f.write(txt)

for x in sorted(d_ctx, key=d_ctx.get, reverse=True):
    s = "{:,}".format(d_ctx[x])
    s = s.replace(',', '.')
    txt = "| {:>6} | {:<60} |\n".format(s, x)
    f.write(txt)
txt = "+--------+--------------------------------------------------------------+\n"
f.write(txt)
f.close()

