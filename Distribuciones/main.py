import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import clases_simulacion as cs




# main
dia_actual = 1
cantidad_1000 = 0
cantidad_3000 = 0
cantidad_6000 = 0

while ((dia_actual < 15) or (len(cs.Las_Bodegas[0].tanques_fermentando) > 0) or (len(cs.Las_Bodegas[1].tanques_fermentando) > 0) or (len(cs.Las_Bodegas[2].tanques_fermentando) > 0)):
    for bodega in cs.Las_Bodegas:
        salidas = bodega.revisar_tanques(dia_actual)
        if len(salidas) == 0:
            print("No hubo salidas en la bodega " + bodega.ubicacion)
        else:
            for salida in salidas:
                cs.Resumen.agregar_fermentado(dia_actual, salida)
    
    for cuartel in cs.Los_Cuarteles:
        if cuartel.precio == 1000:
            cantidad_1000 = cantidad_1000 + cuartel.cosecha_por_dia(dia_actual)
        elif cuartel.precio == 3000:
            cantidad_3000 = cantidad_1000 + cuartel.cosecha_por_dia(dia_actual)
        elif cuartel.precio == 6000:
            cantidad_6000 = cantidad_1000 + cuartel.cosecha_por_dia(dia_actual)
    
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
        
    cantidad_1000 = 0
    cantidad_3000 = 0
    cantidad_6000 = 0
    dia_actual = dia_actual + 1
