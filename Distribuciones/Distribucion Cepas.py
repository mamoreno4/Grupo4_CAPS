import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import math
# Ver si poner todo en una lista o excel 
#Leer excel
#Iniciar  distr
#Cepa c
df = pd.read_excel('Datos.xlsx', sheet_name='C')

x = np.array(df)
dist = distfit(method='discrete')

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="C")
#Leer excel
#Iniciar  distr
#Cepa CF

df = pd.read_excel('Datos.xlsx', sheet_name='CF')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="CF")
#Leer excel
#Iniciar  distr
#Cepa CS
df = pd.read_excel('Datos.xlsx', sheet_name='CS')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="CS")

#Leer excel
#Iniciar  distr
#Cepa G
df = pd.read_excel('Datos.xlsx', sheet_name='G')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="G")

#Leer excel
#Iniciar  distr
#Cepa M
df = pd.read_excel('Datos.xlsx', sheet_name='M')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="M")
#Leer excel
#Iniciar  distr
#Cepa S
df = pd.read_excel('Datos.xlsx', sheet_name='S')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="S")

#Leer excel
#Iniciar  distr
#Cepa V
df = pd.read_excel('Datos.xlsx', sheet_name='V')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="V")

#Leer excel
#Iniciar  distr
#Cepa SB
df = pd.read_excel('Datos.xlsx', sheet_name='SB')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="SB")
