from random import uniform, random, seed, randint, gauss
import numpy as np
import pandas as pd
from scipy.stats import binom


class Cuartel:

    def __init__(self, listav):
        self.id=listav[1]
        self.variedad=listav[5]
        self.precio=listav[6]
        self.cosecha_por_dia=dict()

    def agregar_cosecha(self,dia,cantidad):
        self.cosecha_por_dia[dia]=cantidad
        pass

    def __str__(self):
        return "-> {}".format(self.id)
    
    def __repr__(self):
        return "Cuartel {}".format(self.id)
    

class Bodega:

    def __init__(self,ubicacion_tanques):
        self.id_tanque=0
        self.ubicacion=ubicacion_tanques[0]
        self.tanques=[]
        self.tanques_fermentando=[]
        self.tanques_disponibles=[]
        tanques_30=ubicacion_tanques[1]
        tanques_50=ubicacion_tanques[2]
        tanques_75=ubicacion_tanques[3]
        tanques_100=ubicacion_tanques[4]
        for i in range(tanques_30):
            T=Tanque(30,self.ubicacion,self.id_tanque)
            self.id_tanque+=1
            self.agregar_tanque_disponible(T)
        for i in range(tanques_50):
            T=Tanque(50,self.ubicacion,self.id_tanque)
            self.id_tanque+=1
            self.agregar_tanque_disponible(T)
        for i in range(tanques_75):
            T=Tanque(75,self.ubicacion,self.id_tanque)
            self.id_tanque+=1
            self.agregar_tanque_disponible(T)
        for i in range(tanques_100):
            T=Tanque(100,self.ubicacion,self.id_tanque)
            self.id_tanque+=1
            self.agregar_tanque_disponible(T)
        pass

    def agregar_tanque_disponible(self,tanque):
        self.tanques.append(tanque)
        self.tanques_disponibles.append(tanque)
        pass

    def agregar_tanque_fermentando(self,tanque):
        self.tanques.append(tanque)
        self.tanques_fermentando.append(tanque)
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
        pass

    def fermentar(self,cantidad,dia,variedad,precio,distr):
        if self.estado=="Disponible":
            self.estado="Fermentando"
            self.dia_inicial=dia
            self.cantidad_fermentado=cantidad
            self.variedad_fermentando=variedad
            self.precio=precio
            self.dia_termino=dia+self.generar_dia(dia,variedad,distr)
            return self
        else:
            return "Error: tanque no Disponible"
        
    def vaciar_tanque(self):
        dias_fermentando=self.dia_termino-self.dia_inicial
        fermentado=[self.cantidad_fermentado,self.variedad_fermentando,self.variedad_fermentando,dias_fermentando]
        self.cantidad_fermentado=0
        self.variedad_fermentando=""
        self.dia_inicial=0
        self.dia_termino=0
        self.estado="Disponible"
        return fermentado
    
    def generar_dia(self,dia,variedad,distr):
        Dist=distr[distr["Cepa"]==variedad]
        n=Dist.iloc[0][2]
        p=Dist.iloc[0][3]
        dia_generado=binom.rvs(n, p)
        return dia_generado
    
    def __repr__(self):
        return "Tanque {}".format(self.id)+" de la bodega {}".format(self.ubicacion)
    

#Revisar que mas poner en resumen
class Resumen:

    def __init__(self):
        self.dias=dict()
        for i in range(100):
            self.dias["Dia "+i]=[]
        pass

    def agregar_dia(self,dia):
        self.dias["Dia "+dia]=[]
        pass

    def agregar_cosecha(self,dia,cosecha):
        self.dias["Dia "+dia].append("Se cosecho "+cosecha)
        pass

    def agregar_fermentado(self,dia,fermentado):
        self.dias["Dia "+dia].append("Se fermento "+fermentado[0]+" de variedad "+fermentado[1]+" de precio "+fermentado[2]+" en "+ fermentado[3] +" dias")
        pass

    def agregar_sobrante(self,dia,sobrante):
        self.dias["Dia "+dia].append("El dia"+ dia +" sobro la cantidad de "+sobrante)
        pass

    def agregar_tanque(self, dia, cantidad):
        self.dias["Dia "+dia].append("El dia"+ dia +" se agrego a tanque la cantidad de "+ cantidad)
        pass
    



Distribuciones= pd.read_excel('./../Distribuciones/dist.xlsx')


Cuart= pd.read_excel('Datos Base Ordenados (Cosecha).xlsx')
Los_Cuarteles=[]
for i in range(60):
    CT=Cuartel(Cuart.iloc[i])
    Los_Cuarteles.append(CT)

Bodegas=pd.read_excel("Datos base G4 (2).xlsx",sheet_name="Tanques")
Las_Bodegas=[]
for i in range(3):
    BT=Bodega(Bodegas.iloc[i])
    Las_Bodegas.append(BT)







#Crear clases (Cuarteles,Bodegas,Tanques,Resumen)
    #Bodegas
        #revisar tanques(listo)
        #tanques disponibles(return que tanque con que capacidad esta disponible)(listo)
    #Tanques
        #generar dia(listo)
        #revisar tanques(llamar vaciar tanques)(listo)
    #Resumen
        #crear estructura(casi listo)

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
