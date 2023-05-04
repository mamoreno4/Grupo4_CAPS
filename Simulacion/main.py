import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import clases_simulacion as cs


Distribuciones= pd.read_excel('./../Distribuciones/dist.xlsx', index_col=0)



# main
dia_actual = 1
#Cantidad de cosecha por bodega y cepa
#dictionary = {'key':value}
cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_3000 = ['Machali':['G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0], 'Chepica':['G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0], 'Nancagua':['G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0]]
cantidad_6000 = ['Machali':['G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0], 'Chepica':['G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0], 'Nancagua':['G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0]]
#tamaño de tanques para iterar
tamanos_T = [100,75,50,30]
while ((dia_actual < 15) or (len(cs.Las_Bodegas[0].tanques_fermentando) > 0) or (len(cs.Las_Bodegas[1].tanques_fermentando) > 0) or (len(cs.Las_Bodegas[2].tanques_fermentando) > 0)):
    for bodega in cs.Las_Bodegas:
        salidas = bodega.revisar_tanques(dia_actual)
        if len(salidas) == 0:
            print("No hubo salidas en la bodega " + bodega.ubicacion)
        else:
            for salida in salidas:
                cs.Resumen.agregar_fermentado(dia_actual, salida)
    #revisar cosecha diaria por cuartel y precio
    for cuartel in cs.Los_Cuarteles:
        if cuartel.precio == 1000:
            CD=cuartel.cosecha_por_dia[dia_actual]
            #junta las variedades de cada cuartel
            cantidad_1000[CD[0]][cuartel.variedad] = cantidad_1000 + CD[1]
        elif cuartel.precio == 3000:
            CD=cuartel.cosecha_por_dia[dia_actual]
            cantidad_3000[CD[0]][cuartel.variedad] = cantidad_3000 + CD[1]
        elif cuartel.precio == 6000:
            CD=cuartel.cosecha_por_dia[dia_actual]
            cantidad_6000[CD[0]][cuartel.variedad] = cantidad_6000 + CD[1]
    #iterar bodegas
    for bodega in cs.Las_Bodegas:
        #establecer bodega actual
        Nbodega=bodega.ubicacion
        #iterar por precio
        for Ncepa in cantidad_6000[Nbodega]:
            #iterar por tamaño de tanque
            for tamano in tamanos_T:
                #boleano para saber si es mas grande que el tanque
                Grande=True
                #mientras sea mas grande que el tanque y haya tanques disponibles
                while Grande==True and len(bodega.tanques_disponibles(tamano))>0:
                    #selecciona el primer tanque disponible
                    Td=bodega.tanques_disponibles(tamano)[0]
                    #si la cantidad es mayor que el 95% del tanque
                    if cantidad_6000[Nbodega][Ncepa] > tamano*0.95:
                        Td.fermentar(tamano*0.95, dia_actual, Ncepa,6000,Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_6000[Nbodega][Ncepa] = cantidad_6000[Nbodega][Ncepa] - tamano*0.95
                    #si la cantidad es mayor que el 65% del tanque
                    elif tamano*0.65 <= cantidad_6000[Nbodega][Ncepa] <= tamano*0.95:
                        Td.fermentar(cantidad_6000[Nbodega][Ncepa], dia_actual, Ncepa,6000,Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_6000[Nbodega][Ncepa] = 0
                        Grande=False
                    #si la cantidad es menor que el 65% del tanque
                    elif cantidad_6000[Nbodega][Ncepa] < tamano*0.65:
                        Grande=False
        for Ncepa in cantidad_3000[Nbodega]:
            for tamano in tamanos_T:
                Grande=True
                while Grande==True and len(bodega.tanques_disponibles(tamano))>0:
                    Td=bodega.tanques_disponibles(tamano)[0]
                    if cantidad_3000[Nbodega][Ncepa] > tamano*0.95:
                        Td.fermentar(tamano*0.95, dia_actual, Ncepa,3000,Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_3000[Nbodega][Ncepa] = cantidad_3000[Nbodega][Ncepa] - tamano*0.95
                    elif tamano*0.65 <= cantidad_3000[Nbodega][Ncepa] <= tamano*0.95:
                        Td.fermentar(cantidad_3000[Nbodega][Ncepa], dia_actual, Ncepa,3000,Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_3000[Nbodega][Ncepa] = 0
                        Grande=False
                    elif cantidad_3000[Nbodega][Ncepa] < tamano*0.65:
                        Grande=False

        for Ncepa in cantidad_1000[Nbodega]:
            for tamano in tamanos_T:
                Grande=True
                while Grande==True and len(bodega.tanques_disponibles(tamano))>0:
                    Td=bodega.tanques_disponibles(tamano)[0]
                    if cantidad_1000[Nbodega][Ncepa] > tamano*0.95:
                        Td.fermentar(tamano*0.95, dia_actual, Ncepa,1000,Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_1000[Nbodega][Ncepa] = cantidad_1000[Nbodega][Ncepa] - tamano*0.95
                    elif tamano*0.65 <= cantidad_1000[Nbodega][Ncepa] <= tamano*0.95:
                        Td.fermentar(cantidad_1000[Nbodega][Ncepa], dia_actual, Ncepa,1000,Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_1000[Nbodega][Ncepa] = 0
                        Grande=False
                    elif cantidad_1000[Nbodega][Ncepa] < tamano*0.65:
                        Grande=False
                    
            
    """""
    for bodega in cs.Las_Bodegas:
        if len(bodega.tanques_disponibles) > 0:
            for tanque in bodega.tanques_disponibles:
                if cantidad_6000 < tanque.capacidad*0.65:
                    print("No hay cantidad suficiente de variedad de precio de 6000 para ocupar el tanque")
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_1000)
                elif tanque.capacidad*0.65 <= cantidad_6000 <= tanque.capacidad*0.95:
                    tanque = tanque.fermentar(cantidad_6000, dia_actual, "", 6000, "")
                    bodega.agregar_tanque_fermentando(tanque)
                    cs.Resumen.agregar_tanque(dia_actual, cantidad_6000)
                    cantidad_6000 = 0
                elif cantidad_6000 > tanque.capacidad*0.95:
                    tanque = tanque.fermentar(tanque.capacidad*0.95, dia_actual, "", 6000, "")
                    bodega.agregar_tanque_fermentando(tanque)
                    cantidad_6000 = cantidad_6000 - tanque.capacidad*0.95
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_6000)

                if cantidad_3000 < tanque.capacidad*0.65:
                    print("No hay cantidad suficiente de variedad de precio de 3000 para ocupar el tanque")
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_1000)
                elif tanque.capacidad*0.65 <= cantidad_3000 <= tanque.capacidad*0.95:
                    tanque = tanque.fermentar(cantidad_3000, dia_actual, "", 3000, "")
                    bodega.agregar_tanque_fermentando(tanque)
                    cs.Resumen.agregar_tanque(dia_actual, cantidad_3000)
                    cantidad_3000 = 0
                elif cantidad_3000 > tanque.capacidad*0.95:
                    tanque = tanque.fermentar(tanque.capacidad*0.95, dia_actual, "", 3000, "")
                    bodega.agregar_tanque_fermentando(tanque)
                    cantidad_3000 = cantidad_3000 - tanque.capacidad*0.95
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_3000)

                if cantidad_1000 < tanque.capacidad*0.65:
                    print("No hay cantidad suficiente de variedad de precio de 1000 para ocupar el tanque")
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_1000)
                elif tanque.capacidad*0.65 <= cantidad_1000 <= tanque.capacidad*0.95:
                    tanque = tanque.fermentar(cantidad_1000, dia_actual, "", 1000, "")
                    bodega.agregar_tanque_fermentando(tanque)
                    cs.Resumen.agregar_tanque(dia_actual, cantidad_1000)
                    cantidad_1000 = 0
                elif cantidad_1000 > tanque.capacidad*0.95:
                    tanque = tanque.fermentar(tanque.capacidad*0.95, dia_actual, "", 1000, "")
                    bodega.agregar_tanque_fermentando(tanque)
                    cantidad_1000 = cantidad_1000 - tanque.capacidad*0.95
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_1000)

        elif len(bodega.tanques_disponibles) == 0:
            print("No hay tanques disponibles en la bodega " + bodega.ubicacion)
    """""
    cantidad_1000 = 0
    cantidad_3000 = 0
    cantidad_6000 = 0
    dia_actual = dia_actual + 1
