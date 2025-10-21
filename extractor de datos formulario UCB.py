"""
extractor de datos formulario UCB
"""

#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pdfplumber
import re
import pandas as pd

def extract_data_from_pdf(pdf_path):
    # Abrir el PDF y extraer todo el texto
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"

    # Dividir el texto en líneas para facilitar la búsqueda de patrones
    lines = full_text.splitlines()

    # Diccionario donde almacenaremos la información extraída
    data = {}

    # Ejemplo 1: Extraer el nombre completo.
    # Se asume que tras el encabezado "DATOS PERSONALES" viene una línea con los nombres.
    for i, line in enumerate(lines):
        if "DATOS PERSONALES" in line:
            if i+1 < len(lines):
                data["Nombre Completo"] = lines[i+1].strip()
            break

    # Ejemplo 2: Extraer la fecha de nacimiento.
    # Se busca un patrón de fecha formado por día, mes y año.
    match_dob = re.search(r'(\d{1,2}\s+\d{1,2}\s+\d{4})', full_text)
    if match_dob:
        data["Fecha de Nacimiento"] = match_dob.group(1)
    else:
        data["Fecha de Nacimiento"] = None

    # Ejemplo 3: Extraer el correo electrónico.
    match_email = re.search(r'[\w\.-]+@[\w\.-]+', full_text)
    if match_email:
        data["Email"] = match_email.group(0)
    else:
        data["Email"] = None

    # Ejemplo 4: Extraer el programa a estudiar.
    for idx, line in enumerate(lines):
        if "Programa a Estudiar" in line:
            if idx+1 < len(lines):
                data["Programa a Estudiar"] = lines[idx+1].strip()
            break

    # Se pueden agregar más patrones para extraer otros campos según sea necesario.
    return data

if __name__ == "__main__":
    pdf_file = r"C:\Users\HP\Downloads\prueba.pdf"
    extracted_info = extract_data_from_pdf(pdf_file)

    # Convertir la información extraída en un DataFrame de pandas
    df = pd.DataFrame([extracted_info])
    print(df)


# In[ ]:




