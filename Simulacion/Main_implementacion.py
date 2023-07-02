from random import uniform, seed, randint, gauss
from numpy.random import Generator, PCG64
import numpy as np
import pandas as pd
from scipy.stats import binom
from clases_simulacion import *
import time
from pp import *
inicio = time.time()
#Archivo Main para la simulacion
#Nesecita cargar los datos de las distribuciones, los cuarteles, las bodegas y los trabajadores
#Los archivos estan en path relativos
#Para cambiarlos dirigirse a la funcion crear_clases() en el archivo clases_simulacion.py
# ------------------------------------------------------------

#Código a medir
time.sleep(1)
#Escenario random
escenario=2123660
# ------------------------------------------------------------
#Cantidad de simulaciones actuales
Cantidad_simulaciones=0
#Cantidad de simulaciones objetivo
Cantidad_simulaciones_objetivo=10
#Lista con los resumenes de cada simulacion
RESUMENES=[]
# ------------------------------------------------------------
#Inicializacion de la simulacion
while Cantidad_simulaciones<Cantidad_simulaciones_objetivo:
    #iniciar tiempo de simulacion
    ini=time.time()
    #Aumentar cantidad de simulaciones
    Cantidad_simulaciones+=1
    print("Simulacion " + str(Cantidad_simulaciones))
    #inicializar variables
    # ------------------------------------------------------------
    #Variables de la simulacion
    dia_actual = 1
    # Largo de periodo del horizonte de planificacion
    largo_periodo = 23
    # Gap objetivo al alcanzar
    gap = 0.005
    # Tiempo limite de ejecucion en segundos (20 minutos) por iteracion de gurobi
    time_limit = 1200
    #Crear resumen
    resumen = Resumen()
    resumen.costo_trabajo = 0
    #setear escenario
    escenario+=1
    seed=escenario
    resumen.seed = seed
    # ------------------------------------------------------------
    #Entregar semilla a las distribuciones
    scipy_randomGen = binom
    numpy_randomGen = Generator(PCG64(seed))
    binom.random_state=numpy_randomGen
    # ------------------------------------------------------------
    #Poblar clases con datos
    Distribuciones,Los_Cuarteles,Las_Bodegas=crear_clases()
    resumen.agregar_cosechaT(Los_Cuarteles)
    estanques_ocupados,tanques_relidad=pasar_tanques_dict(Las_Bodegas,dia_actual,largo_periodo)
    total_cosechar=pasar_cuartel_dict(Los_Cuarteles)
    trab=[]
    # Contador de dias de viavilidad de la planificacion
    contador=1
    # Variables de control de la simulacion
    diferencia=False
    fermentando=False
    # ------------------------------------------------------------
    # Listas de seguimiento de la simulacion
    Cosecha_dia_ex=[[],[],[]]
    fermentado_dia_ex=[[],[],[],[]]
    trab_dia_ex=[[],[],[]]
    #Iterar dias
    while (dia_actual <= 79 or fermentando == True):
        #Cantidad de cosecha por bodega y cepa
        #dictionary = {'key':value}
        cantidad_1000 = {'Machali':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Chepica':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Nancagua':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}}
        cantidad_3000 = {'Machali':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Chepica':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Nancagua':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}}
        cantidad_6000 = {'Machali':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Chepica':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}, 'Nancagua':{'CS':0, 'S':0, 'C':0, 'G':0, 'CF':0, 'M':0, 'SB':0, 'Ch':0, 'V':0}}
        print("Dia " + str(dia_actual))
        #Revisar fermentacion saliente diaria por bodega
        for bodega in Las_Bodegas:
            # Revisa si hay salidas de fermentado en la bodega
            salidas = bodega.revisar_tanques(dia_actual)
            resumen.dias_ocupado_tanques.append(len(bodega.tanques_fermentando)/len(bodega.tanques))
            if len(salidas) == 0:
                #print("No hubo salidas en la bodega " + bodega.ubicacion)
                pass
            else:
                for salida in salidas:
                    # Agregar a resumen las salidas de fermentado
                    resumen.agregar_fermentado(dia_actual, salida)
                    resumen.fermentado += salida[0]
                    if salida[3] == 1000:
                        resumen.fermentado_1000[bodega.ubicacion][salida[1]] += salida[0]
                    elif salida[3] == 3000:
                        resumen.fermentado_3000[bodega.ubicacion][salida[1]] += salida[0]
                    elif salida[3] == 6000:
                        resumen.fermentado_6000[bodega.ubicacion][salida[1]] += salida[0]
                    pass
        #Revisar si los tanques correspondientes esta disponibles
        if (dia_actual != 1):
            print("Revisar si los tanques correspondientes esta disponibles")
            if contador>=10:
                estanques_ocupados,tanques_relidad=pasar_tanques_dict(Las_Bodegas,dia_actual,largo_periodo)
            revisado=revisar_input(dict_diario,estanques_ocupados,Las_Bodegas,dia_actual)
            # Si hay diferencia entre los tanques ocupados y los que deberian estar ocupados
            if len(revisado)>=1:
                print("DIFERENCIA")
                #print(revisado)
                diferencia=True
                # Por cada tanque que existe diferencia, se actualiza el diccionario
                for i in revisado:
                    if i[1]=='tanque ocupado':
                        t="estanque_"+str(i[0].ubicacion.lower())+"_"+str(i[0].id)
                        for i in dict_diario["dia_"+str(dia_actual)]:
                            if i["Estanque"]==t:
                                dict_diario["dia_"+str(dia_actual)].pop(dict_diario["dia_"+str(dia_actual)].index(i))
            else:
                #Aumenta el contador de dias de viabilidad de la planificacion
                contador+=1
        #Revisar si hay que llamar a gurobi
        if (dia_actual <= 1 or diferencia==True or contador>=10):
            # Si hay que llamar a gurobi
            # revisar si el dia actual es el ultimo dia de la planificacion
            if (dia_actual <= 79):
                print("Hora de optimizar")
                # Aumentar cantidad de optimizaciones realizadas en el resumen
                resumen.sim+=1
                # Pasar el estado actual de los tanques a un diccionario
                estanques_ocupados,tanques_relidad=pasar_tanques_dict(Las_Bodegas,dia_actual,largo_periodo)
                # Pasar los cuarteles a un diccionario
                total_cosechar=pasar_cuartel_dict(Los_Cuarteles)
                for a in Los_Cuarteles:
                    for i in range(1,100):
                        a.cosecha_por_dia[i]=[]
                # Llamar a gurobi
                cosecha, trabajadores, estanques = optimizacion_cosecha(dia_actual,largo_periodo,estanques_ocupados, total_cosechar, gap,time_limit)
                # Leer el output de gurobi
                dict_diario=pasar_tanques_a_diario(estanques)
                estanques_ocupados,tanques_relidad=pasar_tanques_dict(Las_Bodegas,dia_actual,largo_periodo)
                trab=leer_gurobi(Los_Cuarteles,cosecha,trabajadores)
                # Diferencia es falso
                diferencia=False
                # Reiniciar el contador de dias de viabilidad de la planificacion
                contador=1
        # Agregar costos de trabajadores al resumen
        for i in trab:
            if i["Dia"]=="dia_"+str(dia_actual):
                trab_dia_ex[0].append("Dia "+str(dia_actual))
                trab_dia_ex[1].append(i["Cuartel"])
                trab_dia_ex[2].append(i["Valor"])
                resumen.costo_trabajo+=i["Valor"]
            



        #crear diccionarios de despreciacion de la uva, segun dia cosechado
        despreciacion_1000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
        despreciacion_3000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
        despreciacion_6000 = {'Machali':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Chepica':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}, 'Nancagua':{'G':1, 'Ch':1, 'SB':1, 'C':1, 'CS':1, 'S':1, 'M':1, 'CF':1, 'V':1}}
        #Revisar cosecha diaria por cuartel y precio
        for cuartel in Los_Cuarteles:
                #si la cantidad de cosecha del dia por cuartel es mayor a 0 continuar
                #print(cuartel.cosecha_por_dia[dia_actual])
                if len(cuartel.cosecha_por_dia[dia_actual]) > 0:
                    for i in cuartel.cosecha_por_dia[dia_actual]:
                        #agregar cosecha al resumen
                        if i[1] > 1:
                            Cosecha_dia_ex[0].append("Dia "+str(dia_actual))
                            Cosecha_dia_ex[1].append(str(cuartel))
                            Cosecha_dia_ex[2].append(str(i[1]))
                            resumen.cosechado +=i[1]
                            print(cuartel)
                            print(cuartel.cosechable)
                            cuartel.cosechable -= i[1]
                            print(i[1])
                            print(cuartel.cosechable)
                            if cuartel.cosechable < 0.001:
                                cuartel.cosechable = 0
                                print("Cuartel " + str(cuartel)+" cosechado")
                        #agregar cosecha por precio al diccionario con las bodegas y cepas del dia
                        if cuartel.precio == 1000:
                            cantidad_1000[i[0]][cuartel.variedad] += round(i[1],2)
                            #revisar despreciacion de la uva
                            despreciacion=cuartel.gen_desp(dia_actual,1000)
                            #agregar costo de transporte al resumen
                            resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]*1000
                            #si la despreciacion es menor a la despreciacion actual, reemplazar
                            if despreciacion<despreciacion_1000[i[0]][cuartel.variedad]:
                                despreciacion_1000[i[0]][cuartel.variedad]=despreciacion
                        elif cuartel.precio == 3000:
                            cantidad_3000[i[0]][cuartel.variedad] += round(i[1],2)
                            despreciacion=cuartel.gen_desp(dia_actual,3000)
                            resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]*1000
                            if despreciacion<despreciacion_3000[i[0]][cuartel.variedad]:
                                despreciacion_3000[i[0]][cuartel.variedad]=despreciacion
                        elif cuartel.precio == 6000:
                            cantidad_6000[i[0]][cuartel.variedad] += round(i[1],2)
                            despreciacion=cuartel.gen_desp(dia_actual,6000)
                            resumen.costo_transporte += cuartel.transporte[i[0]]*i[1]*1000
                            if despreciacion<despreciacion_6000[i[0]][cuartel.variedad]:
                                despreciacion_6000[i[0]][cuartel.variedad]=despreciacion
                        else:
                            print("Error en precio")
                            pass
                else:
                    pass
                
        #Revisar cosecha diaria por bodega y cepa
        for bodega in Las_Bodegas:
            #establecer bodega actual
            Nbodega = bodega.ubicacion
            #iterar por cepa y precio
            for Ncepa in cantidad_6000[Nbodega]:
                #calidad de la uva
                calidad=6000
                #cantidad de uva
                cantidad=cantidad_6000[Nbodega][Ncepa]
                #si la cantidad es mayor a al tamaño mas pequeño continuar
                if cantidad>=30*0.75:
                    #dia actual
                    dia="dia_"+str(dia_actual)
                    tanques_a_usar=tanques_dia(dia,Nbodega,Ncepa,dict_diario,calidad)
                    tanks=[]
                    # iterar por tanques a usar
                    for i in tanques_a_usar:
                        id=int(i[3])
                        TTT=bodega.devolver_tanque_id(id)
                        tanks.append((TTT,TTT.capacidad))
                        #print("El tanque "+str(TTT)+" tiene "+str(TTT.capacidad)+" litros y su estado es"+str(TTT.estado) )
                    #LLamar a la funcion que combina tanques
                    result=comb_liquido(tanks, cantidad)
                    #print("TANQUES A USAR dia "+str(dia_actual)+" bodega "+str(Nbodega)+" cepa "+str(Ncepa)+" calidad "+str(calidad) )
                    #print(result)
                    #print(tanques_a_usar)
                    #si la funcion comb_liquido retorna algo
                    if result:
                        #Agregar datos
                        fermentado_dia_ex[0].append("Dia "+str(dia_actual))
                        fermentado_dia_ex[1].append(str(Ncepa))
                        fermentado_dia_ex[2].append(str(calidad))
                        fermentado_dia_ex[3].append(result)
                        print("Combina tanques encontrada V1")
                        #iterar por tanques y cantidad de uva
                        # Fermentar segun los resultados de la funcion comb_liquido
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
                    else:
                        print("ERROR: No se pudo combinar tanques")
                        print("TANQUES A USAR dia "+str(dia_actual)+" bodega "+str(Nbodega)+" cepa "+str(Ncepa)+" calidad "+str(calidad) )
                        print(tanques_a_usar)
                        print("RESULT")
            #Igual que el anterior pero con calidad 3000
            for Ncepa in cantidad_3000[Nbodega]:
                calidad=3000
                cantidad=cantidad_3000[Nbodega][Ncepa]
                if cantidad>=30*0.75:
                    dia="dia_"+str(dia_actual)
                    tanques_a_usar=tanques_dia(dia,Nbodega,Ncepa,dict_diario,calidad)
                    tanks=[]
                    for i in tanques_a_usar:
                        id=int(i[3])
                        TTT=bodega.devolver_tanque_id(id)
                        tanks.append((TTT,TTT.capacidad))
                        print("El tanque "+str(TTT)+" tiene "+str(TTT.capacidad)+" litros y su estado es"+str(TTT.estado) )
                    result=comb_liquido(tanks, cantidad)
                    print("TANQUES A USAR dia "+str(dia_actual)+" bodega "+str(Nbodega)+" cepa "+str(Ncepa)+" calidad "+str(calidad) )
                    print(result)
                    #print(tanques_a_usar)
                    if result:
                        fermentado_dia_ex[0].append("Dia "+str(dia_actual))
                        fermentado_dia_ex[1].append(str(Ncepa))
                        fermentado_dia_ex[2].append(str(calidad))
                        fermentado_dia_ex[3].append(result)
                        print("Combina tanques encontrada V1")
                        #iterar por tanques y cantidad de uva
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
                    else:
                        print("ERROR: No se pudo combinar tanques")
                        print("TANQUES A USAR dia "+str(dia_actual)+" bodega "+str(Nbodega)+" cepa "+str(Ncepa)+" calidad "+str(calidad) )
                        print(tanques_a_usar)
                        print("RESULT")
            #Igual que el anterior pero con calidad 1000
            for Ncepa in cantidad_1000[Nbodega]:
                calidad=1000
                cantidad=cantidad_1000[Nbodega][Ncepa]
                if cantidad>=30*0.75:
                    dia="dia_"+str(dia_actual)
                    tanques_a_usar=tanques_dia(dia,Nbodega,Ncepa,dict_diario,calidad)
                    tanks=[]
                    for i in tanques_a_usar:
                        id=int(i[3])
                        TTT=bodega.devolver_tanque_id(id)
                        tanks.append((TTT,TTT.capacidad))
                        print("El tanque "+str(TTT)+" tiene "+str(TTT.capacidad)+" litros y su estado es "+str(TTT.estado) )
                    result=comb_liquido(tanks, cantidad)
                    print(cantidad)
                    print("TANQUES A USAR dia "+str(dia_actual)+" bodega "+str(Nbodega)+" cepa "+str(Ncepa)+" calidad "+str(calidad) )
                    print(result)
                    #print(tanques_a_usar)
                    if result:
                        fermentado_dia_ex[0].append("Dia "+str(dia_actual))
                        fermentado_dia_ex[1].append(str(Ncepa))
                        fermentado_dia_ex[2].append(str(calidad))
                        fermentado_dia_ex[3].append(result)                    
                        print("Combina tanques encontrada V1")
                        #iterar por tanques y cantidad de uva
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
                    else:
                        print("ERROR: No se pudo combinar tanques")
                        print("TANQUES A USAR dia "+str(dia_actual)+" bodega "+str(Nbodega)+" cepa "+str(Ncepa)+" calidad "+str(calidad) )
                        print(tanques_a_usar)
                        print("RESULT")


        #Contar sobras del dia                    
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
        #Termino de contar sobras del dia

        #Restablecer cosecha del dia
        #Aumentar dia
        dia_actual +=1
        # Dia inicio de gurobi al dia actual
        dia_inicio=dia_actual
        #Restablecer boleano
        fermentando=False
        #revisar si hay tanques fermentando
        for i in Las_Bodegas:
            t=i.tanques_fermentando
            if len(t)>=1:
                fermentando=True
        


    #Se imprime el resumen de todo lo fermentado y sobrasa
    #resumen.imprimir_resumen()
    #Agregar costos de sobras
    for x in Los_Cuarteles:
        C=x.cosechable*x.precio*10*1000
        resumen.costo_sobras+=C
    #Guardar datos de resumen
    resumen.dict_dia=[Cosecha_dia_ex,trab_dia_ex,fermentado_dia_ex]
    resumen.largo=largo_periodo
    #Calcular tiempo
    fin = time.time()
    resumen.time=fin-ini
    #Guardar resumen
    RESUMENES.append(resumen)

    
# Tiempo de ejecucion
print(fin-inicio) # 1.0005340576171875
# ------------------------------------------------------------
#CREAR EXCEL
nomb="solucion_"+str(largo_periodo)+"d_gap"+str(gap)
crear_excel(nomb,RESUMENES)
# ------------------------------------------------------------
#DEVOLVER FEEDBACK



