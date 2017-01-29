import socket
import select
from time import time, ctime
import sys
import signal
from simulation import Simulation
import errno

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
    self.en_cours=False
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
	

  def lit(self,sockClient):
    # recoit les donnees d'un client et verifie qu il est toujours connecte 
    print "lecture"
    print("en_cours",self.en_cours)
    again = True
    receptionFichier = False
    sockClient.send('Action')
    while again:
      try:
        data = sockClient.recv(self.TAILLE_BLOC)
        #print('recu : %s' %data)
        if receptionFichier:
          self.en_cours=False
          print "Telechargement fichier: ",data
          print "Longueur", len(data)
          sockClient.send('end')
          fichier=open("serveur.txt","w")
          data = data.split('\n')
          if data[0] == 'Create':
            data[0] = str(len(self.simulations))
            simul = Simulation(len(self.simulations))
            self.simulations.append(simul)
          else:
            simul_courante = self.simulations[int(data[0])]
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
            if not(self.en_cours) :
              print("Envoi d'un fichier")
              f=open("serveur.txt","r")
              data=f.read()
              print("data :",data)
              sockClient.send(data)
              f.close()
              sockClient.send('end')
              self.en_cours=True
            else :
              sockClient.send('end')
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

