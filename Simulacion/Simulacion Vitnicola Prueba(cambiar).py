from datetime import date, datetime, timedelta
from random import uniform, random, seed, randint, gauss
import numpy as np
import pandas as pd

class Cuartel:
    def __init__(self, listav,cosecha_aproximada):
        self.id=listav[0]
        self.variedad=listav[4]
        self.precio=listav[5]
        self.cantidad_dia=cosecha_aproximada
    def __str__(self):
        return "-> {}".format(self.id)
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
    def tanques_disponibles(self):
        disp=[]
        for i in self.tanques_disponibles:
            disp.append([i,i.capacidad])
        return disp

#tanques?
class Tanque:
    def __init__(self,capacidad):
        self.capacidad=capacidad
        self.estado="Disponible"
        self.dia_inicial=0
        self.dia_termino=0
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        pass
    def fermentar(self,cantidad,dia,variedad):
        self.estado="Fermentando"
        self.dia_inicial=dia
        self.cantidad_fermentado=cantidad
        self.variedad_fermentando=""
        self.dia_termino=self.generar_dia(variedad)
    def vaciar_tanque(self):
        dias_fermentando=self.dia_termino-self.dia_inicial
        fermentado=[self.cantidad_fermentado,self.variedad_fermentando,dias_fermentando]
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        self.dia_inicial=0
        self.dia_termino=0
        return fermentado
    def generar_dia(self,variedad):
        pass









#numpy ver si vale la pena? primera intancia parece que si


#Crear clases (Cuarteles,Bodegas,Tanques,Resumen)
    #Bodegas
        #revisar tanques(listo)
        #tanques disponibles(return que tanque con que capacidad esta disponible)(listo)
    #Tanques
        #generar dia
        #revisar tanques(llamar vaciar tanques)(listo)
    #Resumen
        #crear estructura

#Leer datos
    #Leer excel
        #Poblar cuarteles
        #Poblar bodegas
            #Poblar tanques
    #Leer lista gurobi
        #poblar cosecha por dia
#main
    #while maximo dias o tanque fermentando
        #dia inicia
            #atualizar tanques
            #revisar tanques
            #poner output en resumen
        #revisar que se cosecho a que tanque
            #juntar cosecha(que se puede mezclar) y bodega destino 
            #ver tanque disponibles
                #si no hay tanque disponible
                    #poner en resumen que no se cumplio y proseguir
                #si hay disponibilidad
                    #heuristica
                        #decidir
                            #flujo(heuristica)-despues
                                #pogramar desicion a que tanque
                        #rellenar tanques(generar dia salida)
                    #si sobro cosecha
                        #poner en resumen que sobro y no se cumplio
                    # si falto cosecha para llenar tanques
                        #poner en resumen y que no se cumplio
                      
    
        
    #computo
        #leer resumen
