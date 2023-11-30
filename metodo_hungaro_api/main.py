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
    
    return {
        "matriz": matriz_final.tolist(),
        "iteracion_1": iteracion_1,
        "iteracion_2": iteracion_2
    }

# {
#   "matriz": [
#     180,150,200,200,250,305,450,500,200,208,320,100
#   ],
#   "fila": 3,
#   "columnas": 4
# }

