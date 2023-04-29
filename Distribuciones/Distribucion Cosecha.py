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
df = pd.read_excel('Datos.xlsx', sheet_name='Hoja1')

x = np.array(df)
# Fit distributions
dist = distfit(method='discrete')
dist.fit_transform(x)

# Print the results
print(dist.summary)
# Plot the fitted distributions
dist.plot()
print(dist.plot_summary())  