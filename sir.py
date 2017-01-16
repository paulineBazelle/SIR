from agent import Agent
import random
import numpy as np

def initialisation(w, h,n, num_simul, pr, pm, pi):
		#tab=[[0]*h]*w
		#for i in range(w):
		#	for j in range(h):
		#		tab[i][j]= []
		f= open("donnees.txt","w")
		f.write("Simulation " + str(num_simul) + "\n")
		f.write(str(w)+ "\n")
		f.write(str(h)+ "\n")
		f.write(str(n)+ "\n")
		f.write(str(pr)+ "\n")
		f.write(str(pm)+ "\n")
		f.write(str(pi)+ "\n")
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
		

def move():
		f=open("donnees.txt","r")
		#Lit tout le fichier
		l=f.readlines()
		f.close()
		
		#Recupere la taille de la grille
		t=len(l[1])-2
		if t!=0:
			w=int(l[1][0:t])	#Enleve le caractere de retour a la ligne et transforme en entier
		else:
			w=int(l[1][0])
		t=len(l[2])-2
		if t!=0:
			h=int(l[2][0:t])
		else:
			h=int(l[2][0])
		
		f=open("donnees.txt","w")
		#Modifie l'etape 
		l[8]="Move \n"
		#Ecrit la simulation, les parametres, le pas et l'etape dans le fichier
		for i in range(9):
			f.write(l[i])
		
		#Parcoure les n-9 lignes du fichier qui presente la position et l'etat
		for i in range(9,len(l)):
			#Recupere coordonnees x et y et l'etat
			split=l[i].split(" ")
			x=int(split[0])
			y=int(split[1])
			etat=int(split[2])
			#Effectue le deplacement de chaque agent
			#Tire un deplacement aleatoire
			d=random.choice(["n","s","e","o"])
			#se deplace selon de deplacement aleatoire tire
			if(d=="n"):
				y=y+1
				#Verifie que y ne sors pas de l'environnement
				if y==h:
					y=0
			if(d=="s"):
				y=y-1
				if y==-1:
					y=h-1
			if(d=="e"):
				x=x+1
				if x==w:
					x=0
			if(d=="o"):
				x=x-1
				if x==-1:
					x=w-1
			#Ecrit les nouvelles coordonnees des agents dans le fichier
			f.write(str(x) + " " + str(y) + " " + str(etat) + "\n")
		f.close()
			
def infection():
		#Lecture du fichier
		f = open('donnees.txt','r')
		lines = f.readlines()
		f.close()

		#recuperation de la taille de la grille
		w = int(lines[1].replace('\n', ''))
		h = int(lines[2].replace('\n', ''))
		#recuperation du nombre d'agents
		N = int(lines[3].replace('\n', ''))
		#recuperation de pi
		pi = float(lines[6].replace('\n', ''))

		#creation de la grille
		grid = np.zeros((w,h))
		grid = grid.tolist()
		for i in range(w):
			for j in range(h):
				grid[i][j]= []

		#ajout des agents a leur position dans la grille
		for l in lines[9:]:
			line = l.split()
			x = int(line[0])
			y = int(line[1])
			etat = int(line[2])
			agent = Agent(etat,x,y)
			grid[x][y].append(agent)

		#infection
		for i in range(w):
			for j in range(h):
				if grid[i][j]:
					infected = False
					for agent in grid[i][j]:
						if agent.etat == 1:
							infected = True
							break
					if infected:
						p = random.random()
						if p <= pi:
							for agent in grid[i][j]:
								if agent.etat == 0:
									agent.etat = 1

		#Fichier de sortie
		f = open('donnees.txt','w')
		#Ecrit les parametres
		for line in lines[:8]:
			f.write(line)
		#Ecrit la nouvelle etape
		f.write('Infect\n')
		#Ecrit les nouveaux etats des agents
		for i in range(w):
			for j in range(h):
				if grid[i][j]:
					for agent in grid[i][j]:
						f.write(str(agent.x) + " " + str(agent.y) + " " + str(agent.etat) + "\n")
		f.close()

		
initialisation(10,5,5,1,0.5,0.4,0.1)
#move()
#infection()
	
	
