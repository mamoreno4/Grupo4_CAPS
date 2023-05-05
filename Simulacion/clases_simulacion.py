from random import uniform, random, seed, randint, gauss
import numpy as np
import pandas as pd
from scipy.stats import binom
import re



class Cuartel:

    def __init__(self, listav):
        self.id=listav[1]
        self.variedad=listav[5]
        self.precio=listav[6]
        self.cosecha_por_dia=dict()

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
        pass

    def fermentar(self,cantidad,dia,variedad,precio,distr):
        if self.estado=="Disponible":
            self.estado="Fermentando"
            self.dia_inicial=dia
            self.cantidad_fermentado=cantidad
            self.variedad_fermentando=variedad
            self.precio=precio
            self.dia_termino=dia+self.generar_dia(variedad,distr)
            print("Se comienza a fermentar {} de variedad {} hasta el día {} ".format(cantidad,variedad,self.dia_termino))
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
        return fermentado
    
    def generar_dia(self,variedad,distr):
        n=distr.loc[variedad][1]
        p=distr.loc[variedad][2]
        dia_generado=binom.rvs(n, p)
        return dia_generado
    
    def __repr__(self):
        return "Tanque {}".format(self.id)+" de la bodega {}".format(self.ubicacion)
    

#Revisar que mas poner en resumen
class Resumen:

    def __init__(self):
        self.dias=dict()
        self.fermentado_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.fermentado_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        self.fermentado_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
        for i in range(100):
            self.dias[i]=[]
        pass

    def agregar_dia(self,dia):
        self.dias[dia]=[]
        pass

    def agregar_cosecha(self,dia,cosecha):
        self.dias[dia].append("Se cosecho "+cosecha)
        pass

    def agregar_fermentado(self,dia,fermentado):
        self.dias[dia].append("Se fermento "+str(fermentado[0])+" de variedad "+str(fermentado[1])+" de precio "+str(fermentado[2])+" en "+ str(fermentado[3]) +" dias")
        pass

    def agregar_sobrante(self,dia,sobrante,precio):
        self.dias[dia].append("El dia"+ str(dia) +" sobro la cantidad de "+str(sobrante)+" de variedad "+str(precio))
        pass

    def agregar_tanque(self, dia, cantidad):
        self.dias[dia].append("El dia"+ dia +" se agrego a tanque la cantidad de "+ cantidad)
        pass
    
    def imprimir_resumen(self):
        for i in self.fermentado_1000:
            for j in self.fermentado_1000[i]:
                print("EL total final fermentado en la bodega {} de cepa {} es {}".format(i,j,self.fermentado_1000[i][j]))
        for i in self.fermentado_3000:
            for j in self.fermentado_3000[i]:
                print("EL total final fermentado en la bodega {} de cepa {} es {}".format(i,j,self.fermentado_3000[i][j]))
        for i in self.fermentado_6000:
            for j in self.fermentado_6000[i]:
                print("EL total final fermentado en la bodega {} de cepa {} es {}".format(i,j,self.fermentado_6000[i][j]))
    


resumen = Resumen()
Distribuciones = pd.read_excel('./../Distribuciones/dist.xlsx', index_col=0)

df = pd.read_csv('solucion.csv')

Cuart = pd.read_excel('Datos Base Ordenados (Cosecha).xlsx')
Los_Cuarteles = []
for i in range(1,61):
    CT = Cuartel(Cuart.iloc[i-1])
    D = df.where(df["Cuartel"] == "cuartel_"+str(i))
    D = D.dropna()
    for j in range(len(D)):
        V = D.iloc[j]["Valor"]
        BB = D.iloc[j]["Bodega"]
        DIA = int(D.iloc[j]["Dia"][4:])
        CT.agregar_cosecha(DIA,[BB,V])
    Los_Cuarteles.append(CT)

Bodegas = pd.read_excel("Datos base G4 (2).xlsx",sheet_name="Tanques")
Las_Bodegas = []
for i in range(3):
    BT = Bodega(Bodegas.iloc[i])
    Las_Bodegas.append(BT)



dia_actual = 1
#Cantidad de cosecha por bodega y cepa
#dictionary = {'key':value}
cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}

#tamaño de tanques para iterar
tamanos_T = [100,75,50,30]
while ((dia_actual < 100)):
    
    print("Dia " + str(dia_actual))
    
    for bodega in Las_Bodegas:
        salidas = bodega.revisar_tanques(dia_actual)
        if len(salidas) == 0:
            #print("No hubo salidas en la bodega " + bodega.ubicacion)
            pass
        else:
            for salida in salidas:
                resumen.agregar_fermentado(dia_actual, salida)
                if salida[3] == 1000:
                    resumen.fermentado_1000[bodega][salida[3]] += salida[0]
                elif salida[3] == 3000:
                    resumen.fermentado_3000[bodega][salida[3]] += salida[0]
                elif salida[3] == 6000:
                    resumen.fermentado_6000[bodega][salida[3]] += salida[0]
                pass

    #Revisar cosecha diaria por cuartel y precio
    for cuartel in Los_Cuarteles:
        if dia_actual in cuartel.cosecha_por_dia:
            if cuartel.precio == 1000:
                CD = cuartel.cosecha_por_dia[dia_actual]
                Nueva = CD[1]
                CCC = cantidad_1000[CD[0]][cuartel.variedad]
                CN = Nueva+CCC
                cantidad_1000[CD[0]][cuartel.variedad] = CN
            elif cuartel.precio == 3000:
                CD = cuartel.cosecha_por_dia[dia_actual]
                Nueva = CD[1]
                CCC=cantidad_1000[CD[0]][cuartel.variedad]
                CN = Nueva + CCC
                cantidad_3000[CD[0]][cuartel.variedad] = CN
            elif cuartel.precio == 6000:
                CD = cuartel.cosecha_por_dia[dia_actual]
                Nueva = CD[1]
                CCC = cantidad_1000[CD[0]][cuartel.variedad]
                CN = Nueva+CCC
                cantidad_6000[CD[0]][cuartel.variedad] = CN

    #Iterar bodegas
    for bodega in Las_Bodegas:
        #establecer bodega actual
        Nbodega = bodega.ubicacion
        #iterar por precio
        for Ncepa in cantidad_6000[Nbodega]:
            #iterar por tamaño de tanque
            for tamano in tamanos_T:
                #boleano para saber si es mas grande que el tanque
                Grande = True
                #mientras sea mas grande que el tanque y haya tanques disponibles
                while ((Grande == True) and (len(bodega.tanques_capacidad(tamano)) > 0)):
                    #selecciona el primer tanque disponible
                    Td = bodega.tanques_capacidad(tamano)[0]
                    #si la cantidad es mayor que el 95% del tanque
                    if cantidad_6000[Nbodega][Ncepa] > tamano*0.95:
                        Td.fermentar(tamano*0.95, dia_actual, Ncepa, 6000, Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_6000[Nbodega][Ncepa] = cantidad_6000[Nbodega][Ncepa] - tamano*0.95
                    #si la cantidad es mayor que el 65% del tanque
                    elif tamano*0.65 <= cantidad_6000[Nbodega][Ncepa] <= tamano*0.95:
                        Td.fermentar(cantidad_6000[Nbodega][Ncepa], dia_actual, Ncepa, 6000, Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_6000[Nbodega][Ncepa] = 0
                        Grande = False
                    #si la cantidad es menor que el 65% del tanque
                    elif cantidad_6000[Nbodega][Ncepa] < tamano*0.65:
                        Grande = False

        for Ncepa in cantidad_3000[Nbodega]:
            for tamano in tamanos_T:
                Grande = True
                while ((Grande == True) and (len(bodega.tanques_capacidad(tamano)) > 0)):
                    Td = bodega.tanques_capacidad(tamano)[0]
                    if cantidad_3000[Nbodega][Ncepa] > tamano*0.95:
                        Td.fermentar(tamano*0.95, dia_actual, Ncepa, 3000, Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_3000[Nbodega][Ncepa] = cantidad_3000[Nbodega][Ncepa] - tamano*0.95
                    elif tamano*0.65 <= cantidad_3000[Nbodega][Ncepa] <= tamano*0.95:
                        Td.fermentar(cantidad_3000[Nbodega][Ncepa], dia_actual, Ncepa, 3000, Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_3000[Nbodega][Ncepa] = 0
                        Grande = False
                    elif cantidad_3000[Nbodega][Ncepa] < tamano*0.65:
                        Grande = False

        for Ncepa in cantidad_1000[Nbodega]:
            for tamano in tamanos_T:
                Grande = True
                while ((Grande == True) and (len(bodega.tanques_capacidad(tamano)) > 0)):
                    Td=bodega.tanques_capacidad(tamano)[0]
                    if cantidad_1000[Nbodega][Ncepa] > tamano*0.95:
                        Td.fermentar(tamano*0.95, dia_actual, Ncepa, 1000, Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_1000[Nbodega][Ncepa] = cantidad_1000[Nbodega][Ncepa] - tamano*0.95
                    elif tamano*0.65 <= cantidad_1000[Nbodega][Ncepa] <= tamano*0.95:
                        Td.fermentar(cantidad_1000[Nbodega][Ncepa], dia_actual, Ncepa, 1000, Distribuciones)
                        bodega.agregar_tanque_fermentando(Td)
                        cantidad_1000[Nbodega][Ncepa] = 0
                        Grande = False
                    elif cantidad_1000[Nbodega][Ncepa] < tamano*0.65:
                        Grande = False
    
    sobras = 0
    for i in cantidad_1000:
        for j in cantidad_1000[i]:
            sobras+=cantidad_1000[i][j]
    if sobras != 0:
        resumen.agregar_sobrante(dia_actual, sobras, 1000)
    sobras = 0
    for i in cantidad_3000:
        for j in cantidad_3000[i]:
            sobras += cantidad_3000[i][j]
    if sobras != 0:
        resumen.agregar_sobrante(dia_actual, sobras, 3000)

    sobras = 0
    for i in cantidad_6000:
        for j in cantidad_6000[i]:
            sobras+=cantidad_6000[i][j]
    if sobras != 0:
        resumen.agregar_sobrante(dia_actual, sobras, 6000)
    sobras = 0
    if len(resumen.dias[dia_actual]) > 0:
        print(resumen.dias[dia_actual])

    
    cantidad_1000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
    cantidad_3000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
    cantidad_6000 = {'Machali':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Chepica':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}, 'Nancagua':{'G':0, 'Ch':0, 'SB':0, 'C':0, 'CS':0, 'S':0, 'M':0, 'CF':0, 'V':0}}
    dia_actual = dia_actual + 1

#Se imprime el resumen de todo lo fermentado
resumen.imprimir_resumen()


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
    #Computo
        #Leer resumen
