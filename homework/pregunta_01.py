"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import re
import glob
import os
import pandas as pd

def read_records_from_input(input_folder):
        sequence = []
        path = os.path.join(input_folder, "*")
        files = glob.glob(path)
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    sequence.append(line)
        return sequence


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
    input_folder = "files/input"
    records = read_records_from_input(input_folder)
    del records[3] 
    patron = r"  [a-zA-ZáéíóúÁÉÍÓÚñÑ]"
    indices_filas = []
    indices_filas.append(0)
    indices_filas.extend([coincidencia.start()+2 for coincidencia in re.finditer(patron, records[0])])
    
    resultado = []
    fila_resultado =[]

    for fila in records:
      if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', fila.strip())  and len(fila_resultado) > 0:
        resultado.append(fila_resultado)
        fila_resultado = []

      else:
        partes = []
        for i in range(len(indices_filas)):
          if i+1 < len(indices_filas):
            palabras = fila[indices_filas[i]:indices_filas[i+1]].strip()
          else:
            palabras = fila[indices_filas[i]:].strip()
          palabras = re.sub(r"\s+", " ", palabras)
          partes.append(palabras)
          
        if fila_resultado:
          fila_resultado = list(map(lambda a, b: re.sub(r"\s+", " ", a +" "+b), fila_resultado, partes))
        else:
          fila_resultado = partes

    tabla = pd.DataFrame(resultado[1:],columns=resultado[0])

    tabla.columns = (
      tabla.columns
      .str.lower()
      .str.strip()
      .str.replace(' ', '_')
    )

    tabla[tabla.columns[-1]] = (
    tabla[tabla.columns[-1]]
    .str.replace(',', ', ')
    .str.replace('.', '')
    )

    tabla[tabla.columns] = tabla[tabla.columns].apply(
      lambda col: col.str.replace(r'\s+', ' ', regex=True).str.strip()
    )



    tabla[tabla.columns[0]] = pd.to_numeric(tabla[tabla.columns[0]], errors='coerce')
    tabla[tabla.columns[1]] = pd.to_numeric(tabla[tabla.columns[1]], errors='coerce')

    tabla[tabla.columns[2]] = (
    tabla[tabla.columns[2]]
    .str.replace('%', '')
    .str.replace(' ', '')
    .str.replace(',', '.')
    )


    tabla[tabla.columns[2]] = pd.to_numeric(tabla[tabla.columns[2]], errors='coerce')
    return tabla

pregunta_01()


