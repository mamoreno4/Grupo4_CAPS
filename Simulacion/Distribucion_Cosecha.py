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
#Cosechas
df = pd.read_excel("Datos base G4 (2).xlsx", sheet_name='Histórico de cosechas')
x = np.array(df)
distr_cuart=[]
for i in x:
    # Fit distributions
    # dist = distfit()
    # dist.fit_transform(i)
    # Print the results
    # Plot the fitted distributions
    Generar_data_cuarteles=i.mean()+i.std()
    distr_cuart.append(Generar_data_cuarteles)
# print(distr_cuart)
