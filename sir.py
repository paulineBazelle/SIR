from agent import Agent
import random

def initialisation(w, h,n, num_simul, pr, pm, pi):
		#tab=[[0]*h]*w
		#for i in range(w):
		#	for j in range(h):
		#		tab[i][j]= []
		f= open("donnees.txt","w")
		f.write("Simulation " + str(num_simul) + "\n")
		f.write(str(w) +" "+ str(h) +" " + str(n) + " "+ str(pr) + " " + str(pm) + " " + str(pi) +"\n")
		f.write("0" + "\n")
		f.write("Initialisation" +"\n")
		for k in range(n-1):
			x=random.randint(0,w-1)
			y=random.randint(0,h-1)
			f.write(str(x) +" " + str(y) + " 0\n")
			#tab[x][y].append(Agent(0))
		x=random.randint(0,w-1)
		y=random.randint(0,h-1)
		f.write(str(x) +" " + str(y) + " 1\n")
		#tab[x][y].append(Agent(1))
		f.close()
		
		




		
initialisation(10,5,5,1,0.5,0.4,0.1)

	
	
