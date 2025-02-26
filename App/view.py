﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.DataStructures import graphstructure as gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import linkedlistiterator as lit


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- REQ. 1: Identificar los clústeres de comunicación")
    print("2- Identificar los puntos de conexión críticos de la red")
    print("3- La ruta de menor distancia")
    print("4- Identificar la Infraestructura Crítica de la Red ")
    print("5-Análisis de fallas ")
    print("6- Los mejores canales para transmitir")
    print("7- La mejor ruta para comunicarme")
    print("8- Graficar los Grafos")



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        analyzer=controller.init()
        analyzer=controller.loadServices(analyzer)
        print("El total de landing points:"+ str(gr.numVertices(analyzer['connections'])))
        print("El total de conexiones entre landing points:" + str(gr.numEdges(analyzer['connections'])))
        print("El total de países:"+ str(mp.size(analyzer['countries'])))
        #for i in range (0,1): 
        #    for a in (analyzer['landingpoints']['table']['elements']):
        #        b=a
                
        #print("La información del primer landing point cargado: identificador:{0}, nombre:{1}, latitud:{2}, longitud:{3}".format(b[landing_point_id],b[id],b[name],b[latitude],b[longitude]))
#Mostrar la información de población y número usuarios de Internet del último país cargado.


    elif int(inputs[0]) == 1:
        l1=input("ingrese primer landing point:")
        l2=input("ingrese segundo landing point:")
        result=controller.Clusters(analyzer, l1, l2)
        #print(result)
        if result[0]==True:
            r="si"
        else:
            r="no"
        print("Los landingpoints {0} y {1} {2} son del mismo cluster ".format(l1,l2,r))
        print("EL total de clusters es de " + str(result[1]))
    
    elif int(inputs[0]) ==2:
        result=controller.req2(analyzer)

    elif int(inputs[0]) == 3:
        paisA=input("ingrese primer pais:")
        paisB=input("ingrese segundo pais:")
        result=controller.distPaises(analyzer, paisA, paisB)
        number=result[1]
        a=lit.newIterator(result[0])
        while lit.hasNext(a):
            e=lit.next(a)
            print("from " + str(e['vertexA'])+ " to "+str(e['vertexB'])+ " in " + str(e['weight']) )
        print("The total distances is " + str(number))
       # if result[0]==True:
        #    r="si"
        #else:
            #r="no"
        #print("Los landingpoints {0} y {1} {2} son del mismo cluster ".format(l1,l2,r))
        #print("EL total de clusters es de" + str(result[1]))
    
    elif int(inputs[0] == 4):
        result=controller.req4(analyzer)

    elif int(inputs[0]) == 5:
        paisA=input("ingrese el nombre del landingpoint completo ")
        result=controller.Fallas(analyzer, paisA)
        lis=lt.newList()
        a=lit.newIterator(result)
        while lit.hasNext(a):
            e=lit.next(a)
            if e!=None:
                b=lt.isPresent(lis, e)
                if b==0:
                    lt.addLast(lis, e)
        print("El numero de paises afectados es:"+ str(lt.size(lis)))
        print("Los paises afectados son:")
        a=lit.newIterator(lis)
        while lit.hasNext(a):
            e=lit.next(a)
            print(e)
  
        
    else:
        sys.exit(0)
sys.exit(0)
