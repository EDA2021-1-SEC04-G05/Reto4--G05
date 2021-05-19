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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import graphstructure as gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {
                    'landingpoints': None,
                    'connections': None,
                    'countries': None}

    analyzer['landingpoints'] = mp.newMap(maptype='PROBING',
                                     comparefunction=compareIds)
    analyzer['countries'] = mp.newMap(maptype='PROBING',
                                     comparefunction=compareIds)

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds)
    return analyzer


# Funciones para agregar informacion al catalogo
def addLanding(analyzer,line):
    origin=line['\ufefforigin']
    destination=line['destination']
    length=line['cable_length'].strip(" km")
    addPoint(analyzer,origin)
    addPoint(analyzer,destination)
    addLine(analyzer,length,origin,destination)

def addPoint(analyzer,origin):
    exists=gr.containsVertex(analyzer['connections'], origin)
    if not exists: 
        gr.insertVertex(analyzer['connections'], origin)
def addLine(analyzer,length,origin,destination):
    arco=gr.getEdge(analyzer['connections'],origin,destination)
    if arco == None: 
        gr.addEdge(analyzer['connections'],origin,destination,length)

def addInfo(analyzer,line):
    mp.put(analyzer['landingpoints'],line['landing_point_id'],line)

def addCountry(analyzer,line):
    mp.put(analyzer['countries'],line['CountryName'],line)

  

# ==============================
# Funciones de consulta
# ==============================


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
def compareNames(countryname, entry):
    """
    Compara dos ids de videos, id es un identificador
    y entry una pareja llave-valor
    """
    if countryname == entry :
        return 0
    elif countryname > entry:
        return 1
    else:
        return -1