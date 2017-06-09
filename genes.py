import numpy as np
import random as rd
import poblacion as pob

def combinar(ind1, ind2):

	if np.random.randint(0, 2) == 1:
		i = pob.Individuo(ind1.dur_cambio, ind1.simple)
	else:
		i = pob.Individuo(ind2.dur_cambio, ind2.simple)

	if np.random.randint(0, 2) == 1:
		i.o = ind1.o
	else:
		i.o = ind2.o

	if np.random.randint(0, 2) == 1:
		i.l = ind1.l
	else:
		i.l = ind2.l

	if np.random.randint(0, 2) == 1:
		i.op = ind1.op
	else:
		i.op = ind2.op

	if np.random.randint(0, 2) == 1:
		i.lp = ind1.lp
	else:
		i.lp = ind2.lp

	return i
	
def clonar(ind1):
	i = pob.Individuo(ind1.dur_cambio, ind1.simple)
	i.o = ind1.o
	i.l = ind1.l
	i.op = ind1.op
	i.lp = ind1.lp
	i.dur_cambio = ind1.dur_cambio
	i.puntuacion = ind1.puntuacion
	return i

def mutar(ind):
	i = clonar(ind)

	a = np.random.randint(0, 5)
	if np.random.randint(0, 2) == 1:
		change=-rd.random()*0.2
		if a==0:
			i.dur_cambio = i.dur_cambio + np.random.randint(1, 6) 
	else:
		change=0.1
		if a==0:
			i.dur_cambio = i.dur_cambio - np.random.randint(1, 6)
	if a==1:
		i.o = i.o + change*i.o
	elif a==2:
		i.l = i.l + change*i.l
	elif a==3:
		i.op = i.op + change*i.op
	else:
		i.lp = i.lp + change*i.lp

	return i
