from random import uniform, seed, randint, gauss
from numpy.random import Generator, PCG64
import numpy as np
import pandas as pd
from scipy.stats import binom



class Cuartel:

    def __init__(self, listav):
        self.id=listav[1]
        self.variedad=listav[5]
        self.precio=listav[6]
        self.cosecha_por_dia=dict()
        self.dia_optimo=0

    def agregar_cosecha(self,dia,cantidad_bodega):
        self.cosecha_por_dia[dia]=cantidad_bodega
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
        self.tanques_disponibles.remove(tanque)
        self.tanques_fermentando.append(tanque)
        print("Se agrega tanque {} a fermentar".format(tanque.id))
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
            print("Se comienza a fermentar {} de variedad {} hasta el día {} en la bodega {}".format(cantidad,variedad,self.dia_termino,self.ubicacion))
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
        self.fermentado_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.fermentado_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.fermentado_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        
        self.sobras_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.sobras_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.sobras_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}

        
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
    def dias_promedio_fermentacion(self):
        Promedio = 0
        for i in self.dias_generados:
            Promedio += i
        Promedio = Promedio/len(self.dias_generados)
        return Promedio
    
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