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
    self.nbPas = 100
    # creation de la connection pour le serveur, protocol TCP, domaine internet
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # recuperation du numero de port via la ligne de commande
    sock.bind(('',int(sys.argv[1])))
    sock.listen(5)
    
    # en attente qu'un client se connecte
    while stopBoolServ:
      newsock, addr = sock.accept()
      print "connection entrante : %s:%d" % addr
      # on lit ce que la socket a ecrit
      self.lit(newsock)
      
      
    print "arret de la boucle accept, en attente de connexion ..."
    sock.shutdown(1)
    sock.close()
  
  def not_ended(self):
    pas_fini=False
    for i in range(len(self.simulations)):
      if self.simulations[i].end==False:
        pas_fini=True
        break
    return pas_fini
      
      
  def libre(self):
    pas_en_cours=-1
    for i in range(len(self.simulations)):
      if self.simulations[i].en_cours==False and self.simulations[i].end==False:
        pas_en_cours=i
        break
    return pas_en_cours
	

  def lit(self,sockClient):
    # recoit les donnees d'un client et verifie qu il est toujours connecte 
    print "lecture"
    again = True
    receptionFichier = False
    sockClient.send('Action')
    while again:
      try:
        data = sockClient.recv(self.TAILLE_BLOC)
        #print('recu : %s' %data)
        if receptionFichier:
          print "Telechargement fichier: ",data
          print "Longueur", len(data)
          sockClient.send('end')
          data = data.split('\n')
          if data[0] == 'Create':
            data[0] = str(len(self.simulations))
            simul = Simulation(len(self.simulations))
            self.simulations.append(simul)
            fichier=open("%s.txt"%(data[0]),"w")
          else:
            simul_courante = self.simulations[int(data[0])]
            simul_courante.en_cours=False
            fichier=open("%s.txt"%(data[0]),"w")
            etape = data[8]
            if etape == 'Move':
              print('end move')
              simul_courante.infect = True
              simul_courante.move = False
            if etape == 'Infect':
              print('end infect')
              simul_courante.infect = False
              simul_courante.update = True
            if etape == 'Update':
              print('end update')
              simul_courante.update = False
              simul_courante.stats = True
            if etape == 'Stats':
              print('end stats')
              simul_courante.stats = False
              pas = int(data[7])
              if pas == self.nbPas:
                simul_courante.statsFinale()
                simul_courante.end=True
              if pas < self.nbPas:
                print('end pas %i' %pas)
                simul_courante.finPas()
                data[7] = str(pas + 1)
                agents = []
                for line in data[9:13]:
                  agents.append(int(line.split()[1]))
                simul_courante.S.append(agents[0])
                simul_courante.I.append(agents[1])
                simul_courante.R.append(agents[2])
                simul_courante.M.append(agents[3])
                del data[9:13]
          for line in data:
            fichier.write(line + '\n')
          #fichier.writelines(data)
          fichier.close()
          receptionFichier = False
        else:
          if data == 'Envoi':
            print("Reception d'un fichier")
            receptionFichier = True
            sockClient.send('Pret')
          if data == 'Pret':
            if self.not_ended():
              print("Envoi d'un fichier")
              r=self.libre()
              if r!=-1:
                f=open("%i.txt"%r,"r")
                data=f.read()
                print("data :",data)
                sockClient.send(data)
                f.close()
                sockClient.send('end')
                self.simulations[r].en_cours=True
              else :
                sockClient.send('end')
            else:
              print "Fin de toutes les simulations"
              sockClient.send('final')
          if data == "end":
            print "fin de la connexion demandee par le client"
            again = False
      
      except IOError,e:
        if e.errno == errno.ECONNRESET:
          print('possible perte de donnees...')
					
    print('fin de la communication')
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
