from random import uniform, seed, randint, gauss
from numpy.random import Generator, PCG64
import numpy as np
import pandas as pd
from scipy.stats import binom
from clases_simulacion import *



seed=15
scipy_randomGen = binom
numpy_randomGen = Generator(PCG64(seed))
binom.random_state=numpy_randomGen

Distribuciones = pd.read_excel('./../Distribuciones/dist.xlsx', index_col=0)

df = pd.read_csv('solucion (2).csv')

Cuart = pd.read_excel('Datos Base Ordenados (Cosecha).xlsx')
Los_Cuarteles = []
for i in range(1,61):
    CT = Cuartel(Cuart.iloc[i-1])
    D = df.where(df["Cuartel"] == "cuartel_"+str(i))
    D = D.dropna()
    for j in range(len(D)):
        V = D.iloc[j]["Valor"]
        BB = D.iloc[j]["Bodega"]
        DIA = int(D.iloc[j]["Dia"][4:])
        CT.agregar_cosecha(DIA,[BB,V])
    Los_Cuarteles.append(CT)

Bodegas = pd.read_excel("Datos base G4 (2).xlsx",sheet_name="Tanques")
Las_Bodegas = []
for i in range(3):
    BT = Bodega(Bodegas.iloc[i])
    Las_Bodegas.append(BT)

dia_actual = 0
#Cantidad de cosecha por bodega y cepa
#dictionary = {'key':value}
cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
#tamaño de tanques para iterar
tamanos_T = [100,75,50,30]
RESUMENES=[]
#Iterar seeds
for u in range(1):
    dia_actual = 0
    resumen = Resumen()
    seed=u
    scipy_randomGen = binom
    numpy_randomGen = Generator(PCG64(seed))
    binom.random_state=numpy_randomGen
    while ((dia_actual < 120)):
        #print("Dia " + str(dia_actual))
        for bodega in Las_Bodegas:
            salidas = bodega.revisar_tanques(dia_actual)
            if len(salidas) == 0:
                #print("No hubo salidas en la bodega " + bodega.ubicacion)
                pass
            else:
                for salida in salidas:
                    resumen.agregar_fermentado(dia_actual, salida)
                    resumen.fermentado += salida[0]
                    if salida[3] == 1000:
                        resumen.fermentado_1000[bodega.ubicacion][salida[1]] += salida[0]
                    elif salida[3] == 3000:
                        resumen.fermentado_3000[bodega.ubicacion][salida[1]] += salida[0]
                    elif salida[3] == 6000:
                        resumen.fermentado_6000[bodega.ubicacion][salida[1]] += salida[0]
                    pass

        #Revisar cosecha diaria por cuartel y precio

        for cuartel in Los_Cuarteles:
            if dia_actual in cuartel.cosecha_por_dia:
                resumen.cosechado +=cuartel.cosecha_por_dia[dia_actual][1]
                if cuartel.precio == 1000:
                    CD = cuartel.cosecha_por_dia[dia_actual]
                    cantidad_1000[CD[0]][cuartel.variedad] += cuartel.cosecha_por_dia[dia_actual][1]
                elif cuartel.precio == 3000:
                    CD = cuartel.cosecha_por_dia[dia_actual]
                    cantidad_3000[CD[0]][cuartel.variedad] += cuartel.cosecha_por_dia[dia_actual][1]
                elif cuartel.precio == 6000:
                    CD = cuartel.cosecha_por_dia[dia_actual]
                    cantidad_6000[CD[0]][cuartel.variedad] += cuartel.cosecha_por_dia[dia_actual][1]
                else:
                    print("Error en precio")
                    pass
        #Iterar bodegas
        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por precio
            for Ncepa in cantidad_6000[Nbodega]:
                #iterar por tamaño de tanque
                for tamano in tamanos_T:
                    #boleano para saber si es mas grande que el tanque
                    Grande = True
                    #mientras sea mas grande que el tanque y haya tanques disponibles
                    while ((Grande == True) and (len(bodega.tanques_capacidad(tamano)) > 0)):
                        #selecciona el primer tanque disponible
                        Td = bodega.tanques_capacidad(tamano)[0]
                        #si la cantidad es mayor que el 95% del tanque
                        if cantidad_6000[Nbodega][Ncepa] > tamano*0.95:
                            Td.fermentar(tamano*0.95, dia_actual, Ncepa, 6000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_6000[Nbodega][Ncepa] -= tamano*0.95
                            resumen.porcentaje_tanque.append(0.95)
                        #si la cantidad es mayor que el 75% del tanque
                        elif tamano*0.75 <= cantidad_6000[Nbodega][Ncepa] <= tamano*0.95:
                            Td.fermentar(cantidad_6000[Nbodega][Ncepa], dia_actual, Ncepa, 6000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.porcentaje_tanque.append(cantidad_6000[Nbodega][Ncepa]/tamano)
                            cantidad_6000[Nbodega][Ncepa] -= cantidad_6000[Nbodega][Ncepa]
                            resumen.dias_generados.append(Td.generado)
                            Grande = False
                        #si la cantidad es menor que el 75% del tanque
                        elif cantidad_6000[Nbodega][Ncepa] < tamano*0.75:
                            Grande = False
        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por precio
            for Ncepa in cantidad_3000[Nbodega]:
                for tamano in tamanos_T:
                    Grande = True
                    while ((Grande == True) and (len(bodega.tanques_capacidad(tamano)) > 0)):
                        Td = bodega.tanques_capacidad(tamano)[0]
                        if cantidad_3000[Nbodega][Ncepa] > tamano*0.95:
                            Td.fermentar(tamano*0.95, dia_actual, Ncepa, 3000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            cantidad_3000[Nbodega][Ncepa] -=tamano*0.95
                            resumen.dias_generados.append(Td.generado)
                            resumen.porcentaje_tanque.append(0.95)
                        elif tamano*0.75 <= cantidad_3000[Nbodega][Ncepa] <= tamano*0.95:
                            Td.fermentar(cantidad_3000[Nbodega][Ncepa], dia_actual, Ncepa, 3000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.porcentaje_tanque.append(cantidad_3000[Nbodega][Ncepa]/tamano)
                            cantidad_3000[Nbodega][Ncepa] -= cantidad_3000[Nbodega][Ncepa]
                            Grande = False
                            resumen.dias_generados.append(Td.generado)

                        elif cantidad_3000[Nbodega][Ncepa] < tamano*0.75:
                            Grande = False

        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por precio
            for Ncepa in cantidad_1000[Nbodega]:
                for tamano in tamanos_T:
                    Grande = True
                    while ((Grande == True) and (len(bodega.tanques_capacidad(tamano)) > 0)):
                        Td=bodega.tanques_capacidad(tamano)[0]
                        if cantidad_1000[Nbodega][Ncepa] > tamano*0.95:
                            Td.fermentar(tamano*0.95, dia_actual, Ncepa, 1000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            cantidad_1000[Nbodega][Ncepa] -= tamano*0.95
                            resumen.dias_generados.append(Td.generado)
                            resumen.porcentaje_tanque.append(0.95)
                        elif tamano*0.75 <= cantidad_1000[Nbodega][Ncepa] <= tamano*0.95:
                            Td.fermentar(cantidad_1000[Nbodega][Ncepa], dia_actual, Ncepa, 1000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.porcentaje_tanque.append(cantidad_1000[Nbodega][Ncepa]/tamano)
                            cantidad_1000[Nbodega][Ncepa] -= cantidad_1000[Nbodega][Ncepa]
                            Grande = False
                            resumen.dias_generados.append(Td.generado)

                        elif cantidad_1000[Nbodega][Ncepa] < tamano*0.75:
                            Grande = False
                            
        sobras = 0
        for i in cantidad_1000:
            for j in cantidad_1000[i]:
                sobras+=cantidad_1000[i][j]
                resumen.sobras_cepas_bodega[i][j] += cantidad_1000[i][j]
                resumen.sobras_1000[i][j] += cantidad_1000[i][j]
                if cantidad_1000[i][j] != 0:
                    resumen.sobras_cantidad_dia.append(cantidad_1000[i][j])
        resumen.sobras+=sobras
        if sobras != 0:
            resumen.agregar_sobrante(dia_actual, sobras, 1000)

        sobras = 0
        for i in cantidad_3000:
            for j in cantidad_3000[i]:
                sobras += cantidad_3000[i][j]
                resumen.sobras_cepas_bodega[i][j] += cantidad_3000[i][j]
                resumen.sobras_3000[i][j] += cantidad_3000[i][j]
                if cantidad_3000[i][j] != 0:
                    resumen.sobras_cantidad_dia.append(cantidad_3000[i][j])

        resumen.sobras+=sobras

        if sobras != 0:
            resumen.agregar_sobrante(dia_actual, sobras, 3000)

        sobras = 0
        for i in cantidad_6000:
            for j in cantidad_6000[i]:
                sobras+=cantidad_6000[i][j]
                resumen.sobras_cepas_bodega[i][j] += cantidad_6000[i][j]
                resumen.sobras_6000[i][j] += cantidad_6000[i][j]
                if cantidad_6000[i][j] != 0:
                    resumen.sobras_cantidad_dia.append(cantidad_6000[i][j])
        resumen.sobras+=sobras

        if sobras != 0:
            resumen.agregar_sobrante(dia_actual, sobras, 6000)
        sobras = 0
        if len(resumen.dias[dia_actual]) > 0:
            print(resumen.dias[dia_actual])
            pass

        
        cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        dia_actual = dia_actual + 1

    #Se imprime el resumen de todo lo fermentado y sobras
    resumen.imprimir_resumen()
    #RESUMENES.append(resumen)
    #resumen=0


#dias promedio de fermentacion (yo)) -listo
#llenado promedio(yo)-listo
#toneladas no cosechadas(yo) -listo
#revisar como llenar tanques (funcion,heuristicas) (Martin)

#costos(fermentacion, dia optimo, perdidas) 
#llenar excel (fermentado, kpis, cosechado etc)
