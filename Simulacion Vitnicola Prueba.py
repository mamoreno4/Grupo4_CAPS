from datetime import date, datetime, timedelta
from random import uniform, random, seed, randint, gauss
import numpy as np
import pandas as pd
import time as tm

class Cuartel:
    def __init__(self, listav,cosecha_aproximada):
        self.id=listav[0]
        self.dia_opt=listav[1]
        self.dia_ini=listav[2]
        self.dia_final=listav[3]
        self.variedad=listav[4]
        self.precio=listav[5]
        self.prod=listav[7]
        self.cantidad=cosecha_aproximada

    def actualizar_cosecha(self,cosechado):
        pass
    def posible_cosechar(self,dia_actual):
        pass
    def __str__(self):
        return "-> {}".format(self.id)
class Grupo_trabajador:
    def __init__(self,lista_valores):
        pass
class Bodega:
    def __init__(self,ubicacion):
        self.ubicacion=lista_valores[0]
        self.tanques=[]
        self.tanques_fermentando=[]
        self.tanques_disponibles=[]
        pass
    def agregar_tanque(self,tanque):
        self.tanques.append(tanque)
        pass
    def revisar_tanques(self):
        self.tanques_disponibles=[]
        self.tanques_fermentando=[]
        for i in self.tanques:
            if i.estado=="Disponible":
                self.tanques_disponibles.append(i)
            elif i.estado=="Fermentando":
                self.tanques_fermentando.append(i)
            else:
                pass


class Tanques:
    def __init__(self,capacidad):
        self.capacidad=capacidad
        self.estado="Disponible"
        self.dia_termino=0
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        pass
    def fermentar(self,cantidad,dia):
        self.estado="Fermentando"
        self.cantidad_fermentado=cantidad
        dia_aprox=7
        self.dia_termino=dia+timedelta(days=dia_aprox)
    def vaciar_tanque(self):
        fermentado=[self.cantidad_fermentado,self.variedad_fermentando]
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        return fermentado
        
    def generar_dia(self,variedad):
        pass
class Vitnicola:
    def __init__(self, tiempo_simulacion):
        pass
    @property
    def proximo_evento(self):
        evento=1
        return evento
    def dia_inicia(self):
        pass
    def dia_termina(self):
        pass
    def agregar_cuarteles(self,listas_valores):
        pass
    def agregar_trabajadores(self,listas_valores):
        pass
    def agregar_bodegas(self,listas_valores):
        pass
    def run(self):
        while self.tiempo_actual < self.tiempo_maximo:
            evento = self.proximo_evento
            if evento == "fin":
                self.tiempo_actual = self.tiempo_maximo
                break
            elif evento == "Dia_inicia":
                self.dia_inicia()
            elif evento == "Dia_termina":
                self.dia_termina()
    def show(self):
        pass
    
def revisar_dia(dia_actual):
    dia=dia_actual
    cosechable=[]
    optimo=[]
    for i in range(0,60):
        r=dia==df_id["día óptimo"][i]
        if r is True:
            optimo.append(df_id.iloc[i][0])
        else:
            r=dia>=df_id["día inicial"][i]
            if r is True:
                r=dia<=df_id["día final"][i]
                if r is True:
                    cosechable.append(df_id.iloc[i][0])
                else:
                    pass
    return [cosechable,optimo]


#numpy ver como

seed(20)
fechas=[]
inicial = datetime(2019, 1, 1)
dia_actual= datetime(2019, 1, 1)
df = pd.read_excel('Datos Base Ordenados (Cosecha).xlsx')
df_id=df.iloc[0:60,[1,2,3,4,5,6,7,8,9,10,11]]
for i in range(0,60):
    for x in range(1,4):
        df_id.iloc[i,[x]]=inicial+timedelta(days=df_id.iloc[i,x])

