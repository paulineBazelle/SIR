# -*- coding: utf-8 -*-

import socket
import select
from time import time, ctime
import sys
import signal
from simulation import Simulation
import errno
import random

stopBoolServ = True

#exemple de function pour traiter les arrets par ctrl+C
def signal_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  global stopBoolServ 
  stopBoolServ = False
  sys.exit(0)

class Serveur:
  def __init__(self):
    global stopBoolServ
    stopBoolServ = True
    # Initialisation de la classe """
    self.TAILLE_BLOC=2048 # la taille des blocs
    self.simulations = [] #tableau d'objets simulations
    self.nbPas = 100 #Nombre de pas effectue dans une simulation
    self.client={} #Dictionnaire qui associe l'adresse d'un client avec le numero
    #de sa simulation
    # creation de la connection pour le serveur, protocol TCP, domaine internet
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # recuperation du numero de port via la ligne de commande
    sock.bind(('',int(sys.argv[1])))
    sock.listen(5)
    
    # en attente qu'un client se connecte
    while stopBoolServ:
      newsock, addr = sock.accept()
      address=addr[0]
      print "Connection entrante : %s" % address
      # on lit ce que la socket a ecrit
      self.lit(newsock, address)
      
      
    print "arret de la boucle accept, en attente de connexion ..."
    sock.shutdown(1)
    sock.close()
  
  #Definition d'une fonction qui determine si toutes les simulations sont termines
  #Si c'est le cas pas_fini=False
  #A l'inverse si une simulation n'est pas finie pas_fini=True
  def not_ended(self):
    pas_fini=False
    for i in range(len(self.simulations)):
      if self.simulations[i].end==False:
        pas_fini=True
        break
    return pas_fini
      
  #Definition d'une fonction qui determine si une simulation est en cours ou non
  #Si toutes les simulations sont en cours, en_cours=True
  #Si une simulation n'est pas en cours, en_cours=False
  def libre(self):
    pas_en_cours=-1
    for i in range(len(self.simulations)):
      if self.simulations[i].en_cours==False and self.simulations[i].end==False:
        pas_en_cours=i
        break
    return pas_en_cours
	

  def lit(self,sockClient,address):
    # recoit les donnees d'un client et verifie qu il est toujours connecte 
    again = True
    receptionFichier = False
    #Verifie si une simulation est terminee
    if (address in self.client.keys()):
      if (self.simulations[self.client[address]].end==True):
        sockClient.send('Action') #La simulation est termine, on entre en contact
        #avec le client qui la demande
        data=sockClient.recv(self.TAILLE_BLOC)
        if data=='Pret': #Si le client n'est pas occupe
          r=self.client[address] #recupere l'identifiant de la simulation
          f=open("%i.txt"%r,"r") #ouvre le fichier associe à la simulation
          data=f.read() #Lit le contenu du fichier et l'envoi au client
          sockClient.send(data)
          f.close()
          sockClient.send('final') #Envoi le signal pour que fermer la connection
          #avec le client
      else: #Si la simulation n'est pas fini on envoi action au serveur
        sockClient.send('Action')
    else:
      sockClient.send('Action')
      
    #Tant que again est True on reste dans la boucle. Again devient faux lorsque
    #l'un des partie demande de stopper la connexion
    while again:
      try:
        data = sockClient.recv(self.TAILLE_BLOC)
        #On rentre dans la condition si le client envoit un fichier
        if receptionFichier:
          sockClient.send('end')
          data = data.split('\n')
          if data[0] == 'Create': #Si la premiere ligne des donnees envoye par le
            #client est Create alors on initialise la simulation
            data[0] = str(len(self.simulations)) #On recupere l'identifiant de la simulation 
            simul = Simulation(len(self.simulations), address) #on cree un nouvel objet simul
            #de la classe simulation
            self.simulations.append(simul) #On ajoute cette nouvelle simulation 
            #dans la liste simulations
            self.client[address]= simul.ID #On ajoute l'identifiant à l'adresse IP dans le 
            #dictionnaire client
            fichier=open("%s.txt"%(data[0]),"w") #On ouvre le fichier associe à la simulation
          #Si la simulation a deja ete cree on rentre dans cette condition
          else:
            simul_courante = self.simulations[int(data[0])] #On recupere la simulation courante
            simul_courante.en_cours=False 
            fichier=open("%s.txt"%(data[0]),"w") #On ouvre le fichier associe à la simulation
            etape = data[8] #On recupere l'etape : Move, Infect, Update ou Stats
            #On test dans quel etape on se trouve et on modifie les valeurs des 
            #booleen qui sont associes
            #Par exemple si l'on est a l'etape move alors on passe move a False car
            #l'etape et fini et on passe infect a True car c'est l'etape a faire
            if etape == 'Move':                    
              simul_courante.infect = True
              simul_courante.move = False
            if etape == 'Infect':
              simul_courante.infect = False
              simul_courante.update = True
            if etape == 'Update':
              simul_courante.update = False
              simul_courante.stats = True
            if etape == 'Stats':
              simul_courante.stats = False
              pas = int(data[7])
              #On regarde si le pas courant correspond au pas final de la simulation
              if pas == self.nbPas:
                data[8]='FinalStats\n' #On ecrit l'etape dans le fichier
                del data[9:]
                for i in range(len(simul_courante.S)): #On ecrit les etats des differents agents
                  data.append('%i %i %i %i'%(simul_courante.S[i],simul_courante.I[i],simul_courante.R[i],simul_courante.M[i]))
                simul_courante.end=True #La simulation courante est termine on passe end a True
              #Si le nombre de pas est inferieur au nombre de pas final
              if pas < self.nbPas: 
                simul_courante.finPas() #On incremente le pas de 1
                data[7] = str(pas + 1)
                agents = []
                for line in data[9:13]: #On recupere les etats des agents a partir des donnes du fichier
                  agents.append(int(line.split()[1]))
                simul_courante.S.append(agents[0])
                simul_courante.I.append(agents[1])
                simul_courante.R.append(agents[2])
                simul_courante.M.append(agents[3])
                del data[9:13]
          for line in data: #Quelque soit l'etape on reecrit les donnees dans le fichier
            fichier.write(line + '\n')
          fichier.close()
          receptionFichier = False
        #Si le client n'envoit pas de fichier mais un mot cle
        else:
          if data == 'Envoi': #Si le mot cle est Envoi alors le client vas envoyer un fichier
            receptionFichier = True
            sockClient.send('Pret')
          if data == 'Pret': #Si le mot cle est Pret alors le client attend que lui envoit
            #un travail
            if self.not_ended(): #Si il reste des simulations qui ne sont pas terminees, on lui
              #en envoit un nouveau calcul a faire
              r=self.libre()
              if r!=-1: #Si des simulations ne sont pas en cours alors on envoit les donnees au client
                f=open("%i.txt"%r,"r")
                data=f.read()
                print("data :",data)
                sockClient.send(data)
                f.close()
                sockClient.send('end')
                self.simulations[r].en_cours=True
              else :  #si aucune simulation n'est libre on envoit end au client qui se reconnectera
                #plus tard
                sockClient.send('end')
            else: #Si toutes les simulations sont fini alors on envoi le signal de terminaison
              #connection au client
              print("Toutes les simulations sont terminees")
              sockClient.send('final')
          if data == "end": #Si le mot cle est end, le client demande la fin de la connexion
            again = False
    
      
      except IOError,e:
        if e.errno == errno.ECONNRESET:
          print('possible perte de donnees...')
					
    #On ferme la connexion avec le client
    sockClient.shutdown(1)
    sockClient.close()
    connected = False
    

if __name__=="__main__":
  import sys
  if len(sys.argv)<2:
    print "usage : %s <port>" % (sys.argv[0],)
    sys.exit(-1)
  signal.signal(signal.SIGINT, signal_handler)
Serveur()
