import socket 
import select
import time
import sys
import signal
from agent import Agent
import random
import numpy as np
import errno
import matplotlib.pyplot as plt

# correction exercice client socket protocol TCP/IP

""" *********************** Methodes SIR ***********************"""
  
def initialisation(w, h,n, pr, pm, pi):
  """Creation d'une grille de taille w*h avec n-1 agents sains (etat=0)
  et 1 angent infecte (etat=1) dont les positions sont tirees aleatoirement.
  Creation du fichier de donnees avec les parametres de simulation, les
  positions des agents et leur etat qui sera transmis au serveur."""
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
  x=random.randint(0,w-1)
  y=random.randint(0,h-1)
  f.write(str(x) +" " + str(y) + " 1\n")
  f.close()
  

def move():
  """Deplacement aleatoire des agents dans la grille. Les nouvelles
  positions sont enregistrees dans le fichier donnees.txt"""
  f=open("donnees.txt","r")
  #Lit tout le fichier
  l=f.readlines()
  f.close()
  
  #Recupere la taille de la grille
  t=len(l[1])-1
  if t!=0:
    w=int(l[1][0:t])  #Enleve le caractere de retour a la ligne et transforme en entier
  else:
    w=int(l[1][0])
  t=len(l[2])-1
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
    if len(split) !=1:
      x=int(split[0].rstrip('\n'))
      y=int(split[1].rstrip('\n'))
      etat=int(split[2].rstrip('\n'))
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
  """Si plusieurs agents se trouvent a la meme position et qu'un des
  agents est infecte, les autres agents sont infectes avec un probabilite
  pi."""
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
    if len(line)> 1:
      x = int(line[0].rstrip('\n'))
      y = int(line[1].rstrip('\n'))
      etat = int(line[2].rstrip('\n'))
      agent = Agent(etat,x,y)
      grid[x][y].append(agent)

  #infection
  for i in range(w):
    for j in range(h):
      if grid[i][j]:
        #recherche s'il y a un agent infecte a cette position
        infected = False
        for agent in grid[i][j]:
          if agent.etat == 1:
            infected = True
            break
        if infected:
          #tirage de la probabilite et infection des agents
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
  #Ecrit les nouveaux etats des agents et leur position
  for i in range(w):
    for j in range(h):
      if grid[i][j]:
        for agent in grid[i][j]:
          f.write(str(agent.x) + " " + str(agent.y) + " " + str(agent.etat) + "\n")
  f.close()


#rappel : 0: sain , 1: infecte, 2: resistant, 3 :mort
def update():
  """Tire les probabilites pour le passage de l'etat infecte a resistant
  ou mort."""
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
    if len(line) >1: 
        x = int(line[0].rstrip('\n')) 
        y = int(line[1].rstrip('\n')) 
        etat = int(line[2].rstrip('\n')) 
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
  """Compte le nombre d'agents de chaque etat (sain, infecte, resistant,
  mort. Integre ces resultats dans le fichier donnees.txt"""
  #Lecture du fichier
  f=open("donnees.txt", "r")
  lines = f.readlines()
  for i in range(8):
    f.readline(9)
  f.close()
  f2=open("donnees.txt","w")
  for line in lines[:8]: 
    f2.write(line)
  f2.write('Stats\n') 
  n_s = 0
  n_i = 0
  n_r = 0
  n_m = 0
  for i in lines[9:]:
    if (len(i)>2):
      a=i.split()
      state = a[2]
      n_s,n_i,n_r,n_m = count(state,n_s,n_i,n_r,n_m)
  #output file
  f2.write("sains " + str(n_s) +' \n')
  f2.write("infectes " + str(n_i) +' \n')
  f2.write("retires " + str(n_r) +' \n')
  f2.write("morts " + str(n_m) +' \n')
  f2.writelines(lines[9:])
  f2.close()

def statsFinale():
  """Methode appelee a la fin de la simulation pour tracer l'evolution
  des populations de chacun des etats au cours du temps."""
  #Lecture du fichier
  f=open("donnees.txt","r")
  S=[]
  I=[]
  R=[]
  M=[]
  lines=f.readlines()
  ID=int(lines[0])
  for line in lines[9:]: 
    if len(line)>1:
      line=line.split()
      S.append(int(line[0]))
      I.append(int(line[1]))
      R.append(int(line[2]))
      M.append(int(line[3]))
  f.close()
  pas= len(S)
  t=np.arange(pas)
  #print ("Sains :", S)
  plt.plot(t,S,c="green")
  #plt.hold(True)
  plt.plot(t,I,c="blue")
  #plt.hold(True)
  plt.plot(t,R,c="orange")
  #plt.hold(True)
  plt.plot(t,M,c="red")
  plt.axis([0, pas, 0, (S[0]+I[0]+R[0]+M[0])])
  plt.title('Stats simulation %i'%ID)
  plt.savefig('statistics%i'%ID,format='png') 
  #plt.show()
  plt.close()
  

"""*************************** Client *****************************"""


# recuperation de l'adresse du serveur (host) et du port passes en
# arguments.
host = sys.argv[1]
port = sys.argv[2]

# booleen qui controle l'arret du programme
global stopLoopG
stopLoopG = True

# occupe = True si le client est en train de faire une etape elementaire
# (move, infect, update, stats). Reste True jusqu'a l'envoie du fichier
# au serveur.
occupe = False

# termine = True lorsque la simulation demandee par ce client est terminee.
global termine
termine=False

# Recuperation des parametres de simulation
if len(sys.argv) == 9:
  w, h,n, pr, pm, pi = sys.argv[3:]
  initialisation(int(w), int(h), int(n), float(pr), float(pm), float(pi))
  occupe = True

# Fonction pour traiter les arrets par ctrl+C
def signal_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  stopLoopG = False
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C pour arreter le client'

# Dictionnaire permettant d'associer le nom de l'etape lu dans le fichier
# donnees.txt a la fonction correspondante.
dic_func = {'Initialisation': move, 'Move' : infection,
'Infect' : update, 'Update': stats, 'Stats': move, 'FinalStats':statsFinale}

#execute cette boucle tant qu'il n'a pas recu 'end' du serveur.
while stopLoopG:
  stopLoop = True
  try:
    #connection au serveur
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,int(port)))
    print "connecte"
    # receptionFichier = True si le client s'apprete a recevoir un fichier
    receptionFichier = False
  
    #execute cette boucle tant qu'il n'a pas recu 'end' du serveur.
    while stopLoop:
      if receptionFichier:
        data = s.recv(2048)
        if (data== "end"):
          stopLoop = False
          receptionFichier = False 
        elif (data=="final"):
          print('Toutes les simulations sont terminees. Relancer le programme avec des nouveaux parametres')
          stopLoop = False
          stopLoopG = False
          termine=True
          
        else : 
          f=open('donnees.txt','w') #recuperation des donnees
          f.write(data)
          f.close()
          s.send('end') #deconnection du serveur
          occupe = True
          data = data.split('\n')
          func = dic_func[data[8]]
          func() #execution de la fonction elementaire
          receptionFichier = False 
      else:
        msg = s.recv(2048)
        if msg == "end": #deconnection demandee par le serveur
          stopLoop = False
        if msg =='Envoi': #demande d'envoi d'un fichier depuis le serveur
          s.send("Pret")
          receptionFichier = True
        if msg == 'Pret': #envoi des donnees au serveur
          f=open("donnees.txt","r")
          data=f.read() 
          s.send(data)
          f.close()
        if msg == 'Action':
          if occupe: #demande d'envoi des donnees au serveur
            s.send('Envoi')
            occupe = False
          else :
            s.send('Pret') # preparation a la reception des donnees
            receptionFichier = True
        if msg == 'final' :
          print('Toutes les simulations sont terminees. Relancer le programme avec des nouveaux parametres')
          stopLoop = False
          stopLoopG = False
          termine=True

          
  #except socket.error, e:
  except IOError, e:
    if e.errno == errno.EPIPE: 
      print ("epipe")
      s.close()
    elif e.errno == errno.ECONNRESET:
      print ("possible perte de donnees")
    else :
      raise
      
  finally:
    # fermeture de la connexion
    print "finally ..."
    s.send('end')
    s.shutdown(1)#liberer l ensemble de la memoire associe socket
    s.close()
    if (termine==True) :
      # si la simulation demandee est terminee, fin du programme.
      sys.exit(0)
  print "fin du client TCP"


