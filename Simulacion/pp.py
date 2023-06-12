# %%
import pandas as pd
import gurobipy
import os
from gurobipy import GRB, Model, quicksum
import itertools


# %%


# %%
datos1 = pd.read_excel('Datos base G4.xlsx', sheet_name='Datos base G4')
nancagua = pd.read_excel('Datos base G4.xlsx', sheet_name='Bodega Nancagua')
machali = pd.read_excel('Datos base G4.xlsx', sheet_name='Bodega Machali')
chepica = pd.read_excel('Datos base G4.xlsx', sheet_name='Bodega Chepica')
transporte = pd.read_excel('Datos base G4.xlsx', sheet_name='Transporte')

# %%
costo_transporte = {}
for Cuartel, Machali, Chepica, Nancagua in zip(transporte['Cuartel'], transporte['Machali'], transporte['Chepica'], transporte['Nancagua']):
    costo_transporte[f'cuartel_{Cuartel}'] = {'Machali': Machali, 'Chepica': Chepica, 'Nancagua': Nancagua}

# %%
# Conjunto de cuarteles.
cuarteles = []
for i in range (1, 61):
    cuarteles.append(f'cuartel_{i}')

# Diccionario con el factor de conversion de toneladas a litros de cada cuartel.
conversion = {}

# Factor de penalización según día de cosecha.
penalizacion = {}

# %%
# Subconjuntos cepa-calidad. Cada subconjunto contiene los cuarteles que producen una cepa y calidad específica
G_variedad = []
G_reserva = []
G_premium = []
Ch_variedad = []
Ch_reserva = []
Ch_premium = []
SB_variedad = []
SB_reserva = []
SB_premium = []
C_variedad = []
C_reserva = []
C_premium = []
CS_variedad = []
CS_reserva = []
CS_premium = []
S_variedad = []
S_reserva = []
S_premium = []
M_variedad = []
M_reserva = []
M_premium = []
CF_variedad = []
CF_reserva = []
CF_premium = []
V_variedad = []
V_reserva = []
V_premium = []

# %%
# Parámetro binario que es 1 si se puede cosechar el cuartel i en el día t y 0 en caso contrario.
posible_cosechar = {}

# Total a cosechar en cada cuartel, con enfoque robusto da la misma cantidad para todos los cuarteles> 72,2 toneladas.
total_cosechar = {}

# Calidad de uva en el cuartel j.
productividad_cuartel = {}

# Precio de venta por cuartel
precio_venta = {}
cosecha_cuarteles=pd.read_excel('./../Distribuciones/estimado cosecha.xlsx')
cosecha_cuarteles=cosecha_cuarteles.values.tolist()
# %%
for ID in range(1, 61):
    total_cosechar[f'cuartel_{int(ID)}'] = cosecha_cuarteles[ID-1][0]
for ID, Precio, Factor, Variedad, Dia_inicial, Dia_final in zip(datos1['ID'], datos1['Precio'], datos1['Factor'], datos1['Variedad'], datos1['Dia_inicial'], datos1['Dia_final']):
    precio_venta[f'cuartel_{ID}'] = Precio
    if Precio == 1000:
        productividad_cuartel[f'cuartel_{int(ID)}'] = 0.5
    elif Precio == 3000:
        productividad_cuartel[f'cuartel_{int(ID)}'] = 0.42
    elif Precio == 6000:
        productividad_cuartel[f'cuartel_{int(ID)}'] = 0.3

    conversion[f'cuartel_{int(ID)}'] = Factor
    
    penal = {}
    cosechar = {}
    for i in range(0, Dia_inicial + 1):
        if i+1 < Dia_inicial:
            penal[f'dia_{i+1}'] = 0
            cosechar[f'dia_{i+1}'] = 0

        elif i+1 == Dia_inicial:
            cosechar[f'dia_{i+1}'] = 1
            cosechar[f'dia_{i+2}'] = 1
            cosechar[f'dia_{i+3}'] = 1
            cosechar[f'dia_{i+4}'] = 1
            cosechar[f'dia_{i+5}'] = 1
            cosechar[f'dia_{i+6}'] = 1
            cosechar[f'dia_{i+7}'] = 1
            cosechar[f'dia_{i+8}'] = 1

            if Precio == 1000:
                penal[f'dia_{i+1}'] = 0.8
                penal[f'dia_{i+2}'] = 0.8875
                penal[f'dia_{i+3}'] = 0.95
                penal[f'dia_{i+4}'] = 0.9875
                penal[f'dia_{i+5}'] = 1
                penal[f'dia_{i+6}'] = 0.9833
                penal[f'dia_{i+7}'] = 0.9333
                penal[f'dia_{i+8}'] = 0.85
            elif Precio == 3000:
                penal[f'dia_{i+1}'] = 0.6
                penal[f'dia_{i+2}'] = 0.775
                penal[f'dia_{i+3}'] = 0.9
                penal[f'dia_{i+4}'] = 0.975
                penal[f'dia_{i+5}'] = 1
                penal[f'dia_{i+6}'] = 0.9667
                penal[f'dia_{i+7}'] = 0.8667
                penal[f'dia_{i+8}'] = 0.7
            else:
                penal[f'dia_{i+1}'] = 0.1
                penal[f'dia_{i+2}'] = 0.4938
                penal[f'dia_{i+3}'] = 0.775
                penal[f'dia_{i+4}'] = 0.9438
                penal[f'dia_{i+5}'] = 1
                penal[f'dia_{i+6}'] = 0.9111
                penal[f'dia_{i+7}'] = 0.6444
                penal[f'dia_{i+8}'] = 0.2
            
            for j in range(0, datos1['Dia_final'].max() - len(cosechar)):
                penal[f'dia_{i + j + 9}'] = 0
                cosechar[f'dia_{i + j + 9}'] = 0

        penalizacion[f'cuartel_{int(ID)}'] = penal
        posible_cosechar[f'cuartel_{int(ID)}'] = cosechar

    if Variedad == 'G':
        if Precio == 1000:
            G_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            G_reserva.append(f'cuartel_{int(ID)}')
        else:
            G_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'Ch':
        if Precio == 1000:
            Ch_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            Ch_reserva.append(f'cuartel_{int(ID)}')
        else:
            Ch_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'SB':
        if Precio == 1000:
            SB_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            SB_reserva.append(f'cuartel_{int(ID)}')
        else:
            SB_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'C':
        if Precio == 1000:
            C_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            C_reserva.append(f'cuartel_{int(ID)}')
        else:
            C_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'CS':
        if Precio == 1000:
            CS_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            CS_reserva.append(f'cuartel_{int(ID)}')
        else:
            CS_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'S':
        if Precio == 1000:
            S_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            S_reserva.append(f'cuartel_{int(ID)}')
        else:
            S_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'M':
        if Precio == 1000:
            M_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            M_reserva.append(f'cuartel_{int(ID)}')
        else:
            M_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'CF':
        if Precio == 1000:
            CF_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            CF_reserva.append(f'cuartel_{int(ID)}')
        else:
            CF_premium.append(f'cuartel_{int(ID)}')
    elif Variedad == 'V':
        if Precio == 1000:
            V_variedad.append(f'cuartel_{int(ID)}')
        elif Precio == 3000:
            V_reserva.append(f'cuartel_{int(ID)}')
        else:
            V_premium.append(f'cuartel_{int(ID)}')

# %%
# Grupos de cuarteles.
grupos = ['grupo_1', 'grupo_2', 'grupo_3', 'grupo_4', 'grupo_5']
trabajadores_grupo = {'grupo_1': 100, 'grupo_2': 50, 'grupo_3': 100, 'grupo_4': 50, 'grupo_5': 100}
jornada = 8
grupo_cuarteles = {}
grupo1 = []
grupo2 = []
grupo3 = []
grupo4 = []
grupo5 = []
for i in range (0,60):
    if i+1 <= 16:
        grupo1.append(f'cuartel_{i+1}')
    elif i+1 <= 22:
        grupo2.append(f'cuartel_{i+1}')
    elif i+1 <= 32:
        grupo3.append(f'cuartel_{i+1}')
    elif i+1 <= 37:
        grupo4.append(f'cuartel_{i+1}')
    elif i+1 <= 60:
        grupo5.append(f'cuartel_{i+1}')

grupo_cuarteles['grupo_1'] = grupo1
grupo_cuarteles['grupo_2'] = grupo2
grupo_cuarteles['grupo_3'] = grupo3
grupo_cuarteles['grupo_4'] = grupo4
grupo_cuarteles['grupo_5'] = grupo5

# %%
cepa_calidad = {'G':{1000:G_variedad, 3000:G_reserva, 6000:G_premium},
                'Ch': {1000:Ch_variedad, 3000:Ch_reserva, 6000:Ch_premium},
                'SB': {1000:SB_variedad, 3000:SB_reserva, 6000:SB_premium},
                'C': {1000:C_variedad, 3000:C_reserva, 6000:C_premium},
                'CS': {1000:CS_variedad, 3000:CS_reserva, 6000:CS_premium},
                'S': {1000:S_variedad, 3000:S_reserva, 6000:S_premium},
                'M': {1000:M_variedad, 3000:M_reserva, 6000:M_premium},
                'CF': {1000:CF_variedad, 3000:CF_reserva, 6000:CF_premium},
                'V': {1000:V_variedad, 3000:V_reserva, 6000:V_premium}}

# %%
# Lista de todas las cepas que se producen en la viña
cepas = ["G", "Ch", "SB", "C", "CS", "S", "M", "CF", "V"]

# Lista de todas las bodegas donde se envían las uvas cosechadas
bodegas = ["Machali", "Chepica", "Nancagua"]

# Lista de todos los días del periodo de cosecha, hasta el mayor día final de cosecha.
periodo = []
for i in range(0, datos1['Dia_final'].max()):
    periodo.append(f'dia_{i+1}')

# Lista de todas las calidades de uva que se pueden cosechar
calidades = [1000, 3000, 6000]

# Costo por hora trabajada de cada trabajador.
costo_trabajador = 12000

# Big M
M = 1000000

# Multiplicador costo perdida
multiplicador_perdida = 10

# Llenado maximo y minimo de cada estanque
llenado_maximo = 0.95
llenado_minimo = 0.75

# Cantidad de estanques en cada bodega
nro_estanques = {'Machali': 14, 'Chepica': 9, 'Nancagua': 13}

# %%
##  Diccionario con los promedios de tiempos de fermentación de cada cepa.
#
promedio_fermentacion = {'C': 15, 'CF': 16, 'CS': 14, 'G': 18, 'M': 17, 'S': 14, 'V': 17, 'SB': 16, 'Ch': 16}
#
## Lista que agrupa los días en intervalos de X cantidad de días.
#
#agrupacion = {}
#
#for c in cepas:
#    dias_agrupados = {}
#    for i in range(0, datos1['Dia_final'].max() - promedio_fermentacion[c] + 1):
#        d_a = []
#        for j in range(0, promedio_fermentacion[c]):
#            d_a.append(f'dia_{i+j+1}')
#        dias_agrupados[f'agrupacion_{i+1}'] = d_a
#    agrupacion[c] = dias_agrupados


# %%
#agrupaciones_cepa = {}
#for c in cepas:
#    agrupaciones = []
#    for i in range(0, len(agrupacion[c])):
#        agrupaciones.append(f'agrupacion_{i+1}')
#    agrupaciones_cepa[c] = agrupaciones

# %%
lista_estanques = []
lista_estanques_machali = []
lista_estanques_nancagua = []
lista_estanques_chepica = []
dic_estanques = {}
estanques = {}
estanques_nancagua = {}
estanques_machali = {}
estanques_chepica = {}
for ID, capacidad in zip(machali['Id'], machali['capacidad tanques (miles de litros)']):
    estanques_machali[f'estanque_machali_{ID}'] = capacidad
    lista_estanques.append(f'estanque_machali_{ID}')
    lista_estanques_machali.append(f'estanque_machali_{ID}')
dic_estanques['Machali'] = lista_estanques_machali
estanques['Machali'] = estanques_machali

for ID, capacidad in zip(nancagua['Id'], nancagua['capacidad tanques (miles de litros)']):
    estanques_nancagua[f'estanque_nancagua_{ID}'] = capacidad
    lista_estanques.append(f'estanque_nancagua_{ID}')
    lista_estanques_nancagua.append(f'estanque_nancagua_{ID}')
dic_estanques['Nancagua'] = lista_estanques_nancagua
estanques['Nancagua'] = estanques_nancagua

for ID, capacidad in zip(chepica['Id'], chepica['capacidad tanques (miles de litros)']):
    estanques_chepica[f'estanque_chepica_{ID}'] = capacidad
    lista_estanques.append(f'estanque_chepica_{ID}')
    lista_estanques_chepica.append(f'estanque_chepica_{ID}')
dic_estanques['Chepica'] = lista_estanques_chepica
estanques['Chepica'] = estanques_chepica

# %%
capacidad_maxima = {'Nancagua': nancagua['capacidad tanques (miles de litros)'].sum()*llenado_maximo, 'Chepica': chepica['capacidad tanques (miles de litros)'].sum()*llenado_maximo, 'Machali': machali['capacidad tanques (miles de litros)'].sum()*llenado_maximo}
capacidad_minima = {'Nancagua': min(nancagua['capacidad tanques (miles de litros)'])*llenado_minimo, 'Chepica': min(chepica['capacidad tanques (miles de litros)'])*llenado_minimo, 'Machali': min(machali['capacidad tanques (miles de litros)'])*llenado_minimo}

# %%
estanques_ocupados = {}

# %%
def optimizacion_cosecha(dia_inicio, largo_periodo, estanques_ocupados_actual, total_cosechar_actual, gap):
    dia_inicio: int
    largo_periodo: int
    estanques_ocupados_actual: dict
    total_cosechar_actual: dict
    gap: float
    if largo_periodo+dia_inicio > datos1['Dia_final'].max():
        largo_periodo=datos1['Dia_final'].max()-dia_inicio
        
    periodo_cosecha = []
    for i in range(dia_inicio, dia_inicio + largo_periodo):
        periodo_cosecha.append(f'dia_{i}')

    model = Model("Cosecha Vino")
    model.setParam('MIPGap', gap)

    # Lista que agrupa los días en intervalos de X cantidad de días.
    agrupacion = {}
    for c in cepas:
        dias_agrupados = {}
        for i in range(dia_inicio, dia_inicio + largo_periodo - promedio_fermentacion[c] + 1):
            d_a = []
            for j in range(0, promedio_fermentacion[c]):
                d_a.append(f'dia_{i+j}')
            dias_agrupados[f'agrupacion_{i-dia_inicio+1}'] = d_a
        agrupacion[c] = dias_agrupados
    agrupaciones_cepa = {}
    for c in cepas:
        agrupaciones = []
        for i in range(0, len(agrupacion[c])):
            agrupaciones.append(f'agrupacion_{i+1}')
        agrupaciones_cepa[c] = agrupaciones

    # VARIABLES

    # Variable que indica si la bodega b recibe uvas de la cepa c y calidad k en el día t.
    R_btck = model.addVars(bodegas, periodo_cosecha, cepas, calidades, vtype=GRB.BINARY, name="R_btck")
    # Variable que indica la cantidad de uvas cosechadas en el periodo t, que son llevadas desde el cuartel j a la bodega b.
    X_bjt = model.addVars(bodegas, cuarteles, periodo_cosecha, vtype=GRB.CONTINUOUS, name="X_bjt")
    # Variable de utilizacion de tanques en bodegas
    Y_btcke = model.addVars(bodegas, periodo_cosecha, cepas, calidades, lista_estanques, vtype=GRB.BINARY, name="Y_btcke")
    # Variable que indica la horas/hombre asignadas al cuartel j en el periodo t.
    N_jt = model.addVars(cuarteles, periodo_cosecha, vtype=GRB.CONTINUOUS, name="N_jt")

    # RESTRICCIONES
    #Restriccion 1: Un estanque no puede usarse dos veces en al menos X cantidad de dias
    model.addConstrs(quicksum(Y_btcke[b,t,c,k,e] for c in cepas for k in calidades for b in bodegas) <= 1 for bo in bodegas for t in periodo_cosecha for e in dic_estanques[bo]);
    model.addConstrs(quicksum(Y_btcke[b,t,c,k,e] for c in cepas for t in agrupacion[co][a] for k in calidades) <= 1 for b in bodegas for co in cepas for e in dic_estanques[b] for a in agrupaciones_cepa[co]);
    # Restriccion 2: Lo que se envia a las bodegas debe poder almacenarse en su totalidad en alguna combinación de estanques.
    model.addConstrs(quicksum(X_bjt[b,j,t]*conversion[j] for j in cepa_calidad[c][k]) >= quicksum(Y_btcke[b,t,c,k,e]*estanques[b][e] for e in dic_estanques[b])*llenado_minimo for b in bodegas for t in periodo_cosecha for c in cepas for k in calidades);
    model.addConstrs(quicksum(X_bjt[b,j,t]*conversion[j] for j in cepa_calidad[c][k]) <= quicksum(Y_btcke[b,t,c,k,e]*estanques[b][e] for e in dic_estanques[b])*llenado_maximo for b in bodegas for t in periodo_cosecha for c in cepas for k in calidades);
    # Restriccion 3: La cantidad cosechada debe ser mayor que el mínimo de cada bodega
    model.addConstrs(quicksum(X_bjt[b,j,t]*conversion[j] for j in cepa_calidad[c][k]) >= capacidad_minima[b]*R_btck[b,t,c,k] for b in bodegas for t in periodo_cosecha for c in cepas for k in calidades);
    # Restriccion 4: auxiliar para ajustar el valor de la variable binaria R_btck
    model.addConstrs(R_btck[b,t,c,k]*M >= quicksum(X_bjt[b,j,t] for j in cepa_calidad[c][k]) for b in bodegas for t in periodo_cosecha for c in cepas for k in calidades);
    # Restriccion 5: Solo se cosecha el cuartel si es apto segun la ventana de cosecha.
    model.addConstrs(quicksum(X_bjt[b,j,t] for b in bodegas) <= M*posible_cosechar[j][t] for j in cuarteles for t in periodo_cosecha);
    # Restriccion 6: La cantidad de horas-hombre asignadas por grupo de cuarteles no puede superar la cantidad maxima disponible.
    model.addConstrs(quicksum(N_jt[j,t] for j in grupo_cuarteles[g]) <= trabajadores_grupo[g]*jornada for g in grupos for t in periodo_cosecha);
    # Restriccion 7: La cosecha debe ser igual a la productividad de los trabajadores 
    model.addConstrs(quicksum(X_bjt[b,j,t] for b in bodegas) == N_jt[j,t]*productividad_cuartel[j] for j in cuarteles for t in periodo_cosecha);
    #Restriccion 8: no se pueden ocupar estanques que se encuentran ocupados inicialmente
    for estanque in estanques_ocupados_actual:
        model.addConstrs(quicksum(Y_btcke[b,t,c,k,estanque] for b in bodegas for c in cepas for k in calidades) <= 1 - estanques_ocupados_actual[estanque][t] for t in estanques_ocupados_actual[estanque].keys())
    #Restriccion 9: No se puede cosechar mas que el total disponible en cada cuartel.
    model.addConstrs(quicksum(X_bjt[b,j,t] for b in bodegas for t in periodo_cosecha) <= total_cosechar_actual[j] for j in cuarteles);

    # FUNCION OBJETIVO

    obj = quicksum(X_bjt[b,j,t]*conversion[j]*1000*precio_venta[j]*penalizacion[j][t] for b in bodegas for j in cuarteles for t in periodo_cosecha) - quicksum((total_cosechar_actual[j] - quicksum(X_bjt[b,j,t] for b in bodegas for t in periodo_cosecha))*precio_venta[j]*conversion[j]*1000*multiplicador_perdida for j in cuarteles) - quicksum(N_jt[j,t]*costo_trabajador for j in cuarteles for t in periodo_cosecha) - quicksum(X_bjt[b,j,t]*costo_transporte[j][b]*1000 for b in bodegas for t in periodo_cosecha for j in cuarteles)
    model.setObjective(obj, GRB.MAXIMIZE)
    model.optimize()

    # RETORNAR RESULTADOS

    var_names_X = []
    var_bodega_X = []
    var_cuartel_X = []
    var_dia_X = []
    var_values_X = [] 
    var_names_N = []
    var_cuartel_N = []
    var_dia_N = []
    var_values_N = []
    var_names_Y = []
    var_bodega_Y = []
    var_dia_Y = []
    var_cepa_Y = []
    var_calidad_Y = []
    var_estanque_Y = []
    var_values_Y = []

    for var in model.getVars():
        if var.X > 0 and var.varName[0] == 'X':
            splitted_var_X = var.VarName.split(',')
            splitted_var2_X = splitted_var_X[0].split('[')
            var_names_X.append(splitted_var2_X[0])
            var_bodega_X.append(splitted_var2_X[1])
            var_cuartel_X.append(splitted_var_X[1])
            var_dia_X.append(splitted_var_X[2].strip(']'))
            var_values_X.append(var.x)
        elif var.X > 0 and var.varName[0] == 'N':
            splitted_var_N = var.VarName.split(',')
            splitted_var2_N = splitted_var_N[0].split('[')
            var_names_N.append(splitted_var2_N[0])
            var_cuartel_N.append(splitted_var2_N[1])
            var_dia_N.append(splitted_var_N[1].strip(']'))
            var_values_N.append(var.x*costo_trabajador)
        elif var.X > 0 and var.varName[0] == 'Y':
            splitted_var_Y = var.VarName.split(',')
            splitted_var2_Y = splitted_var_Y[0].split('[')
            var_names_Y.append(splitted_var2_Y[0])
            var_bodega_Y.append(splitted_var2_Y[1])
            var_dia_Y.append(splitted_var_Y[1])
            var_cepa_Y.append(splitted_var_Y[2])
            var_calidad_Y.append(splitted_var_Y[3])
            var_estanque_Y.append(splitted_var_Y[4].strip(']'))
            var_values_Y.append(var.x)
    var_values2_X = []
    for cuartel, valor in zip(var_cuartel_X, var_values_X):
        var_values2_X.append((valor)*conversion[cuartel])
    
    df_cosecha = pd.DataFrame({'Variable': var_names_X, 'Cuartel': var_cuartel_X, 'Dia': var_dia_X, 'Bodega': var_bodega_X, 'Valor': var_values2_X})
    df_trabajadores = pd.DataFrame({'Variable': var_names_N, 'Cuartel': var_cuartel_N, 'Dia': var_dia_N, 'Valor': var_values_N})
    df_estanques = pd.DataFrame({'Variable': var_names_Y, 'Bodega': var_bodega_Y, 'Dia': var_dia_Y, 'Cepa': var_cepa_Y, 'Calidad': var_calidad_Y, 'Estanque': var_estanque_Y, 'Valor': var_values_Y})

    return df_cosecha, df_trabajadores, df_estanques
