from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
import numpy as np


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],   # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],   # Permitir todas las cabeceras
)

class Matriz(BaseModel):
    matriz:list[int]
    fila: int = Field(default=..., gt=1)
    columnas: int

@app.post("/", response_model=None)
def hello_world(
    matriz_user:Matriz = Body(...)
):
    matriz = np.reshape(matriz_user.matriz, (matriz_user.fila, matriz_user.columnas))
    if matriz.shape[0] < matriz.shape[1]: #(rows, columns)
        # Agregar una fila de ceros
        nueva_fila = np.zeros((1, matriz.shape[1]), dtype=int)  # Crear una fila de ceros
        # Concatenar la nueva fila al array bidimensional
        array_bidimensional_con_cero = np.vstack((matriz, nueva_fila))
        matriz = array_bidimensional_con_cero
        
    
    if matriz.shape[0] > matriz.shape[1]: #(rows, columns)
        # Agregar una columna de ceros
        nueva_columna = np.zeros((matriz.shape[0], 1), dtype=int)  # Crear una columna de ceros

        # Concatenar la nueva columna al array bidimensional
        array_bidimensional_con_cero = np.hstack((matriz, nueva_columna))
        matriz = array_bidimensional_con_cero
    
    iteracion_1 = []
    for row in matriz.tolist():
        #sacando el minimo de la fila
        min_fila = min(row)
        fila_iteracion = [ n-min_fila for n in row ]
        iteracion_1.append(fila_iteracion)
        
    # Encontrando el numero menor en las columnas y restandolo
    matriz_transpuesta = np.transpose(iteracion_1)
    iteracion_2 = []
    for row in matriz_transpuesta.tolist():
        #sacando el minimo de la fila
        min_fila = min(row)
        fila_iteracion = [ n-min_fila for n in row ]
        iteracion_2.append(fila_iteracion)
        
    matriz_final = np.transpose(iteracion_2)
    
    # Verificando si el ejercicio esta terminado
    terminado, mat = verificar(matriz_final)
    
    if terminado:
        return {
            "matriz": matriz_final.tolist(),
            "iteracion_1": iteracion_1,
            "iteracion_2": iteracion_2,
            "matriz_tachada": mat.tolist()
        }
    
    # Si no esta terminado tendra que hacer mas operaciones...
    nueva_matriz = mat
    
    # Encontrar el número menor positivo en la nueva matriz
    numeros_positivos = nueva_matriz[nueva_matriz > 0]
    numero_menor_positivo = np.min(numeros_positivos)

    # Restar el número menor positivo solo a los valores positivos de la matriz reducida
    matriz_resultante = np.where(nueva_matriz > 0, nueva_matriz - numero_menor_positivo, nueva_matriz)

    terminado, mat = verificar(matriz_resultante)
    
    if terminado:
        return{
            "matriz": matriz_final.tolist(),
            "iteracion_1": iteracion_1,
            "iteracion_2": iteracion_2,
            "matriz_tachada": mat.tolist(),
            "matriz_resultante": matriz_resultante.tolist()
        }
    
    
    return "holi"


def verificar(matriz):
    mat = matriz
    
    # Obtener el número de filas
    num_filas = matriz.shape[0]
    
    # Buscando en que filas o columnas hay 2 o mas ceros para tacharlas
    for i in range(num_filas):
        # Contar el número de elementos iguales a 0 en la fila
        num_zeros = np.count_nonzero(mat[i] == 0)
        
        # Si hay 2 o más 0 en la fila, convertir toda la fila a -1
        if num_zeros >= 2:
            mat[i] = -1
        
        # Verificar la columna i después de completar la verificación de filas
        columna_x = matriz[:, i]
        num_zeros_en_columna_x = np.count_nonzero(columna_x == 0)
        
        # Si hay 2 o más ceros en la columna i, convertir toda la columna a -1
        if num_zeros_en_columna_x >= 2:
            matriz[:, i] = -1
    
    # Buscando en que filas o columnas hay excatamente 1 cero para tacharlas
    for i in range(num_filas):
        # Contar el número de elementos iguales a 0 en la fila i
        num_zeros = np.count_nonzero(mat[i] == 0)
        
        # Si hay exactamente 1 cero en la fila, convertir toda la fila a -1
        if num_zeros == 1:
            mat[i] = -1
        
        # Verificar la columna i después de completar la verificación de filas
        columna_x = matriz[:, i]
        num_zeros_en_columna_x = np.count_nonzero(columna_x == 0)
        
        # Si hay exactamente 1 cero en la columna i, convertir toda la columna a -1
        if num_zeros_en_columna_x == 1:
            matriz[:, i] = -1
    
    # Contando cuantas filas y columnas tachadas hay 
    
    # Encontrar las filas que solo contienen -1
    filas_solo_minus1 = np.all(matriz == -1, axis=1)

    # Encontrar las columnas que solo contienen -1
    columnas_solo_minus1 = np.all(matriz == -1, axis=0)

    # Contar el número de filas y columnas que solo contienen -1
    num_filas_solo_minus1 = np.count_nonzero(filas_solo_minus1)
    num_columnas_solo_minus1 = np.count_nonzero(columnas_solo_minus1)

    return (num_filas_solo_minus1+num_columnas_solo_minus1) == num_filas, mat

# {
#   "matriz": [
#     180,150,200,200,250,305,450,500,200,208,320,100
#   ],
#   "fila": 3,
#   "columnas": 4
# }

