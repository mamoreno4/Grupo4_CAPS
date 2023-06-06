from random import uniform, seed, randint, gauss
from numpy.random import Generator, PCG64
import numpy as np
import pandas as pd
from scipy.stats import binom
import openpyxl
import itertools
#archivo con las clases y funciones del main
class Cuartel:

    def __init__(self, listav):
        self.cosechable=0
        self.id=listav[1]
        self.variedad=listav[5]
        self.precio=listav[6]
        self.cosecha_por_dia=dict()
        for i in range(1,366):
            self.cosecha_por_dia[i]=[]
        self.dia_optimo=listav[2]
        self.costo_hora=listav[8]
        self.transporte={"Machali":listav[9],"Chepica":listav[10],"Nancagua":listav[11]}
        self.despreciacion={1000:[0.8,0.8875,0.95,0.9875,1,0.9833,0.9333,0.85],3000:[0.6,0.775,0.9,0.975,1,0.9667,0.8667,0.7],6000:[0.1,0.4938,0.775,0.9438,1,0.9111,0.6444,0.2]}
    def agregar_cosecha(self,dia,cantidad_bodega):
        self.cosecha_por_dia[dia].append(cantidad_bodega)
        pass
    def set_cosechable(self,cosechable):
        self.cosechable=cosechable
        pass
    def gen_desp(self,dia,precio):
        desp=1
        for i in self.cosecha_por_dia[dia]:
            desp=self.despreciacion[precio][dia+4-int(self.dia_optimo)]
        return desp
    def __str__(self):
        return "-> {}".format(self.id)
    
    def __repr__(self):
        return "Cuartel {}".format(self.id)
    

class Bodega:
    def __init__(self,ubicacion_tanques,nombre):
        self.id_tanque=0
        self.ubicacion=nombre
        self.tanques=[]
        self.tanques_fermentando=[]
        self.tanques_disponibles=[]
        for i in range(1,len(ubicacion_tanques.index)):
            Tanq=ubicacion_tanques.iloc[i]
            T=Tanque(Tanq[1],self.ubicacion,Tanq[0])
            self.agregar_tanque_disponible(T)
        pass

    def agregar_tanque_disponible(self,tanque):
        self.tanques.append(tanque)
        self.tanques_disponibles.append(tanque)
        pass

    def agregar_tanque_fermentando(self,tanque):
        self.tanques_disponibles.remove(tanque)
        self.tanques_fermentando.append(tanque)
        #print("Se agrega tanque {} a fermentar".format(tanque.id))
        pass
    
    def revisar_tanques(self,dia):
        salidas=[]
        self.tanques_disponibles=[]
        self.tanques_fermentando=[]
        for i in self.tanques:
            if i.estado=="Disponible":
                self.tanques_disponibles.append(i)
            elif i.estado=="Fermentando":
                if i.dia_termino==dia:
                    salidas.append(i.vaciar_tanque())
                    self.tanques_disponibles.append(i)
                else:
                    self.tanques_fermentando.append(i)
        return salidas
    
    def tanques_capacidad(self,cap):
        disp=[]
        for i in self.tanques_disponibles:
            if i.capacidad==cap:
                disp.append(i)
        return disp
    
    def __repr__(self):
        return "Bodega {}".format(self.ubicacion)
    

class Tanque:

    def __init__(self,capacidad,ubicacion,id):
        self.id = id
        self.capacidad=capacidad
        self.estado="Disponible"
        self.dia_inicial=0
        self.dia_termino=0
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        self.precio=0
        self.ubicacion=ubicacion
        self.generado=0
        pass

    def fermentar(self,cantidad,dia,variedad,precio,distr):
        if self.estado=="Disponible":
            self.estado="Fermentando"
            self.dia_inicial=dia
            self.cantidad_fermentado=cantidad
            self.variedad_fermentando=variedad
            self.precio=precio
            self.dia_termino=dia+self.generar_dia(variedad,distr)
            #print("Se comienza a fermentar {} de variedad {} hasta el día {} en la bodega {}".format(cantidad,variedad,self.dia_termino,self.ubicacion))
            pass
        else:
            print("Error: tanque no Disponible")
            pass
        
    def vaciar_tanque(self):
        dias_fermentando=self.dia_termino-self.dia_inicial
        fermentado=[self.cantidad_fermentado, self.variedad_fermentando, dias_fermentando, self.precio]
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        self.dia_inicial=0
        self.dia_termino=0
        self.estado="Disponible"
        self.generado=0
        return fermentado
    
    def generar_dia(self,variedad,distr):
        n=distr.loc[variedad][1]
        p=distr.loc[variedad][2]
        dia_generado=binom.rvs(n, p)
        self.generado=dia_generado
        return dia_generado
    
    def __repr__(self):
        return "Tanque {}".format(self.id)+" de la bodega {}".format(self.ubicacion)
    

#Revisar que mas poner en resumen
class Resumen:

    def __init__(self):
        self.dias=dict()
        self.sobras_cepas_bodega={'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.dias_generados=[]
        self.cosechado=0
        self.fermentado=0
        self.sobras=0
        self.seed=0
        self.sobras_cantidad_dia=[]
        self.porcentaje_tanque=[]
        self.total_cosechable=3753.4200000000023
        self.dias_ocupado_tanques=[]
        self.fermentado_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.fermentado_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.fermentado_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.costo_transporte=0
        self.costo_trabajo=0
        self.sobras_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.sobras_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.sobras_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.costo_dias=0
        self.costo_sobras=0
        self.ganancias=0
        for i in range(200):
            self.dias[i]=[]
        pass

    def agregar_dia(self,dia):
        self.dias[dia]=[]
        pass

    def agregar_cosecha(self,dia,cosecha):
        self.dias[dia].append("Se cosecho "+cosecha)
        pass

    def agregar_fermentado(self,dia,fermentado):
        self.dias[dia].append("Se fermento "+str(fermentado[0])+" de variedad "+str(fermentado[1])+" de precio "+str(fermentado[3])+" en "+ str(fermentado[2]) +" dias")
        pass

    def agregar_sobrante(self,dia,sobrante,precio):
        self.dias[dia].append("El dia"+ str(dia) +" sobro la cantidad de "+str(sobrante)+" de variedad "+str(precio))
        pass

    def agregar_tanque(self, dia, cantidad):
        self.dias[dia].append("El dia"+ dia +" se agrego a tanque la cantidad de "+ cantidad)
        pass
    def gen_promedio(self):
        Ganancias_COSTO = self.ganancias-self.costo_dias-self.costo_sobras-self.costo_transporte-self.costo_trabajo

        Promedios = [["Dias generados",],["Dias Ocupado tanques",],["Promedio de porcentaje llenado tanque",],["Promedio de sobrante por dia",],["Cosechado",self.cosechado],["Fermentado",self.fermentado],["Nombre(seed)",self.seed],["Sobrante",self.sobras],["Costo dias",self.costo_dias],["Costo sobras",self.costo_sobras],["Ganancias",self.ganancias],["Costo transporte",self.costo_transporte],["Costo trabajo",self.costo_trabajo],["Ganancia Bruta",Ganancias_COSTO]]
        datos=[self.dias_generados,self.dias_ocupado_tanques,self.porcentaje_tanque,self.sobras_cantidad_dia]
        p=0
        for x in datos:
            Promedio = 0
            for i in x:
                Promedio += i
            if Promedio != 0:
                Promedi = Promedio/len(x)
            Promedios[p].append(Promedi)
            p+=1
        return Promedios

    def imprimir_resumen(self):
        f_total_1000 = 0
        f_total_3000 = 0
        f_total_6000 = 0
        s_total_1000 = 0
        s_total_3000 = 0
        s_total_6000 = 0
        for i in self.fermentado_1000:
            for j in self.fermentado_1000[i]:
                f_total_1000 += self.fermentado_1000[i][j]
                print("EL total final fermentado en la bodega {} de cepa {} es {}".format(i,j,self.fermentado_1000[i][j]))
        for i in self.fermentado_3000:
            for j in self.fermentado_3000[i]:
                f_total_3000 += self.fermentado_3000[i][j]
                print("EL total final fermentado en la bodega {} de cepa {} es {}".format(i,j,self.fermentado_3000[i][j]))
        for i in self.fermentado_6000:
            for j in self.fermentado_6000[i]:
                f_total_6000 += self.fermentado_6000[i][j]
                print("EL total final fermentado en la bodega {} de cepa {} es {}".format(i,j,self.fermentado_6000[i][j]))
        
        for i in self.sobras_1000:
            for j in self.sobras_1000[i]:
                s_total_1000 += self.sobras_1000[i][j]
                print("EL total final de sobras en la bodega {} de cepa {} es {}".format(i,j,self.sobras_1000[i][j]))
        for i in self.sobras_3000:
            for j in self.sobras_3000[i]:
                s_total_3000 += self.sobras_3000[i][j]
                print("EL total final de sobras en la bodega {} de cepa {} es {}".format(i,j,self.sobras_3000[i][j]))
        for i in self.sobras_6000:
            for j in self.sobras_6000[i]:
                s_total_6000 += self.sobras_6000[i][j]
                print("EL total final de sobras en la bodega {} de cepa {} es {}".format(i,j,self.sobras_6000[i][j]))
        
        # Final de fermentado y sobras por precio
        print("El total final de fermentado con precio 1000 es {}".format(f_total_1000))
        print("El total final de fermentado con precio 3000 es {}".format(f_total_3000))
        print("El total final de fermentado con precio 6000 es {}".format(f_total_6000))
        print("El total final de sobras con precio 1000 es {}".format(s_total_1000))
        print("El total final de sobras con precio 3000 es {}".format(s_total_3000))
        print("El total final de sobras con precio 6000 es {}".format(s_total_6000))

def crear_excel(nombre_archivo,lista_resumenes):
    nombre=nombre_archivo+".xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resumen"
    ws['A1'] = "Nombre(seed)"
    ws['B1'] = "Cosechado"
    ws['C1'] = "No cosechado"
    ws['D1'] = "Fermentado"
    ws['E1'] = "Sobrante"
    ws['F1'] = "Promedio de sobrante por dia"
    ws['G1'] = "Promedio de porcentaje llenado tanque"
    ws['H1'] = "Dias generados"
    ws['I1'] = "Dias Ocupado tanques"
    ws['J1'] = "Costos dias fermentando"
    ws['K1'] = "Costos perdidas"
    ws['L1'] = "Costos Transporte"
    ws['M1'] = "Costos Trabajadores"
    ws['N1'] = "Ganancias"
    ws['O1'] = "Ganancias Bruta"
    c=2
    for i in lista_resumenes:
        G=i.gen_promedio()
        ws['A'+str(c)] = G[6][1]
        ws['B'+str(c)] = G[4][1]
        ws['C'+str(c)] = 3754.4000000000024 - G[4][1]
        ws['D'+str(c)] = G[5][1]
        ws['E'+str(c)] = G[7][1]
        ws['F'+str(c)] = G[3][1]
        ws['G'+str(c)] = G[2][1]
        ws['H'+str(c)] = G[0][1]
        ws['I'+str(c)] = G[1][1]
        ws['J'+str(c)] = G[8][1]
        ws['K'+str(c)] = G[9][1]
        ws['N'+str(c)] = G[10][1]
        ws['L'+str(c)] = G[11][1]
        ws['M'+str(c)] = G[12][1]
        ws['O'+str(c)] = G[13][1]


        c+=1
    wb.save(nombre)
# funcion para llenar los tanques version 1
def fill_tanks(tanks, liquid):
    # iniciar variables
    best_combination = None
    best_leftover = float('inf')
    min_tanks_used = float('inf')
    # iterar sobre todas las combinaciones de tanques
    for n in range(1, len(tanks) + 1):
        for combination in itertools.combinations(tanks, n):
            # Calculate the total capacity of the tanks
            total_capacity = sum(capacity for _, capacity in combination)
            
            if total_capacity < liquid:
                continue

            remaining = liquid
            leftover = 0
            fill_levels = []
            # Fill the tanks
            for tank, capacity in combination:
                fill_level = min(max(remaining / total_capacity, 0.75), 0.95)
                fill_amount = fill_level * capacity
                fill_levels.append((tank, fill_amount))
                remaining -= fill_amount
                leftover += capacity - fill_amount
            # Check if this is the best combination so far
            if (remaining == 0 or (remaining>0 and remaining<liquid*0.001)) and leftover < best_leftover and n <= min_tanks_used:
                best_combination = fill_levels
                best_leftover = leftover
                min_tanks_used = n

    return best_combination

# funcion para llenar los tanques version 2(desechada)
def find_combination(tanks,liquid):
    # iniciar variables
    n = len(tanks)
    memo = {}
    # funcion recursiva
    def dp(liquid, idx, num_tanks):
        # caso base
        if idx == n:
            return float('inf'), {}

        if (liquid, idx, num_tanks) in memo:
            return memo[(liquid, idx, num_tanks)]

        tank_name, capacity = tanks[idx]
        max_fill = int(capacity * 0.95)
        min_fill = int(capacity * 0.75)

        best_leftovers = float('inf')
        best_combination = {}
        # iterar sobre todas las combinaciones de tanques
        for fill_amount in range(min_fill, max_fill + 1):
            # Calculate the total capacity of the tanks
            if fill_amount <= liquid:
                remaining_liquid = liquid - fill_amount
                new_leftovers, combination = dp(remaining_liquid, idx + 1, num_tanks + 1)
                new_leftovers += capacity - fill_amount
                # Check if this is the best combination so far
                if new_leftovers < best_leftovers:
                    best_leftovers = new_leftovers
                    best_combination = combination.copy()
                    best_combination[tank_name] = fill_amount
        # Check if this is the best combination so far
        if num_tanks < best_leftovers:
            # set memo
            memo[(liquid, idx, num_tanks)] = (num_tanks, best_combination)
            return num_tanks, best_combination
        # set memo
        memo[(liquid, idx, num_tanks)] = (best_leftovers, best_combination)
        return best_leftovers, best_combination

    _, best_combination = dp(liquid, 0, 0)
    return best_combination
# funcion para llenar los tanques version 3
def encontrar_combinacion_liquido(liquido, tanques):
    # Inicializar variables
    mejor_combinacion = None
    diferencia_minima = float('inf')
    num_tanques = len(tanques)
    # Iterar sobre todas las combinaciones de tanques
    for r in range(1, num_tanques + 1):
        # Iterar sobre todas las combinaciones de tanques de tamaño r
        for combo in itertools.combinations(tanques, r):
            # Calcular la suma de las capacidades de los tanques en la combinación
            suma_capacidades = sum(capacidad for _, capacidad in combo)
            # Verificar si la combinación es válida
            if liquido >= suma_capacidades * 0.75 and liquido <= suma_capacidades * 0.95:
                # Calcular la diferencia entre la suma de las capacidades y el líquido
                diferencia = abs(suma_capacidades - liquido)
                # Verificar si la diferencia es menor a la diferencia mínima
                if diferencia < diferencia_minima:
                    diferencia_minima = diferencia
                    mejor_combinacion = combo
    return mejor_combinacion

# funcion para llenar los tanques version 3

def llenar_tanques(liquido_total, tanques):
    # Ordenar los tanques por capacidad (de mayor a menor)
    tanques_ordenados = sorted(tanques, key=lambda x: x[1], reverse=True)
    
    # Inicializar una lista para almacenar la cantidad de líquido en cada tanque
    liquido_tanques = []
    
    # Recorrer los tanques ordenados
    for i, tanque in enumerate(tanques_ordenados):
        nombre_tanque, capacidad_tanque = tanque
        
        # Calcular la cantidad de líquido a poner en el tanque actual
        min_liquido = int(0.75 * capacidad_tanque)  # 75% de la capacidad del tanque
        max_liquido = int(0.95 * capacidad_tanque)  # 95% de la capacidad del tanque
        
        cantidad_liquido = min(liquido_total, max_liquido)
        
        liquido_tanques.append((nombre_tanque, cantidad_liquido))
        liquido_total -= cantidad_liquido
        
        # Si ya no queda líquido por distribuir, se detiene el bucle
        if liquido_total == 0:
            break
    
    return liquido_tanques
# funcion para llenar los tanques version 3

def comb_liquido(tanques, liquido):
    # Inicializar variables
    cantidad_liquido_tanques=None
    combinaciones = encontrar_combinacion_liquido(liquido, tanques)
    # Verificar si se encontró una combinación
    com_best=combinaciones
    # Verificar si se encontró una combinación
    if com_best:
        print(com_best)
        cantidad_liquido_tanques = llenar_tanques(liquido, com_best)
    return cantidad_liquido_tanques

def revisar_input(tanques_ocupados,bodegas):
    tanques_problemas=[]
    for i in bodegas:
        for a in i.tanques_fermentando:
            if a in tanques_ocupados:
                pass
            else:
                tanques_problemas.append([a,"tanque no ocupado"])
    for i in bodegas:
        for a in i.tanques_disponibles:
            if a in tanques_ocupados:
                tanques_problemas.append([a,"tanque ocupado"])
                pass
            else:
                pass
    return tanques_problemas

     

def pasar_tanques_dict(BODEGAS,dia):
    tanques_ocupados={}
    for i in BODEGAS:
        for a in i.tanques_fermentando:
            bod=str(i)[7::]
            id=str(a.id)
            nombre="estanque_"+bod+"_"+id
            nombre=nombre.lower()
            tanques_ocupados[nombre]={}
            for i in range(dia-a.dia_inicial+1):
                tanques_ocupados[nombre]["dia_"+str(i)]=1            
    return tanques_ocupados
def pasar_cuartel_dict(cuarteles):
    cosechar={}
    for i in cuarteles:
        nombre="cuartel_"+str(i.id)[:-2]
        cosechar[nombre]=i.cosechable
    return cosechar