from random import uniform, seed, randint, gauss
from numpy.random import Generator, PCG64
import numpy as np
import pandas as pd
from scipy.stats import binom
from clases_simulacion import *
import time
inicio = time.time()
#Archivo Main para la simulacion
#Nesecita cargar los datos de las distribuciones, los cuarteles, las bodegas y los trabajadores
#Código a medir
time.sleep(1)
# ------------------------------------------------------------

# ------------------------------------------------------------
#inicializar variables
dia_actual = 1
largo_periodo = 7
#Crear resumen
resumen = Resumen()
resumen.costo_trabajo = 0
#setear escenario
seed=21235
resumen.seed = seed
scipy_randomGen = binom
numpy_randomGen = Generator(PCG64(seed))
binom.random_state=numpy_randomGen
# ------------------------------------------------------------
#Poblar clases
Distribuciones,Los_Cuarteles,Las_Bodegas,RESUMENES=crear_clases()
#VER COMO LEER DATOS GUROBI
diccionario_datos_estanques=leer_gurobi(Los_Cuarteles)

#Iterar dias
while (dia_actual <= largo_periodo):
    #Cantidad de cosecha por bodega y cepa
    #dictionary = {'key':value}
    cantidad_1000 = {'Machali':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Chepica':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Nancagua':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}}
    cantidad_3000 = {'Machali':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Chepica':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Nancagua':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}}
    cantidad_6000 = {'Machali':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Chepica':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Nancagua':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}}
    print("Dia " + str(dia_actual))
    #Revisar fermentacion saliente diaria por bodega
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
        # ------------------------------------------------------------
        #REVISAR SI FALLO ALGO (BRREAK?)

    #crear diccionarios de despreciacion de la uva, segun dia cosechado
    despreciacion_1000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
    despreciacion_3000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
    despreciacion_6000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
    #Revisar cosecha diaria por cuartel y precio
    for cuartel in Los_Cuarteles:
            #si la cantidad de cosecha del dia por cuartel es mayor a 0 continuar
            if len(cuartel.cosecha_por_dia[dia_actual]) > 0:
                for i in cuartel.cosecha_por_dia[dia_actual]:
                    #agregar cosecha al resumen
                    if i[1] > 1:
                        resumen.cosechado +=i[1]
                    #agregar cosecha por precio al diccionario con las bodegas y cepas del dia
                    if cuartel.precio == 1000:
                        cantidad_1000[i[0]][cuartel.variedad] += i[1]
                        #revisar despreciacion de la uva
                        despreciacion=cuartel.gen_desp(dia_actual,1000)
                        #agregar costo de transporte al resumen
                        resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]
                        #si la despreciacion es menor a la despreciacion actual, reemplazar
                        if despreciacion<despreciacion_1000[i[0]][cuartel.variedad]:
                            despreciacion_1000[i[0]][cuartel.variedad]=despreciacion
                    elif cuartel.precio == 3000:
                        cantidad_3000[i[0]][cuartel.variedad] += i[1]
                        despreciacion=cuartel.gen_desp(dia_actual,3000)
                        resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]
                        if despreciacion<despreciacion_3000[i[0]][cuartel.variedad]:
                            despreciacion_3000[i[0]][cuartel.variedad]=despreciacion
                    elif cuartel.precio == 6000:
                        cantidad_6000[i[0]][cuartel.variedad] += i[1]
                        despreciacion=cuartel.gen_desp(dia_actual,6000)
                        resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]
                        if despreciacion<despreciacion_6000[i[0]][cuartel.variedad]:
                            despreciacion_6000[i[0]][cuartel.variedad]=despreciacion
                    else:
                        print("Error en precio")
                        pass
            else:
                pass
    #PONER AQUI EL CODIGO PARA USAR LOS TANQUES
    #REVISAR SI FALLO ALGO (BRREAK?)




    if len(resumen.dias[dia_actual]) > 0:
        print(resumen.dias[dia_actual])
        pass

    #restablecer cosecha del dia
    dia_actual +=1

#Se imprime el resumen de todo lo fermentado y sobrasa
#resumen.imprimir_resumen()
RESUMENES.append(resumen)
fin = time.time()
print(fin-inicio) # 1.0005340576171875
# ------------------------------------------------------------

dia_inicio=dia_actual
largo_periodo=7
estanques_ocupados_actual=pasar_tanques_dict(Las_Bodegas,dia_actual)
total_cosechar_actual=pasar_cuartel_dict(Los_Cuarteles)


#crear_excel("solucion_robusta2",RESUMENES)
# ------------------------------------------------------------
#DEVOLVER FEEDBACK



