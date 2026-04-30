import Common as cm
import re

print("Procedura per la elaborazione dei dati da Active Directory - AD-usersAndGroupsResult.csv.")

cm.check_outdir(cm.out_path)

# ===============================
# SET-uri (fără duplicate)
# ===============================
USER_GROUP_PRO = set()
USER_GROUP_STD = set()

GROUP_STD = set()
GROUP_PRO = set()

# ===============================
# Citire lista grupuri
# ===============================
GroupList = cm.start_path + cm.dr + "Lista gruppi Office_FLEXERA.txt"

with open(GroupList, "r") as fc:
    for linea in fc:
        a = linea.strip()
        b = a.split(cm.cs)

        group_name = b[0].strip().lower()
        group_type = b[1].strip().upper().replace('\ufeff', '')

        if group_type == 'STD':
            GROUP_STD.add(group_name)
        else:
            GROUP_PRO.add(group_name)

print("Grupuri STD:", GROUP_STD)
print("Grupuri PRO:", GROUP_PRO)

# ===============================
# Regex filtre
# ===============================
exclude_patterns_Gruppi = [
    re.compile(r'099', re.IGNORECASE),
    re.compile(r'ctx_033', re.IGNORECASE),
    re.compile(r'ctx_870', re.IGNORECASE)
]

exclude_patterns_SamAccountName = [
    re.compile(r'cr', re.IGNORECASE),
    re.compile(r'cre', re.IGNORECASE)
]

# ===============================
# Căutare fișiere
# ===============================
cm.list_files_scandir(cm.start_path, cm.pr["AD_User_Group_Pattern"], cm.pr["Extension_end"])

mesg = "Elemento [{}/{}]"

# ===============================
# Procesare fișiere
# ===============================
for w in cm.files:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"FILE: {w}")
    print("------------------------------------------------------------")

    with open(w, 'r') as fc:
        Linee = fc.readlines()

    del Linee[0]
    n = len(Linee)

    gioin = []
    i = 0

    for linea in Linee:
        print('\r', mesg.format(i, n-1), end='', flush=True)

        b = linea.replace("\x00", "").strip()
        if not b:
            i += 1
            continue

        separa = cm.trova_separa(b)
        tmp = cm.togli_apici(b, separa)
        y = tmp.split(cm.cs)

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
            continue

        a = y[2].strip().lower()  # GroupName
        u = y[5].strip().lower()  # SamAccountName

        # Filtre
        if any(p.search(u) for p in exclude_patterns_SamAccountName):
            i += 1
            continue

        if any(p.search(a) for p in exclude_patterns_Gruppi):
            i += 1
            continue

        # ===============================
        # AICI e cheia: set.add()
        # ===============================
        if a in GROUP_STD:
            USER_GROUP_STD.add((u, a))

        if a in GROUP_PRO:
            USER_GROUP_PRO.add((u, a))

        i += 1

# ===============================
# Statistici
# ===============================
print("\n+-------------------------------------------------------+")
print(f"PRO users: {len(USER_GROUP_PRO)}")

print("\n+-------------------------------------------------------+")
print(f"STD users: {len(USER_GROUP_STD)}")

# ===============================
# Scriere PRO
# ===============================
output_file = cm.dr.join([cm.out_path, cm.pr["FLEXERA_OUT_USER_PRO"]])

with open(output_file, "w") as f:
    f.write("sep=" + cm.cs + "\n")
    f.write("SamAccountName" + cm.cs + "GroupName\n")

    for u, a in sorted(USER_GROUP_PRO):
        f.write(u + cm.cs + a + "\n")

print("Scris:", output_file)

# ===============================
# Scriere STD
# ===============================
output_file = cm.dr.join([cm.out_path, cm.pr["FLEXERA_OUT_USER_STD"]])

with open(output_file, "w") as f:
    f.write("sep=" + cm.cs + "\n")
    f.write("SamAccountName" + cm.cs + "GroupName\n")

    for u, a in sorted(USER_GROUP_STD):
        f.write(u + cm.cs + a + "\n")

print("Scris:", output_file)