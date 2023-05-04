import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import clases_simulacion as cs


Distribuciones= pd.read_excel('./../Distribuciones/dist.xlsx', index_col=0)


df = pd.read_csv('solucion.csv')

Cuart= pd.read_excel('Datos Base Ordenados (Cosecha).xlsx')
Los_Cuarteles=[]
for i in range(1,60):
    CT=cs.Cuartel(Cuart.iloc[i])
    D=df.where(df["Cuartel"]=="cuartel_"+str(i))
    D=D.dropna()
    for j in range(len(D)):
        V=D.iloc[j]["Valor"]
        BB=D.iloc[j]["Bodega"]
        DIA=int(D.iloc[j]["Dia"][4:])
        CT.agregar_cosecha(DIA,[V,BB])
    Los_Cuarteles.append(CT)

Bodegas=pd.read_excel("Datos base G4 (2).xlsx",sheet_name="Tanques")
Las_Bodegas=[]
for i in range(3):
    BT=cs.Bodega(Bodegas.iloc[i])
    Las_Bodegas.append(BT)




# main

dia_actual = 1
#Cantidad de cosecha por bodega y cepa
#dictionary = {'key':value}
cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
#tamaño de tanques para iterar
tamanos_T = [100,75,50,30]
while ((dia_actual < 60)):
    print("Dia " + str(dia_actual))
    for bodega in Las_Bodegas:
        salidas = bodega.revisar_tanques(dia_actual)
        if len(salidas) == 0:
            #print("No hubo salidas en la bodega " + bodega.ubicacion)
            pass
        else:
            for salida in salidas:
                #Resumen.agregar_fermentado(dia_actual, salida)
                pass
    #revisar cosecha diaria por cuartel y precio
    for cuartel in Los_Cuarteles:
        if dia_actual in cuartel.cosecha_por_dia.keys():
            if cuartel.precio == 1000:
                CD=cuartel.cosecha_por_dia[dia_actual]
                Nueva=CD[1]
                CCC=cantidad_1000[CD[0]][cuartel.variedad]
                CN=Nueva+CCC
                cantidad_1000[CD[0]][cuartel.variedad] = CN
            elif cuartel.precio == 3000:
                CD=cuartel.cosecha_por_dia[dia_actual]
                Nueva=CD[1]
                CCC=cantidad_1000[CD[0]][cuartel.variedad]
                CN=Nueva+CCC
                cantidad_3000[CD[0]][cuartel.variedad] = CN
            elif cuartel.precio == 6000:
                CD=cuartel.cosecha_por_dia[dia_actual]
                Nueva=CD[1]
                CCC=cantidad_1000[CD[0]][cuartel.variedad]
                CN=Nueva+CCC
                cantidad_6000[CD[0]][cuartel.variedad] = CN

        #iterar bodegas
    for bodega in Las_Bodegas:
        #establecer bodega actual
        Nbodega=bodega.ubicacion
        #iterar por precio
        for Ncepa in cantidad_6000[Nbodega]:
            #iterar por tamaño de tanque
            for tamano in tamanos_T:
                #boleano para saber si es mas grande que el tanque
                Grande=True
                #mientras sea mas grande que el tanque y haya tanques disponibles
                while Grande==True and len(bodega.tanques_capacidad(tamano))>0:
                    #selecciona el primer tanque disponible
                    Td=bodega.tanques_capacidad(tamano)[0]
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
                while Grande==True and len(bodega.tanques_capacidad(tamano))>0:
                    Td=bodega.tanques_capacidad(tamano)[0]
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
                while Grande==True and len(bodega.tanques_capacidad(tamano))>0:
                    Td=bodega.tanques_capacidad(tamano)[0]
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
    
    cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
    cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
    cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
    dia_actual = dia_actual + 1