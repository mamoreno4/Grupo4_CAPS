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
# Fit distributions
dist = distfit()
dist.fit_transform(x)

# Print the results
print(dist.summary)
# Plot the fitted distributions
dist.plot()
print(dist.plot_summary())  
a=dist.model["params"][0]
b=dist.model["params"][1]
c=dist.model["params"][2]
d=dist.model["params"][3]
Generar_data_cuarteles=sc.stats.beta.rvs(a,b,loc=c,scale=d,size=60)
