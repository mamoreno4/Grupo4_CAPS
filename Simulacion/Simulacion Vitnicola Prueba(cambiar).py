from datetime import date, datetime, timedelta
from random import uniform, random, seed, randint, gauss
import numpy as np
import pandas as pd
import time as tm
#revisar que se queda
#quitar tiempos? Simulacion motecarlo?
#clases se quedan?
#dejar cuartel? como revisar cepas? clase o al inciar simulacion?
class Cuartel:
    def __init__(self, listav,cosecha_aproximada):
        self.id=listav[0]
        self.variedad=listav[4]
        self.precio=listav[5]
        self.cantidad_dia=cosecha_aproximada
    def __str__(self):
        return "-> {}".format(self.id)
#trabajadores no se quedan, quitar
#class Grupo_trabajador:
 #   def __init__(self,lista_valores):
  #      pass
#dejar bodega?
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
        self.tanques_disponibles=[]
        self.tanques_fermentando=[]
        for i in self.tanques:
            if i.estado=="Disponible":
                self.tanques_disponibles.append(i)
            elif i.estado=="Fermentando":
                self.tanques_fermentando.append(i)
            else:
                pass
    def tanques_disponibles(self):
        pass

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
        fermentado=[self.cantidad_fermentado,self.variedad_fermentando]
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
        #revisar tanques
        #tanques disponibles(return que tanque con que capacidad esta disponible)
    #Tanques
        #generar dia
        #revisar tanques(llamar vaciar tanques)
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
