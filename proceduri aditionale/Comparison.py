import os
import difflib
import pdfplumber
import pandas as pd
from docx import Document

# ==========================================================
# INPUT (hardcodat)
# ==========================================================


# C:\Users\crme240\OneDrive - ION\Desktop\CompareDocs\4. IAASM_template.pdf
# C:\Users\crme240\OneDrive - ION\Desktop\CompareDocs\5. IAASSS_template.pdf
FILE1 = r"C:\Users\crme240\OneDrive - ION\Desktop\CompareDocs\Annex 2 - Accordo Oracle Partnernetwork per il Livello 1.pdf"
FILE2 = r"C:\Users\crme240\OneDrive - ION\Desktop\CompareDocs\OPN_Agreement_v100119_IT_ITA_v3 (4).pdf"

OUTPUT = r"C:\Users\crme240\OneDrive - ION\Desktop\CompareDocs\Differences 2.xlsx"

# ==========================================================
# Citire PDF
# ==========================================================

def read_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            t = page.extract_text()

            if t:
                text += t + "\n"

    return text


# ==========================================================
# Citire DOCX
# ==========================================================

def read_docx(file):

    doc = Document(file)

    text = []

    for p in doc.paragraphs:
        text.append(p.text)

    return "\n".join(text)


# ==========================================================
# Citire automata
# ==========================================================

def load_document(file):

    ext = os.path.splitext(file)[1].lower()

    if ext == ".pdf":
        return read_pdf(file)

    elif ext == ".docx":
        return read_docx(file)

    else:
        raise Exception("Format nesuportat")


# ==========================================================
# MAIN
# ==========================================================

text1 = load_document(FILE1)
text2 = load_document(FILE2)

lines1 = text1.splitlines()
lines2 = text2.splitlines()

diff = difflib.ndiff(lines1, lines2)

rows = []

for line in diff:

    if line.startswith("- "):

        rows.append({
            "Status": "Sters",
            "Continut": line[2:]
        })

    elif line.startswith("+ "):

        rows.append({
            "Status": "Adaugat",
            "Continut": line[2:]
        })

df = pd.DataFrame(rows)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

df.to_excel(OUTPUT, index=False)

print("Raport generat:")
print(OUTPUT)