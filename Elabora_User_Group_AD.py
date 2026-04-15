import Common as cm
import re

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

USER_GROUP_PRO = []
USER_GROUP_STD = []

GROUP_STD = []
GROUP_PRO = []

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

print("Procedura per la elaborazione dei dati da Active Directory - AD-usersAndGroupsResult.csv.")

cm.check_outdir(cm.out_path)

#Încărcarea grupurilor care urmează să fie evaluate
# Caricamento dei gruppi da valutare
#
GroupList = cm.start_path + cm.dr + "Lista gruppi Office.txt"

fc = open(GroupList, "r")
Linee = fc.readlines()
for linea in Linee:
    a = str(linea).lower().rstrip('\n')
    b = a.split(cm.cs)
    if b[1] == 'std':
        GROUP_STD.append(b[0])
    else:
        GROUP_PRO.append(b[0])

# DEBUGGING: Afișăm grupurile încărcate
# DEBUGGINGȘ Visualizziamo i gruppi caricati
print("DEBUGGING: Afișăm grupurile încărcate")
print("Grupuri STD:", GROUP_STD)
print("Grupuri PRO:", GROUP_PRO)

#
# Cerco tutti i file in base al pattern indicato in Parametri.json
#
cm.list_files_scandir(cm.start_path, cm.pr["AD_User_Group_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}/{}]"
mes1 = "FILE:[{}]"

# Filtre pentru excluderea grupurilor
# Filtri per escludere dei gruppi
exclude_patterns_Gruppi = [
    re.compile(r'099', re.IGNORECASE),
    re.compile(r'ctx_033', re.IGNORECASE),
    re.compile(r'ctx_870', re.IGNORECASE)
]

# Filtre pentru excluderea SamAccountName
# Filtri per escludere SamAccountName
exclude_patterns_SamAccountName = [
    re.compile(r'cr', re.IGNORECASE),
    re.compile(r'cre', re.IGNORECASE)
]

for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(mes1.format(w))
    print("----------------------------------------------------------------\n")
    fc = open(w, 'r')
    Linee = fc.readlines()
    del Linee[0]  # elimino la prima riga che contiene l'intestazione delle colonne.
    n = len(Linee)
    #
    # ----- Il tracciato record viene desunto dai file estratti ed è sempre uguale.
    #
    # ----- Viene selezionato il nome del gruppo in terza colonna e 
    #       poi viene aggiunto uno per ogni volta che risulta presente in tal
    #       modo abbiamo il conteggio di quanti 'UserName' sono inseriti in quel gruppo
    #
    gioin = []
    i = 0
    for linea in Linee:
        print('\r', mesg.format(i, n-1), end='', flush=True)
        b = linea.replace("\x00", "")  # La riga di questi file è composta da caratteri esadecimali '0' ('\x00') intervalli ai normali caratteri ascii
        b = b.replace("\n", "")
        if b == '':
            i += 1
            continue  # Inoltre, ogni riga risulta essere una lista. Il primo elemento è composto da una riga vuota
        separa = cm.trova_separa(b)
        tmp = cm.togli_apici(b, separa)
        y = tmp.split(cm.cs)  # Separo i campi della riga
        if len(y) < 7:
            if not gioin:
                gioin = y
                i += 1
                continue
            else:
                y = gioin + y[1:]
                gioin = []
        if y[6] == 'Group':
            i += 1
            continue  # Se lo User è un gruppo lo ignoriamo
        a = str(y[2]).lower()  # GroupName
        u = str(y[5]).lower()  # SamAccountName
        # Debugging: Afisam valorile raw
        #print(f"Procesare: SamAccountName={u}, GroupName={a}")
        # Filtru pentru SamAccountName: excludem conturile care contin CR sau CRE
        ## Filtro per SamAccountName: escludiamo gli account che contengono CR o CRE
        if any(pattern.search(u) for pattern in exclude_patterns_SamAccountName):
            #print(f"Exclus din cauza SamAccountName: {u}")
            i += 1
            continue
        # Filtru pentru GroupName: excludem grupurile care contin 099, ctx_033, ctx_870
        #Filtro per GroupName: escludiamo gli gruppi che contegno 099, ctx_033, ctx_870
        if any(pattern.search(a) for pattern in exclude_patterns_Gruppi):
            #print(f"Exclus din cauza GroupName: {a}")
            i += 1
            continue
        if a in GROUP_STD:
            u_combined = u + cm.cs + a
            if u_combined not in USER_GROUP_STD:
                USER_GROUP_STD.append(u_combined)
              #  print(f"Adaugat in STD -- Aggiunto in STD: {u_combined}")
        if a in GROUP_PRO:
            u_combined = u + cm.cs + a
            if u_combined not in USER_GROUP_PRO:
                USER_GROUP_PRO.append(u_combined)
             #   print(f"Adaugat in PRO -- Aggiunto in PRO: {u_combined}")
        i += 1

n = len(USER_GROUP_PRO)
print("\n\n+-------------------------------------------------------+\n")
print(f"Per i gruppi indicati in 'List gruppi office PROPlus' risultano {n} utenti")

n = len(USER_GROUP_STD)
print("\n\n+-------------------------------------------------------+\n")
print(f"Per i gruppi indicati in 'List gruppi office Standard' risultano {n} utenti")

# --- Scrierea fișierului 'User_list_pro.csv'
# --- Scrittura del file 'User_list_pro.csv'
#
y = [cm.out_path, cm.pr["OUT_USER_PRO"]]
output_file = cm.dr.join(y)

f = open(output_file, "w")
f.write("sep=" + cm.cs + "\n")
print("\n\nScrittura file " + output_file)
riga = "SamAccountName" + cm.cs + "GroupName"
f.write(riga + "\n")

for g in USER_GROUP_PRO:
    f.write(g + "\n")
f.close()

# -- Scrierea fisierului 'User_list_std.csv.'
# --- Scrittura del file 'User_list_std.csv'
#
y = [cm.out_path, cm.pr["OUT_USER_STD"]]
output_file = cm.dr.join(y)

f = open(output_file, "w")
f.write("sep=" + cm.cs + "\n")
print("\n\nScrittura file " + output_file)
riga = "SamAccountName" + cm.cs + "GroupName"
f.write(riga + "\n")

for g in USER_GROUP_STD:
    f.write(g + "\n")
f.close()





#l = list(USER_GROUP.keys())
#
#n = len(USER_GROUP)
#for j in range(0, n):
#    print('\r', mesg.format(j, n-1), end='', flush=True)
#    riga = l[j] + cm.cs + USER_GROUP[l[j]]
#    f.write(riga + "\n")
#f.close()
#

#
# --- Scrittura del file 'Group_list.csv'
#

#y = [cm.out_path, cm.pr["OUT_GROUP"]]
#
#output_file = cm.dr.join(y)
#
#f = open(output_file, "w")
#f.write("sep=" + cm.cs + "\n")
#print("\n\nScrittura file " + output_file)
#riga = "GroupName" + cm.cs + "N. Users"
#f.write(riga + "\n")
#
#l = list(GROUP.keys())
#
#n = len(GROUP)
#for j in range(0, n):
#    print('\r', mesg.format(j, n-1), end='', flush=True)
#    riga = l[j] + cm.cs + GROUP[l[j]]
#    f.write(riga + "\n")
#f.close()        