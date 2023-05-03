import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import clases_simulacion as cs


# Ver si poner todo en una lista o excel
Distribucion_cepa=[["Cepa","Distribucion","Parametro 1","Parametro 2"]]
#Leer excel
#Iniciar  distr
Cepa="C"
df = pd.read_excel('Datos.xlsx', sheet_name='C')

x = np.array(df)
dist = distfit(method='discrete')

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="C")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Leer excel
#Iniciar  distr
#Cepa CF
Cepa="CF"
df = pd.read_excel('Datos.xlsx', sheet_name='CF')
x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="CF")
#Leer excel
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Iniciar  distr
#Cepa CS
Cepa="CS"
df = pd.read_excel('Datos.xlsx', sheet_name='CS')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="CS")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Leer excel
#Iniciar  distr
#Cepa G
Cepa="G"
df = pd.read_excel('Datos.xlsx', sheet_name='G')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="G")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Leer excel
#Iniciar  distr
#Cepa M
Cepa="M"
df = pd.read_excel('Datos.xlsx', sheet_name='M')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="M")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Leer excel
#Iniciar  distr
#Cepa S
Cepa="S"
df = pd.read_excel('Datos.xlsx', sheet_name='S')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="S")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Leer excel
#Iniciar  distr
#Cepa V
Cepa="V"
df = pd.read_excel('Datos.xlsx', sheet_name='V')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="V")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])

#Leer excel
#Iniciar  distr
#Cepa SB
Cepa="SB"
df = pd.read_excel('Datos.xlsx', sheet_name='SB')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
#print(dist.summary)

# Plot the fitted distributions
#dist.plot(title="SB")
Distribucion_cepa.append([Cepa,dist.model["name"],dist.model["params"][0],dist.model["params"][1]])
Distribucion_cepa.append(["Ch",dist.model["name"],dist.model["params"][0],dist.model["params"][1]])




# create a NumPy array
data = np.array(Distribucion_cepa)

# create a Pandas DataFrame from the NumPy array
df = data
df = pd.DataFrame(data[1:], columns=data[0])

# save the DataFrame to an Excel file
df.to_excel('dist.xlsx', index=False)


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
                    pass
                elif cantidad_6000 > tanque.capacidad*0.95:
                    pass
                if cantidad_3000 < tanque.capacidad*0.65:
                    print("No hay cantidad suficiente de variedad de precio de 3000 para ocupar el tanque")
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_1000)
                elif tanque.capacidad*0.65 <= cantidad_3000 <= tanque.capacidad*0.95:
                    pass
                elif cantidad_3000 > tanque.capacidad*0.95:
                    pass
                if cantidad_1000 < tanque.capacidad*0.65:
                    print("No hay cantidad suficiente de variedad de precio de 1000 para ocupar el tanque")
                    cs.Resumen.agregar_sobrante(dia_actual, cantidad_1000)
                elif tanque.capacidad*0.65 <= cantidad_1000 <= tanque.capacidad*0.95:
                    pass
                elif cantidad_1000 > tanque.capacidad*0.95:
                    pass

        elif len(bodega.tanques_disponibles) == 0:
            print("No hay tanques disponibles en la bodega " + bodega.ubicacion)
        
    cantidad_1000 = 0
    cantidad_3000 = 0
    cantidad_6000 = 0
    dia_actual = dia_actual + 1