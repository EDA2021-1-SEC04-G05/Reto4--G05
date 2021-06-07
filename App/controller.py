"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
import time
import tracemalloc


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadServices(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    """

    servicefile='connections.csv'
    servicesfile = cf.data_dir + servicefile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for line in input_file:
        model.addLanding(analyzer,line)
    servicefile='landing_points.csv'
    servicesfile = cf.data_dir + servicefile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for line in input_file:
        model.addInfo(analyzer,line)

    servicefile='countries.csv'
    servicesfile = cf.data_dir + servicefile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for line in input_file:
        model.addCountry(analyzer,line)
    print("1")
    model.addConnection(analyzer)
    print('2')
    model.addCapital(analyzer)
    print('3')
    """
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return (analyzer,delta_time, delta_memory)"""
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def Clusters(analyzer,l1,l2):
    ans=model.Clusters(analyzer, l1, l2)
    return ans

def req2(analyzer):
    ans=model.req2(analyzer)
    return ans

def distPaises (analyzer,paisA,paisB):
    ans=model.distPaises(analyzer, paisA, paisB)
    return ans
    
def req4(analyzer):
    ans=model.req4(analyzer)
    return ans

def Fallas (analyzer,vertice):
    ans=model.fallas(analyzer, vertice)
    return ans

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo



#funciones para medir 
