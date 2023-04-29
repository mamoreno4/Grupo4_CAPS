import scipy as sc
from distfit import distfit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import math

df = pd.read_excel('Datos.xlsx', sheet_name='C')

x = np.array(df)
dist = distfit(method='discrete')

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="C")


df = pd.read_excel('Datos.xlsx', sheet_name='CF')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="CF")

df = pd.read_excel('Datos.xlsx', sheet_name='CS')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="CS")


df = pd.read_excel('Datos.xlsx', sheet_name='G')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="G")


df = pd.read_excel('Datos.xlsx', sheet_name='M')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="M")

df = pd.read_excel('Datos.xlsx', sheet_name='S')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="S")


df = pd.read_excel('Datos.xlsx', sheet_name='V')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="V")


df = pd.read_excel('Datos.xlsx', sheet_name='SB')

x = np.array(df)

# Fit distributions
dist.fit_transform(x)

# Print the results
print(dist.summary)

# Plot the fitted distributions
dist.plot(title="SB")
