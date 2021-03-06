from agent import Agent
import random
import numpy as np
import socket 
import select
import time
import sys
import signal
#import matplotlib.pyplot as plt (pour le graphic final)

def initialisation(w, h,n, pr, pm, pi):
  #tab=[[0]*h]*w
  #for i in range(w):
  #	for j in range(h):
  #		tab[i][j]= []
  f= open("donnees.txt","w")
  f.write("Create\n")
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
  l[8]="Move\n"
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


#rappel : 0: sain , 1: infecte, 2: resistant, 3 :mort
def update(): 
	#Lecture du fichier 
	f = open('donnees.txt','r') 
 	lines = f.readlines() 
	f.close() 
 
 
 	#recuperation de la taille de la grille 
 	w = int(lines[1].replace('\n', '')) 
 	h = int(lines[2].replace('\n', '')) 
 	#recuperation du nombre d'agents 
 	N = int(lines[3].replace('\n', '')) 
 	#recuperation de pr 
 	pr = float(lines[4].replace('\n', '')) 
	#recuperation de pm
 	pm = float(lines[5].replace('\n', '')) 
 
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
 
 
	#Resistance ou mort
 	for i in range(w): 
 		for j in range(h): 

			for agent in grid[i][j]: 
 				if agent.etat == 1:  
 					p = random.random()
 					if p <= pr: 
						agent.etat = 2 
					else : 
						if (p>pr and p<=(pm+pr)): 
							agent.etat=3
 
 
 	#Fichier de sortie 
	f = open('donnees.txt','w') 
 	for line in lines[:8]: 
 		f.write(line) 
 	#Ecrit la nouvelle etape 
 	f.write('Update\n') 
 	#Ecrit les nouveaux etats des agents 
 	for i in range(w): 
 		for j in range(h): 
 			if grid[i][j]: 
				for agent in grid[i][j]: 
					f.write(str(agent.x) + " " + str(agent.y) + " " + str(agent.etat) + "\n") 
 	f.close() 


def count(state,n_s,n_i,n_r,n_m): 
	if int(state) == 0: #sain
		n_s += 1
	elif int(state) == 1: #infecte
		n_i += 1
	elif int(state) == 2: #resistant / retire
		n_r += 1
	else: #mort
		n_m += 1
	return n_s,n_i,n_r,n_m
		
def stats():
  f=open("donnees.txt", "r")
  f2=open("f_output.txt","w")
  lines = f.readlines() 
	#n_simulations= sim[11] #utile pour le graphique
  for i in range(8):
    f.readline(9)
  for line in lines[:8]: 
    f2.write(line)
  f2.write('\n')
  f2.write('Stats\n') 
  n_s = 0
  n_i = 0
  n_r = 0
  n_m = 0
	#~ sains = []
	#~ infectes = []
	#~ retires = []
	#~ morts = []
  for i in lines[9:]:
    state = i[4]
    n_s,n_i,n_r,n_m = count(state,n_s,n_i,n_r,n_m)
	#output file
  f2.write("sains " + str(n_s) +' \n')
  f2.write("infectes " + str(n_i) +' \n')
  f2.write("retires " + str(n_r) +' \n')
  f2.write("morts " + str(n_m) +' \n')
  f.close()
  f2.writelines(lines[9:])
  f2.close()
	#ca c'est pour faire le graphique
	#~ sains.append(n_s)  
	#~ infectes.append(n_i)
	#~ retires.append(n_r)
	#~ morts.append(n_m)
	

###After all the simulations
#Plot of the population
#~ def creates_plot(n_simulations,sains,infectes,retires,morts): 
	#~ t=np.arange(len(n_simulations))
	#~ plt.plot(t,sains,c="green")
	#~ plt.hold(True)
	#~ plt.plot(t,infectes,c="blue")
	#~ plt.hold(True)
	#~ plt.plot(t,retires,c="yellow")
	#~ plt.hold(True)
	#~ plt.plot(t,morts,c="red")
	#~ plt.savefig('statistics',format='png') 
	#~ plt.show()




		
#initialisation(10,5,5,1,0.5,0.4,0.1)
#move()
#infection()
#update()
#stats()	
	
#~ ######Creation du client 
#~ # correction exercice client socket protocol TCP/IP
#~ 

stopLoop = True
host = sys.argv[1]
port = sys.argv[2]

# exemple de function pour traiter les arrets par ctrl+C
def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
	global stopBool
	
        sys.exit(0)
#

signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C pour arreter le client'
#creation de la socket puis connexion
try:

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,int(port)))

	while stopLoop:
  		msg = raw_input('>> ')
  		# envoi puis reception de la reponse
  		s.send(msg)
		if msg == "end":
			stopLoop = False
  		else: 
			data = s.recv(255) #la taille 
  			print data # on affiche la reponse

except socket.error, e:
    	print "erreur dans l'appel a une methode de la classe socket: %s" % e
    	sys.exit(1)
finally:
	# fermeture de la connexion
	print "finally ..."
	s.shutdown(1)#liberer l ensemble de la memoire associe socket
	s.close()
print "fin du client TCP"





