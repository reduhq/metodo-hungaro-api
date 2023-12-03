from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
import numpy as np

import copy


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
    
    resultado_final = resultado(matriz_final)
    
    if terminado:
        return {
            "matriz": matriz.tolist(),
            "iteracion_1": iteracion_1,
            "iteracion_2": iteracion_2,
            "matriz_tachada": mat.tolist(),
            "resultado_final": resultado_final
        }
    
    # Si no esta terminado tendra que hacer mas operaciones...
    nueva_matriz = mat
    print(matriz_final)
    print(nueva_matriz)
    
    # Encontrar el número menor positivo en la nueva matriz
    numeros_positivos = nueva_matriz[nueva_matriz > 0]
    numero_menor_positivo = np.min(numeros_positivos)

    # Restar el número menor positivo solo a los valores positivos de la matriz reducida
    matriz_resultante = np.where(nueva_matriz > 0, nueva_matriz - numero_menor_positivo, nueva_matriz)

    terminado2, mat2 = verificar(matriz_resultante)
    
    #########################################33
    # Encontrar los índices donde la segunda matriz tiene -1
    indices_a_rellenar = np.where(matriz_resultante == -1)

    # Rellenar esos espacios con los datos de la primera matriz
    matriz_resultante[indices_a_rellenar] = matriz_final[indices_a_rellenar]
    
    resultado_final = resultado(matriz_resultante)
    
    if terminado2:
        return{
            "matriz": matriz.tolist(),
            "iteracion_1": iteracion_1,
            "iteracion_2": iteracion_2,
            "matriz_tachada": mat.tolist(),
            "matriz_resultante": matriz_resultante.tolist(),
            "resultado_final": resultado_final
        }
    
    
    return "holi"


def verificar(matriz):
    mat = copy.copy(matriz)
    
    # Obtener el número de filas
    num_filas = mat.shape[0]
    
    # Buscando en que filas o columnas hay 2 o mas ceros para tacharlas
    for i in range(num_filas):
        # Contar el número de elementos iguales a 0 en la fila
        num_zeros = np.count_nonzero(mat[i] == 0)
        
        # Si hay 2 o más 0 en la fila, convertir toda la fila a -1
        if num_zeros >= 2:
            mat[i] = -1
        
        # Verificar la columna i después de completar la verificación de filas
        columna_x = mat[:, i]
        num_zeros_en_columna_x = np.count_nonzero(columna_x == 0)
        
        # Si hay 2 o más ceros en la columna i, convertir toda la columna a -1
        if num_zeros_en_columna_x >= 2:
            mat[:, i] = -1
    
    # Buscando en que filas o columnas hay excatamente 1 cero para tacharlas
    for i in range(num_filas):
        # Contar el número de elementos iguales a 0 en la fila i
        num_zeros = np.count_nonzero(mat[i] == 0)
        
        # Si hay exactamente 1 cero en la fila, convertir toda la fila a -1
        if num_zeros == 1:
            mat[i] = -1
        
        # Verificar la columna i después de completar la verificación de filas
        columna_x = mat[:, i]
        num_zeros_en_columna_x = np.count_nonzero(columna_x == 0)
        
        # Si hay exactamente 1 cero en la columna i, convertir toda la columna a -1
        if num_zeros_en_columna_x == 1:
            mat[:, i] = -1
            
    # si toda la matriz es igual a -1, retornar true y la matriz resultante
    
    # Verifica si todos los elementos son iguales a -1
    son_todos_iguales = np.all(mat == -1)
    if son_todos_iguales:
        return True, mat
    
    # Contando cuantas filas y columnas tachadas hay 
    
    # Encontrar las filas que solo contienen -1
    filas_solo_minus1 = np.all(mat == -1, axis=1)

    # Encontrar las columnas que solo contienen -1
    columnas_solo_minus1 = np.all(mat == -1, axis=0)

    # Contar el número de filas y columnas que solo contienen -1
    num_filas_solo_minus1 = np.count_nonzero(filas_solo_minus1)
    num_columnas_solo_minus1 = np.count_nonzero(columnas_solo_minus1)

    return (num_filas_solo_minus1+num_columnas_solo_minus1) == num_filas, mat

def resultado(matriz_final):
    matriz = matriz_final
    indices_cero = []

    # Iterando en cada fila para encontrar las filas donde solo hay exactamente un 0
    for i, fila in enumerate(matriz):
        #
        indices_cero_fila = np.where(fila == 0)[0]

        if len(indices_cero_fila) == 1:
            indice_cero = indices_cero_fila[0]
            indices_cero.append([int(i), int(indice_cero)])

    nuevos_indices = encontrar_filas_con_dos_o_mas_ceros(matriz, indices_cero)
    
    indices = indices_cero + nuevos_indices
    return indices


def encontrar_filas_con_dos_o_mas_ceros(matriz, indices_cero_anterior):
    nuevas_filas_cero = []

    for i, fila in enumerate(matriz):
        indices_cero_fila = np.where(fila == 0)[0]
        
        if len(indices_cero_fila) == 1:
            continue

        # Verificar si alguna columna con 0 tiene exactamente un 0
        for indice_cero in indices_cero_fila:
            columna = matriz[:, indice_cero]
            if np.count_nonzero(columna == 0) == 1:
                nuevas_filas_cero.append([int(i), int(indice_cero)])
                break
        else:
            # Si no se encontró ninguna columna con exactamente un 0,
            # buscar en la lista anterior y agregar el primer índice que cumple las condiciones
            for indice_cero in indices_cero_fila:
                if indice_cero not in [idx[1] for idx in indices_cero_anterior]:
                    nuevas_filas_cero.append([int(i), int(indice_cero)])
                    break

    return nuevas_filas_cero

# {
#   "matriz": [
#     180,150,200,200,250,305,450,500,200,208,320,100
#   ],
#   "fila": 3,
#   "columnas": 4
# }


# {
#   "matriz": [
#     10,10,5,13,0,4,6,0,9,1,10,0,3,8,5,0,8,10,5,0,12,14,0,4,0,13,16,12,12,13,10,4,0,2,5,9
#   ],
#   "fila": 6,
#   "columnas": 6
# }


# {
#   "matriz": [
#     3,4,0,4,5,0,0,0,3
#   ],
#   "fila": 3,
#   "columnas": 3
# }
