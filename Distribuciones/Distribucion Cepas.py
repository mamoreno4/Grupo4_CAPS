import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import openpyxl

# Ver si poner todo en una lista o excel
Distribucion_cepa=[]
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


workbook = openpyxl.Workbook()

worksheet = workbook.active

for row in Distribucion_cepa:
    worksheet.append(row)

workbook.save('dist.xlsx')