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
from DISClib.DataStructures import listiterator as lit
import haversine as hs
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.Algorithms.Graphs import scc 
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
                                              size=140000,
                                              comparefunction=compareIds)
    return analyzer


# Funciones para agregar informacion al catalogo
def addLanding(analyzer,line):
    origin=line['\ufefforigin']
    cable_id=line['cable_id']
    lableo=origin+"-"+cable_id
    destination=line['destination']
    labled=destination+"-"+cable_id
    length=line['cable_length']

    if length!='n.a.':
        length=length.strip(" km").replace(",", "")
        length=float(length)
    addPoint(analyzer,lableo)
    addPoint(analyzer,labled)
    addLine(analyzer,length,lableo,labled)


def addPoint(analyzer,lable):
    exists=gr.containsVertex(analyzer['connections'], lable)
    if not exists: 
        gr.insertVertex(analyzer['connections'], lable)
def addLine(analyzer,length,origin,destination):
    arco=gr.getEdge(analyzer['connections'],origin,destination)
    if arco == None: 
        gr.addEdge(analyzer['connections'],origin,destination,length)

def addInfo(analyzer,line):
    mp.put(analyzer['landingpoints'],line['landing_point_id'],line)

def addCountry(analyzer,line):
    mp.put(analyzer['countries'],line['CountryName'],line)

def addConnection(analyzer):
    vertices=gr.vertices(analyzer['connections'])
    a=lit.newIterator(vertices)
    while lit.hasNext(a):
        c=lit.next(a)
        b=lit.newIterator(vertices)
        while lit.hasNext(b):
            d=lit.next(b)
            if c!=d: 
                h=c.split("-")
                j=d.split("-")
                if h[0]==j[0]:
                    addLine(analyzer,100,c,d)
def addCapital(analyzer):
    #print("Capital")
    Lista=lt.newList()
    for capital in (analyzer['countries']['table']['elements']):
        if capital['key']!=None:
            cap=mp.get(analyzer['countries'], capital['key'])
            cap=cap['value']
            addPoint(analyzer,cap['CapitalName'])
            mini=100000000000
            dist=0
            landes=" "
            loc1=(float(cap['CapitalLatitude']),float(cap['CapitalLongitude']))
            for landingp in (analyzer['landingpoints']['table']['elements']):
                if landingp['key']!=None and landingp['key'] not in Lista:
                    land=mp.get(analyzer['landingpoints'], landingp['key'])
                    land=land['value']
                    loc2=(float(land['latitude']),float(land['longitude']))
                    dist=hs.haversine(loc1,loc2)
                    if dist<mini:
                        mini=dist
                        landes=land['landing_point_id']
            vertices=gr.vertices(analyzer['connections'])
            a=lit.newIterator(vertices)
            while lit.hasNext(a):
                c=lit.next(a)
                h=c.split("-")
                #print(h)
                #if h[0] not in Lista:
                if h[0]==landes:
                    #print(h[0],c)
                    #print(h[0])
                    addLine(analyzer,mini,cap['CapitalName'],c)
                   # print(capital['key'],c)
            lt.addLast(Lista, landes)
                
            #print('va uno')

# ==============================
# Funciones de consulta
# ==============================
def Clusters(analyzer,l1,l2):
    estructura=scc.KosarajuSCC(analyzer['connections'])
    idscc=estructura['idscc']
    numero=scc.connectedComponents(estructura)
    land1=lt.newList()
    land2=lt.newList()
    vertices=gr.vertices(analyzer['connections'])
    a=lit.newIterator(vertices)
    answer=False
    while lit.hasNext(a):
        c=lit.next(a)
        h=c.split("-")
                #print(h)
                #if h[0] not in Lista:
        if h[0]==l1:
            lt.addLast(land1, c)
        if h[0]==l2:
            lt.addLast(land2, c)
    la1=lit.newIterator(land1)
    while lit.hasNext(la1):
        b=lit.next(la1)
        entry=mp.get(idscc,b)
        cluster=me.getValue(entry)
        la2=lit.newIterator(land1)
        while lit.hasNext(la2):
            c=lit.next(la2)
            entry=mp.get(idscc,c)
            cluster1=me.getValue(entry)
            if cluster1==cluster:
                answer=True
                return (answer,numero)
    return (answer,numero)
def distPaises (analyzer,paisA,paisB):
    pA=mp.get(analyzer['countries'],paisA)
    route=dij.Dijkstra(analyzer['connections'], pA['CapitalName'])
    pB=mp.get(analyzer['countries'],paisB)
    #route=dij.Dijkstra(analyzer['connections'], pB['CapitalName'])
    path=dij.hasPathTo(route, pB['CapitalNames'])
    if path==True:
        dist=dij.distTo(route, pB['CapitalNames'])
        path=dij.pathTo(route, pB['CapitalNames'])
    return (dist,path)

    #has path to 
    #dist to 
    #path to 



        
    
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