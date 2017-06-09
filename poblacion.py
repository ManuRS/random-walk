import numpy as np
import random as rd
from copy import deepcopy
import math

class Poblacion:
	def __init__(self, num_poblacion, dur_cambio, simple):
		self.num = num_poblacion
		self.l = []
		for i in range (num_poblacion):
			self.l.append(Individuo(dur_cambio, simple))
			
	def vaciar(self):
		self.l=[]
		self.num = 0
		
	def add_inv(self, ind):
		self.l.append(ind)
		self.num+=1
		
	def get_individuo(self, i):
		return self.l[i]

	def get_best_guy(self):
		maxP=-1
		for ind in self.l:
			if ind.puntuacion>maxP:
				maxP=ind.puntuacion
				select=ind
		return select

	def get_best_guy_limit(self, limit):
		maxP=-1
		for ind in self.l:
			if ind.puntuacion>maxP and ind.puntuacion<limit:
				maxP=ind.puntuacion
				select=ind
		return select

	def get_worst_guy(self):
		minP=999999
		for ind in self.l:
			if ind.puntuacion<minP:
				minP=ind.puntuacion
				selec=ind
		return selec

	def fit_medio(self):
		sum=0
		for ind in self.l:
			sum+=ind.puntuacion
		return sum/len(self.l)

	def reset_puntuaciones(self, simple):
		for ind in self.l:
			ind.puntuacion=0
			if simple==True:
				ind.x=0
				ind.y=0
			else:
				ind.x=rd.random()
				ind.y=rd.random()

class Individuo:
	def __init__(self, dur_cambio, simple):
		self.o_old=rd.random()*2*math.pi
		self.o=rd.random()*2*math.pi
		self.l=rd.random()*0.2
		self.op=rd.random()*2*math.pi
		self.lp=rd.random()*0.9
		if dur_cambio<1:
			dur_cambio=1
		self.dur_cambio=np.random.randint(0, dur_cambio)
		self.simple=simple
		if simple==True:
			self.x=0
			self.y=0
		else:
			self.x=rd.random()
			self.y=rd.random()
		self.act_cambio=0
		self.puntuacion=0
		self.xx=0
		self.yy=0
		self.xl=[]
		self.yl=[]

	def get_comiendo(self):
		if self.act_cambio==0:
			return False
		else:
			self.act_cambio-=1
			return True

	def start_comiendo(self):
		self.act_cambio=self.dur_cambio

	def da_paseo(self):

		self.xl.append(self.xx)
		self.yl.append(self.yy)

		if self.get_comiendo()==False:
			ang = self.o_old+self.o%(2*math.pi)
			ang += np.random.normal(0,0.05) % (2*math.pi)
			self.o_old=ang
			self.x = self.x + self.l * math.cos(ang)
			self.y = self.y + self.l * math.sin(ang)
			self.xx = self.xx + self.l * math.cos(ang)
			self.yy = self.yy + self.l * math.sin(ang)

		else:
			ang = self.o_old+self.op%(2*math.pi)
			ang += np.random.normal(0,0.05) % (2*math.pi)
			self.o_old=ang
			self.x = self.x + self.lp * math.cos(ang)
			self.y = self.y + self.lp * math.sin(ang)	
			self.xx = self.xx + self.l * math.cos(ang)
			self.yy = self.yy + self.l * math.sin(ang)

		
		r = np.random.normal(0,0.01)
		r2 = np.random.normal(0,0.01)
		self.x += r 
		self.xx += r
		self.y += r2
		self.yy += r2
		

		while self.x>1.0:
			self.x-=1

		while self.x<0.0:
			self.x+=1
	
		while self.y>1.0:
			self.y-=1

		while self.y<0.0:
			self.y+=1
