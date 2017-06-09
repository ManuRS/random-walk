import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt

class Tablero:

	def __init__(self, dimension):
		self.t = np.zeros((dimension, dimension))

	def __init__(self, dimension, radio_monton):

		#Esta clase da cansersito
		#Los centroides se añaden de 4 en 4
		#Es para que esten mas o menos equilibrados

		self.t = np.zeros((dimension, dimension))
		mitad = dimension / 2
		self.dim = dimension
		self.num_comida=0

		for asd in range(2):

			centro_ax = np.random.randint(radio_monton, mitad-1-radio_monton)
			centro_ay = np.random.randint(radio_monton, mitad-1-radio_monton)

			centro_bx = np.random.randint(mitad+radio_monton, dimension-1-radio_monton)		
			centro_by = np.random.randint(0+radio_monton, mitad-1-radio_monton)

			centro_cx = np.random.randint(radio_monton, mitad-1-radio_monton)		
			centro_cy = np.random.randint(mitad+radio_monton, dimension-1-radio_monton)

			centro_dx = np.random.randint(mitad+radio_monton, dimension-1-radio_monton)		
			centro_dy = np.random.randint(mitad+radio_monton, dimension-1-radio_monton)

		

			for i in range (radio_monton):
				for j in range(radio_monton):
					self.t[centro_ax+i][centro_ay+j] = 1
					self.t[centro_ax+i][centro_ay-j] = 1
					self.t[centro_ax-i][centro_ay-j] = 1
					self.t[centro_ax-i][centro_ay+j] = 1

					self.t[centro_bx+i][centro_by+j] = 1
					self.t[centro_bx+i][centro_by-j] = 1
					self.t[centro_bx-i][centro_by-j] = 1
					self.t[centro_bx-i][centro_by+j] = 1

					self.t[centro_cx+i][centro_cy+j] = 1
					self.t[centro_cx+i][centro_cy-j] = 1
					self.t[centro_cx-i][centro_cy-j] = 1
					self.t[centro_cx-i][centro_cy+j] = 1

					self.t[centro_dx+i][centro_dy+j] = 1
					self.t[centro_dx+i][centro_dy-j] = 1
					self.t[centro_dx-i][centro_dy-j] = 1
					self.t[centro_dx-i][centro_dy+j] = 1

		#self.x=[]
		#self.y=[]
		for i in range (len(self.t)):
			for j in range(len(self.t)):	
				if self.t[i][j]==1:	
					self.num_comida+=1
					#self.x.append(i)
					#self.y.append(j)

	def copia_t(self):
		return deepcopy(self)

	def print_t(self):

		for i in range (len(self.t)):
			for j in range(len(self.t)):
				if self.t[i][j]==1:
					print('O', end=' ')
				else:
					print(' ', end=' ')
			print('')

	def plot_t(self, c1, c2, c11, c22):
		x=[]
		y=[]
		for i in range (len(self.t)):
			for j in range(len(self.t)):	
				if self.t[i][j]==1:	
					x.append(i)
					y.append(j)

		plt.figure(figsize=(10,10))
		plt.plot(x, y, 'o', color='green', label='Disponibles')
		plt.plot(c1, c2, '--', color='blue', label='Caminante', alpha=0.5)
		plt.plot(c11, c22, 'o', color='red', label='Comidos')
		plt.plot(c1[0], c2[0], 'o', color='black')
		plt.xlim([0,self.dim])
		plt.ylim([0,self.dim])
		plt.legend(loc='best')
		plt.savefig('best.svg', format='svg')
