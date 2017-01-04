from agent import Agent
import random

def initialisation(w, h,n):
		tab=[[0]*h]*w
		for i in range(w):
			for j in range(h):
				tab[i][j]= []
		for k in range(n-1):
			x=random.randint(0,w-1)
			y=random.randint(0,h-1)
			tab[x][y].append(Agent(0))
		x=random.randint(0,w-1)
		y=random.randint(0,h-1)
		tab[x][y].append(Agent(1))
		return tab 
		
		
		
print (initialisation(10,5,5))

	
	
