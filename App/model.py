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
from DISClib.DataStructures import linkedlistiterator as lit
import haversine as hs
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.Algorithms.Graphs import scc 
import sys
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
sys.setrecursionlimit(999999)

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
                    'countries': None,
                    'cont':0,
                    'list':" "}

    analyzer['landingpoints'] = mp.newMap(maptype='PROBING',
                                     comparefunction=compareIds)
    analyzer['countries'] = mp.newMap(maptype='PROBING',
                                     comparefunction=compareIds)

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds)
    analyzer['list']=lt.newList()
    return analyzer


# Funciones para agregar informacion al catalogo

def addLanding(analyzer,line):
    a=lt.isEmpty(analyzer['list'])
    if a==True:
        origin=line['\ufefforigin']
        cable_id=line['cable_id']
        lableo=origin+"-"+cable_id
        addPoint(analyzer, lableo)

        length=line['cable_length']
        if length!='n.a.':
            length=length.strip(" km").replace(",", "")
            length=float(length)
        else:
            length=0.1
        lt.addFirst(analyzer['list'], (lableo,length))
        #mp.put(analyzer['names'], line['name'], lableo)

    else:
        #origin=line['\ufefforigin']
        cable_id=line['cable_id']
        last=lt.getElement(analyzer['list'], lt.size(analyzer['list']))
        lableo=last[0]
        lengthl=last[1]
        destination=line['\ufefforigin']
        labled=destination+"-"+cable_id
        length=line['cable_length']

        if length!='n.a.':
            length=length.strip(" km").replace(",", "")
            length=float(length)
        else:
            length=0
        #addPoint(analyzer,lableo)
        addPoint(analyzer,labled)
        addLine(analyzer,lengthl,lableo,labled)
        lt.addLast(analyzer['list'], (labled,length))
        #mp.put(analyzer['names'], line['name'], lableo)


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
    lable=line['landing_point_id']+"-"+line['name']
    addPoint(analyzer,lable)

def addCountry(analyzer,line):
    mp.put(analyzer['countries'],line['CountryName'],line)
    addPoint(analyzer,line['CapitalName'])

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
            cap=me.getValue(mp.get(analyzer['countries'], capital['key']))
            mini=100000000000
            dist=0
            landes=" "
            loc1=(float(cap['CapitalLatitude']),float(cap['CapitalLongitude']))
            for landingp in (analyzer['landingpoints']['table']['elements']):
                if landingp['key']!=None and landingp['key'] not in Lista:
                    land=me.getValue(mp.get(analyzer['landingpoints'], landingp['key']))
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
                    #
                    #print(cap['CapitalName'],c)
            lt.addLast(Lista, landes)
                
            #print('va uno')

# ==============================
# Funciones de consulta
# ==============================
def Clusters(analyzer,l1,l2):
    estructura=scc.KosarajuSCC(analyzer['connections'])
    idscc=estructura['idscc']
    #print(idscc)
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
        #print(cluster)
        la2=lit.newIterator(land2)
        while lit.hasNext(la2):
            c=lit.next(la2)
            entry=mp.get(idscc,c)
            cluster1=me.getValue(entry)
            if cluster1==cluster:
                #print(cluster1)
                answer=True
                return (answer,numero)
    return (answer,numero)

def distPaises (analyzer,paisA,paisB):
    pA=me.getValue(mp.get(analyzer['countries'],paisA))
    minin=1000000
    listi=lt.newList()
    loc1=(float(pA['CapitalLatitude']),float(pA['CapitalLongitude']))
    for landingp in (analyzer['landingpoints']['table']['elements']):
        if landingp['key']!=None:
            land=me.getValue(mp.get(analyzer['landingpoints'], landingp['key']))
            loc2=(float(land['latitude']),float(land['longitude']))
            dist=hs.haversine(loc1,loc2)
            if dist<minin:
                minin=dist
                landeA=land['landing_point_id']
    pB=me.getValue(mp.get(analyzer['countries'],paisB))
    Lista=lt.newList()
    dist=0
    mini=10000000
    loc1=(float(pB['CapitalLatitude']),float(pB['CapitalLongitude']))
    for landingp in (analyzer['landingpoints']['table']['elements']):
         if landingp['key']!=None:
            land=me.getValue(mp.get(analyzer['landingpoints'], landingp['key']))
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
        if h[0]==landes:
            lt.addLast(Lista, c)
        if h[0]==landeA:
            x=c 
            lt.addLast(listi, c)
    dist=-1
    path="No"
    disti=1000000000000000
    pathh="No"
    t=lit.newIterator(listi)
    while lit.hasNext(t):
        y=lit.next(t)
        route=dij.Dijkstra(analyzer['connections'],y)
        a=lit.newIterator(Lista)
        while lit.hasNext(a):
            e=lit.next(a)
            path=dij.hasPathTo(route, e)
            if path==True:
                dist=dij.distTo(route, e)
                path=dij.pathTo(route, e)
                if path !=None and dist<disti: 
                    disti=dist
    return(path,disti)

def fallas(analyzer,vertice):
    print(vertice)
    Lista=lt.newList()
    listi=lt.newList()
    
    #recorrer map con los landing points y decir que si vertice == [name:] entonces name=l[name]

    
    vertices=gr.vertices(analyzer['connections'])
    b=lit.newIterator(vertices)
    name=" "
    while lit.hasNext(b) and name== " ":
        c=lit.next(b)
        if "-" in c:
            h=c.split("-")
            if h[1]==vertice:
                name=c
                print("hola")
    
    edges=gr.adjacents(analyzer['connections'], name)

    b=lit.newIterator(edges)
    while lit.hasNext(b):
        c=lit.next(b)
        h=c.split("-")
        p=me.getValue(mp.get(analyzer['landingpoints'],h[0]))
        loc1=(float(p['latitude']),float(p['longitude']))
        minin=100000000
        landeA=0
        for country in (analyzer['countries']['table']['elements']):
           
            if country['key']!=None:
                land=me.getValue(mp.get(analyzer['countries'], country['key']))
                loc2=(float(land['CapitalLatitude']),float(land['CapitalLongitude']))
                dist=hs.haversine(loc1,loc2)
                if dist<minin:
                    minin=dist
                    print("si")
                    landeA=land['CountryName']
        if landeA !=0:
            lt.addLast(Lista, landeA)  
    return Lista



        
    
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