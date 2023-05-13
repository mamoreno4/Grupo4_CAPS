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

df = pd.read_csv('solucion_18_dias.csv')
ssss=0
sssss=0
Cuart = pd.read_excel('Datos Base Ordenados (Cosecha).xlsx')
Los_Cuarteles = []
for i in range(1,65):
    CT = Cuartel(Cuart.iloc[i-1])
    D = df.where(df["Cuartel"] == "cuartel_"+str(i))
    D = D.dropna()
    for j in range(len(D)):
        V = D.iloc[j]["Valor"]
        BB = D.iloc[j]["Bodega"]
        DIA = int(D.iloc[j]["Dia"][4:])
        CT.agregar_cosecha(DIA,[BB,V])
    Los_Cuarteles.append(CT)

Las_Bodegas = []
Bodegas = pd.read_excel("Datos base G4.xlsx",sheet_name="Bodega Machali")
b=Bodega(Bodegas,"Machali")
Las_Bodegas.append(b)
Bodegas = pd.read_excel("Datos base G4.xlsx",sheet_name="Bodega Chépica")
b=Bodega(Bodegas,"Chepica")
Las_Bodegas.append(b)
Bodegas = pd.read_excel("Datos base G4.xlsx",sheet_name="Bodega Nancagua")
b=Bodega(Bodegas,"Nancagua")
Las_Bodegas.append(b)


dia_actual = 1
#Cantidad de cosecha por bodega y cepa
#dictionary = {'key':value}
cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
#tamaño de tanques para iterar
tamanos_T = [100,75,50,30]
RESUMENES=[]
#Iterar seeds
for u in range(100):
    dia_actual = 1
    resumen = Resumen()
    seed=21234+u
    resumen.seed = seed
    scipy_randomGen = binom
    numpy_randomGen = Generator(PCG64(seed))
    binom.random_state=numpy_randomGen
    while ((dia_actual < 150)):
        #print("Dia " + str(dia_actual))
        for bodega in Las_Bodegas:
            salidas = bodega.revisar_tanques(dia_actual)
            resumen.dias_ocupado_tanques.append(len(bodega.tanques_fermentando)/len(bodega.tanques))
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
        despreciacion_1000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
        despreciacion_3000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
        despreciacion_6000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
        for cuartel in Los_Cuarteles: 
                if len(cuartel.cosecha_por_dia[dia_actual]) > 0:
                    for i in cuartel.cosecha_por_dia[dia_actual]:
                        if i[1] > 1:
                            resumen.cosechado +=i[1]
                        if cuartel.precio == 1000:
                            cantidad_1000[i[0]][cuartel.variedad] += i[1]
                            despreciacion=cuartel.gen_desp(dia_actual,1000)
                            resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]*0.001
                            if despreciacion<despreciacion_1000[i[0]][cuartel.variedad]:
                                despreciacion_1000[i[0]][cuartel.variedad]=despreciacion
                        elif cuartel.precio == 3000:
                            cantidad_3000[i[0]][cuartel.variedad] += i[1]
                            despreciacion=cuartel.gen_desp(dia_actual,3000)
                            resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]*0.001
                            if despreciacion<despreciacion_3000[i[0]][cuartel.variedad]:
                                despreciacion_3000[i[0]][cuartel.variedad]=despreciacion
                        elif cuartel.precio == 6000:
                            cantidad_6000[i[0]][cuartel.variedad] += i[1]
                            despreciacion=cuartel.gen_desp(dia_actual,6000)
                            resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]*0.001
                            if despreciacion<despreciacion_6000[i[0]][cuartel.variedad]:
                                despreciacion_6000[i[0]][cuartel.variedad]=despreciacion
                        else:
                            print("Error en precio")
                            pass
                else:
                    pass
        #Iterar bodegas
        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por precio
            for Ncepa in cantidad_6000[Nbodega]:
                tanks = []
                if cantidad_6000[Nbodega][Ncepa]>=30*0.75:
                    for i in bodega.tanques_disponibles:
                        tanks.append((i,i.capacidad))
                    tanks = sorted(tanks, key=lambda x: x[1], reverse=True)
                    print("Revisar tanques")
                    print("Cantidad: " + str(cantidad_6000[Nbodega][Ncepa]))
                    print("Bodega: " + Nbodega)
                    print("Cepa: " + Ncepa)
                    print("precio: 6000")
                    print("Tanques disponibles:")
                    for i in tanks:
                        print(i[1])
                    print("testeo")
                    result=fill_tanks(tanks, cantidad_6000[Nbodega][Ncepa])
                    print("nuevo resultado")
                    print(result)                            
                    if result:
                        for Td, fill_amount in result:
                            Td.fermentar(fill_amount, dia_actual, Ncepa, 6000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_6000[Nbodega][Ncepa] -= fill_amount
                            resumen.porcentaje_tanque.append(fill_amount/Td.capacidad)
                            resumen.costo_dias+=fill_amount*25*Td.generado*1000
                            resumen.ganancias+=fill_amount*1000*6000*despreciacion_6000[Nbodega][Ncepa]

                            print(Td,fill_amount)
                            print(cantidad_6000[Nbodega][Ncepa])
                tanks = []
                if cantidad_6000[Nbodega][Ncepa]>=30*0.75:
                    for i in bodega.tanques_disponibles:
                        tanks.append((i,i.capacidad))
                    tanks = sorted(tanks, key=lambda x: x[1], reverse=True)
                    print("Revisar tanques")
                    print("Cantidad: " + str(cantidad_6000[Nbodega][Ncepa]))
                    print("Bodega: " + Nbodega)
                    print("Cepa: " + Ncepa)
                    print("precio: 6000")
                    print("Tanques disponibles:")
                    for i in tanks:
                        print(i[1])
                    print("testeo")
                    result=comb_liquido(tanks, cantidad_6000[Nbodega][Ncepa])
                    print("nuevo resultado")
                    print(result)                            
                    if result:
                        for Td, fill_amount in result:
                            Td.fermentar(fill_amount, dia_actual, Ncepa, 6000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_6000[Nbodega][Ncepa] -= fill_amount
                            resumen.porcentaje_tanque.append(fill_amount/Td.capacidad)
                            resumen.costo_dias+=fill_amount*25*Td.generado*1000
                            resumen.ganancias+=fill_amount*1000*6000*despreciacion_6000[Nbodega][Ncepa]
                            print(Td,fill_amount)
                            print(cantidad_6000[Nbodega][Ncepa])
                    
        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por precio
            for Ncepa in cantidad_3000[Nbodega]:
                tanks = []
                if cantidad_3000[Nbodega][Ncepa]>=30*0.75:
                    for i in bodega.tanques_disponibles:
                        tanks.append((i,i.capacidad))
                    tanks = sorted(tanks, key=lambda x: x[1], reverse=True)
                    print("Revisar tanques")
                    print("Cantidad: " + str(cantidad_3000[Nbodega][Ncepa]))
                    print("Bodega: " + Nbodega)
                    print("Cepa: " + Ncepa)
                    print("precio: 3000")
                    print("Tanques disponibles:")
                    for i in tanks:
                        print(i[1])
                    print("testeo")
                    result=fill_tanks(tanks, cantidad_3000[Nbodega][Ncepa])
                    print("nuevo resultado")
                    print(result)                            
                    if result:
                        for Td, fill_amount in result:
                            Td.fermentar(fill_amount, dia_actual, Ncepa, 3000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_3000[Nbodega][Ncepa] -= fill_amount
                            resumen.porcentaje_tanque.append(fill_amount/Td.capacidad)
                            resumen.costo_dias+=fill_amount*25*Td.generado*1000
                            resumen.ganancias+=fill_amount*1000*3000*despreciacion_3000[Nbodega][Ncepa]
                            print(Td,fill_amount)
                            print(cantidad_3000[Nbodega][Ncepa])
                tanks = []
                if cantidad_3000[Nbodega][Ncepa]>=30*0.75:
                    for i in bodega.tanques_disponibles:
                        tanks.append((i,i.capacidad))
                    tanks = sorted(tanks, key=lambda x: x[1], reverse=True)
                    print("Revisar tanques")
                    print("Cantidad: " + str(cantidad_3000[Nbodega][Ncepa]))
                    print("Bodega: " + Nbodega)
                    print("Cepa: " + Ncepa)
                    print("precio: 3000")
                    print("Tanques disponibles:")
                    for i in tanks:
                        print(i[1])
                    print("testeo")
                    result=comb_liquido(tanks, cantidad_3000[Nbodega][Ncepa])
                    print("nuevo resultado")
                    print(result)                            
                    if result:
                        for Td, fill_amount in result:
                            Td.fermentar(fill_amount, dia_actual, Ncepa, 3000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_3000[Nbodega][Ncepa] -= fill_amount
                            resumen.porcentaje_tanque.append(fill_amount/Td.capacidad)
                            resumen.costo_dias+=fill_amount*25*Td.generado*1000
                            resumen.ganancias+=fill_amount*1000*3000*despreciacion_3000[Nbodega][Ncepa]

                            print(Td,fill_amount)
                            print(cantidad_3000[Nbodega][Ncepa])
                
        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por precio
            for Ncepa in cantidad_1000[Nbodega]:
                tanks = []
                if cantidad_1000[Nbodega][Ncepa]>=30*0.75:
                    for i in bodega.tanques_disponibles:
                        tanks.append((i,i.capacidad))
                    tanks = sorted(tanks, key=lambda x: x[1], reverse=True)
                    print("Revisar tanques")
                    print("Cantidad: " + str(cantidad_1000[Nbodega][Ncepa]))
                    print("Bodega: " + Nbodega)
                    print("Cepa: " + Ncepa)
                    print("precio: 1000")
                    print("Tanques disponibles:")
                    for i in tanks:
                        print(i[1])
                    print("testeo")
                    result=fill_tanks(tanks, cantidad_1000[Nbodega][Ncepa])
                    print("nuevo resultado")
                    print(result)                            
                    if result:
                        for Td, fill_amount in result:
                            Td.fermentar(fill_amount, dia_actual, Ncepa, 1000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_1000[Nbodega][Ncepa] -= fill_amount
                            resumen.porcentaje_tanque.append(fill_amount/Td.capacidad)
                            resumen.costo_dias+=fill_amount*25*Td.generado*1000
                            resumen.ganancias+=fill_amount*1000*1000*despreciacion_1000[Nbodega][Ncepa]

                            print(Td,fill_amount)
                            print(cantidad_1000[Nbodega][Ncepa])
                tanks = []
                if cantidad_1000[Nbodega][Ncepa]>=30*0.75:
                    for i in bodega.tanques_disponibles:
                        tanks.append((i,i.capacidad))
                    tanks = sorted(tanks, key=lambda x: x[1], reverse=True)
                    print("Revisar tanques")
                    print("Cantidad: " + str(cantidad_1000[Nbodega][Ncepa]))
                    print("Bodega: " + Nbodega)
                    print("Cepa: " + Ncepa)
                    print("precio: 1000")
                    print("Tanques disponibles:")
                    for i in tanks:
                        print(i[1])
                    print("testeo")
                    result=comb_liquido(tanks, cantidad_1000[Nbodega][Ncepa])
                    print("nuevo resultado")
                    print(result)                            
                    if result:
                        for Td, fill_amount in result:
                            Td.fermentar(fill_amount, dia_actual, Ncepa, 1000, Distribuciones)
                            bodega.agregar_tanque_fermentando(Td)
                            resumen.dias_generados.append(Td.generado)
                            cantidad_1000[Nbodega][Ncepa] -= fill_amount
                            resumen.porcentaje_tanque.append(fill_amount/Td.capacidad)
                            resumen.costo_dias+=fill_amount*25*Td.generado*1000
                            resumen.ganancias+=fill_amount*1000*1000*despreciacion_1000[Nbodega][Ncepa]

                            print(Td,fill_amount)
                            print(cantidad_1000[Nbodega][Ncepa])
                
                            
                            
        sobras = 0
        for i in cantidad_1000:
            for j in cantidad_1000[i]:
                sobras+=cantidad_1000[i][j]
                resumen.sobras_cepas_bodega[i][j] += cantidad_1000[i][j]
                resumen.sobras_1000[i][j] += cantidad_1000[i][j]
                if cantidad_1000[i][j] != 0:
                    resumen.sobras_cantidad_dia.append(cantidad_1000[i][j])
                    resumen.costo_sobras+=cantidad_1000[i][j]*10*1000*1000
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
                    resumen.costo_sobras+=cantidad_3000[i][j]*10*3000*1000

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
                    resumen.costo_sobras+=cantidad_6000[i][j]*10*6000*1000
        resumen.sobras+=sobras

        if sobras != 0:
            resumen.agregar_sobrante(dia_actual, sobras, 6000)
        sobras = 0
        if len(resumen.dias[dia_actual]) > 0:
            #print(resumen.dias[dia_actual])
            pass

        
        cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        dia_actual +=1

    #Se imprime el resumen de todo lo fermentado y sobrasa
    #resumen.imprimir_resumen()
    RESUMENES.append(resumen)
    #resumen=0

crear_excel("prueba 18 dias",RESUMENES)
#dias promedio de fermentacion (yo)) -listo
#llenado promedio(yo)-listo
#toneladas no cosechadas(yo) -listo
#revisar como llenar tanques (funcion,heuristicas) (Martin)

#costos(fermentacion, dia optimo, perdidas) 
#llenar excel (fermentado, kpis, cosechado etc) -listo
