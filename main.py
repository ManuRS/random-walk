import numpy as np
import random as rd
import math
from copy import deepcopy
from matplotlib import pyplot as plt

import poblacion as pob
import tablero as tab
import genes

tam_t = 400
dim_m = 24
dur_cambio = 20
generaciones = 250
individuos = 20
simple=False
poblacion = pob.Poblacion(individuos, dur_cambio, simple)
duracion_paseo=1000
elite=5
num_reps=1

file = open('info.txt','w') 

file.write("CAMINANTE NO HAY CAMINO, SE HACE CAMINO AL ANDAR\n")
print("CAMINANTE NO HAY CAMINO, SE HACE CAMINO AL ANDAR")

file.write("Tamaño cuadricula = "+str(tam_t)+"\n")
print("Tamaño cuadricula = "+str(tam_t))

file.write("Diámetro monticulos = "+str(dim_m)+"\n")
print("Diámetro monticulos = "+str(dim_m))

file.write("Generaciones = "+str(generaciones)+"\n")
print("Generaciones = "+str(generaciones))

file.write("Individuos = "+str(individuos)+"\n")
print("Individuos = "+str(individuos))

file.write("Duracion paseo = "+str(duracion_paseo)+"\n")
print("Duracion paseo = "+str(duracion_paseo))

t = tab.Tablero(tam_t, dim_m) 
file.write("Comidas = "+str(t.num_comida)+"\n")
print("Comidas = "+str(t.num_comida))

file.write("Montones = 8\n")
print("Montones = 8")

file.write("Elite = "+str(elite)+"\n")
print("Elite = "+str(elite))
#if simple==False:
	#print("Tableros por individuo en una generacion = "+str(num_reps))
#print("Modo simple = "+str(simple))

los_mejores=[]
fit_medio=[]
los_peores=[]
counter_barra=1

if duracion_paseo<t.num_comida:
	div=duracion_paseo
else:
	div=t.num_comida

#Generaciones
if simple==True:
	#Mismo tablero siempre, para que el best siempre mejore
	t = tab.Tablero(tam_t, dim_m)
else:
	tableros=[]
	for i in range(num_reps):
		tableros.append(tab.Tablero(tam_t, dim_m))

for g in range(generaciones):
	if(math.fmod(g,10)==0):
		print("Generacion "+str(g)+"/"+str(generaciones))

	if(math.fmod(g,generaciones/10.0)==0):
		print('[', end='')
		for i in range(counter_barra):
			print('=', end='')
		for i in range(10-counter_barra):
			print('-', end='')
		counter_barra+=1
		print(']')
		
	poblacion.reset_puntuaciones(simple)

	#Individuos caminan
	for i in range(individuos):
		ind = poblacion.get_individuo(i)

		if simple==True:
			#Individuo camina
			t2 = t.copia_t()
			for dur in range(duracion_paseo):
				ind.da_paseo()
				if t2.t[ int (ind.x*tam_t) ][ int (ind.y*tam_t) ] == 1:
					t2.t[ int (ind.x*tam_t) ][ int (ind.y*tam_t) ] = 0
					ind.puntuacion+=1
					ind.start_comiendo()
		else:
			#Para que la puntuacion sea realista les hacemos a cada uno recorrer varios tableros
			for t in tableros:
				t2 = t.copia_t() 
				for dur in range(duracion_paseo):
					ind.da_paseo()
					if t2.t[ int (ind.x*tam_t) ][ int (ind.y*tam_t) ] == 1:
						t2.t[ int (ind.x*tam_t) ][ int (ind.y*tam_t) ] = 0
						ind.puntuacion+=1
						ind.start_comiendo()
			ind.puntuacion=ind.puntuacion/num_reps

	#Elite
	new_gen=[]
	elite_list=[]
	best=genes.clonar(poblacion.get_best_guy())
	elite_list.append(best)
	limite=best.puntuacion

	'''
	print ("\n==GEN=="+str(g))
	print ("o = "+str(int( ((best.o*360)/(2*math.pi))%360 ))+"º")
	print ("l = {0:.2f}%".format(best.l*100))
	print ("op = "+str(int( ((best.op*360)/(2*math.pi))%360 ))+"º")
	print ("l = {0:.2f}%".format(best.lp*100))
	print ("dc = "+str(best.dur_cambio))	
	'''

	for i in range(elite-1):
		tipo=poblacion.get_best_guy_limit(limite)
		elite_list.append(tipo)
		limite=tipo.puntuacion

	los_mejores.append(best.puntuacion/div)
	los_peores.append(poblacion.get_worst_guy().puntuacion/div)
	fit_medio.append(poblacion.fit_medio()/div)

	#Recombinar
	aux_gen=[]

	#Propiciamos que los mejores se reproduzcan mas
	for i in range(individuos):
		a = poblacion.get_individuo(np.random.randint(0, individuos))
		b = poblacion.get_individuo(np.random.randint(0, individuos))
		if a.puntuacion>b.puntuacion:
			aux_gen.append(a)
		else:
			aux_gen.append(b)

	#Reproduccion
	for i in range(individuos-elite):
		ind_a = aux_gen[np.random.randint(0, individuos)]
		ind_b = aux_gen[np.random.randint(0, individuos)]
		new_gen.append(genes.combinar(ind_a, ind_b))

	#Mutacion
	for i in range(individuos-elite):
		if rd.random()>0.2:
			ind = new_gen[i]
			new_gen[i] = genes.mutar(ind)

	#Old gen die
	for tipo in elite_list:
		new_gen.append(tipo)
	poblacion.vaciar()
	for i in range(individuos):
		poblacion.add_inv(new_gen[i])

#Info de la evolucion
plt.figure(figsize=(10,10))
plt.plot(los_mejores, color='green', label='Mejores')
plt.plot(los_peores, color='red', label='Peores')
plt.plot(fit_medio, color='blue', label='Fit medio')
plt.ylim([0,1])
plt.ylabel('Pocentaje capturado')
plt.xlabel('Generacion')
plt.title('Evolucion algoritmo genetico')
plt.legend(loc='best')
plt.savefig('evol.svg', format='svg')

#Impresion del mejor dando un paseito
mejor = poblacion.get_best_guy()
mejor.puntuacion=0
if simple==True:
	mejor.x=0
	mejor.y=0
else:
	mejor.x=rd.random()
	mejor.y=rd.random()

#Lo hacemos varias veces para tener una puntuacion mas fina
num_reps_final=4
for veces in range(num_reps_final):
	t2 = tab.Tablero(tam_t, dim_m) 
	for dur in range(duracion_paseo):
		mejor.da_paseo()
		if t2.t[ int (mejor.x*tam_t) ][ int (mejor.y*tam_t) ] == 1:
			mejor.puntuacion+=1
			mejor.start_comiendo()
	if simple==True:
		mejor.x=0
		mejor.y=0
	else:
		mejor.x=rd.random()
		mejor.y=rd.random()

#La ultima vez me guardo el camino y las cosas para pintarlo
t2 = tab.Tablero(tam_t, dim_m) 
x=[]
y=[]
c1=[]
c2=[]
x.append( int (mejor.x*tam_t) )
y.append( int (mejor.y*tam_t) )

for dur in range(duracion_paseo):
	mejor.da_paseo()
	x.append( int (mejor.x*tam_t) )
	y.append( int (mejor.y*tam_t) )
	if t2.t[ int (mejor.x*tam_t) ][ int (mejor.y*tam_t) ] == 1:
		t2.t[ int (mejor.x*tam_t) ][ int (mejor.y*tam_t) ] = 0
		c1.append( int (mejor.x*tam_t) ) 
		c2.append( int (mejor.y*tam_t) )
		mejor.puntuacion+=1
		mejor.start_comiendo()

t2.plot_t(x, y, c1, c2) # El plot es solo un ejemplo

file.write ("\n*******************************\n\n")
print ("\n*******************************\n")

file.write ("Puntuacion final = {0:.2f}%\n".format((mejor.puntuacion/(num_reps_final+1))/div*100))
print ("Puntuacion final = {0:.2f}%".format((mejor.puntuacion/(num_reps_final+1))/div*100))

file.write ("o = "+str(int( ((mejor.o*360)/(2*math.pi))%360 ))+"º\n")
print ("o = "+str(int( ((mejor.o*360)/(2*math.pi))%360 ))+"º")

file.write ("l = {0:.2f}%\n".format(mejor.l*100))
print ("l = {0:.2f}%".format(mejor.l*100))

file.write ("op = "+str(int( ((mejor.op*360)/(2*math.pi))%360 ))+"º\n")
print ("op = "+str(int( ((mejor.op*360)/(2*math.pi))%360 ))+"º")

file.write ("l = {0:.2f}%\n".format(mejor.lp*100))
print ("l = {0:.2f}%".format(mejor.lp*100))

file.write ("dc = "+str(mejor.dur_cambio)+'\n')	
print ("dc = "+str(mejor.dur_cambio))	

file.write ("\n*******************************\n\n")
print ("\n*******************************\n")

file.write ("Ahora la movida final\n")
print ("Ahora la movida final")

listasx=[]
listasy=[]
mejor.xl=[]
mejor.yl=[]
mejor.x=0
mejor.xx=0
mejor.y=0
mejor.yy=0
mejor.o_old=rd.random()*2*math.pi

duracion_paseo=16000
num_mejores=10
for i in range(num_mejores):
	t2 = tab.Tablero(tam_t, dim_m) 
	for dur in range(duracion_paseo):
		mejor.da_paseo()
		if t2.t[ int (mejor.x*tam_t) ][ int (mejor.y*tam_t) ] == 1:
			mejor.puntuacion+=1
			mejor.start_comiendo()
	
	mejor.x=0
	mejor.xx=0
	mejor.y=0
	mejor.yy=0
	listasx.append(mejor.xl)
	mejor.xl=[]
	listasy.append(mejor.yl)
	mejor.yl=[]

plt.close('all')
plt.figure(figsize=(15,5))
for subx in listasx:
	plt.plot(subx)
plt.savefig('camx.svg', format='svg')

plt.close('all')
plt.figure(figsize=(15,5))
for subx in listasy:
	plt.plot(subx)
plt.savefig('camy.svg', format='svg')

mediasx=[]
mediasy=[]
mediasxy=[]
varx=[]
vary=[]
varxy=[]
for j in range(duracion_paseo):
	mediax=0
	mediay=0
	sumx=0
	sumy=0

	for i in range(num_mejores):
		mediax += listasx[i][j]
		mediay += listasy[i][j]
	mediax = mediax / num_mejores
	mediay = mediay / num_mejores
	mediasx.append(mediax)
	mediasy.append(mediay)
	mediasxy.append(mediax+mediax)

	for i in range(num_mejores):
		sumx += (listasx[i][j] - mediax)**2
		sumy += (listasy[i][j] - mediay)**2
	sumx = sumx / num_mejores
	sumy = sumy / num_mejores
	varx.append(sumx)
	vary.append(sumy)
	varxy.append(sumx+sumy)

plt.close('all')
plt.figure(figsize=(10,15))

plt.figure(1)

plt.subplot(611)
plt.title('Media x')
plt.plot(mediasx)
plt.xticks([])

plt.subplot(612)
plt.title('Media y')
plt.plot(mediasy)
plt.xticks([])

plt.subplot(613)
plt.title('Media x+y')
plt.plot(mediasxy)
plt.xticks([])

plt.subplot(614)
plt.title('Varianza x')
plt.plot(varx)
plt.xticks([])

plt.subplot(615)
plt.title('Varianza y')
plt.plot(vary)
plt.xticks([])

plt.subplot(616)
plt.title('Varianza x+y')
plt.plot(varxy)

plt.savefig('var.svg', format='svg')

file.close() 

plt.figure(figsize=(8,8))
plt.title('Varianza x+y')
plt.plot(varxy)
plt.savefig('varxy.svg', format='svg')

