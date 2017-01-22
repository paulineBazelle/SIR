import socket
import select
from time import time, ctime
import sys
import signal
from simulation import Simulation

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
		# re coit les donnees d'un client et verifie qu il est toujours connecte 
		print "lecture"
		again = True
    receptionFichier = False
		while again:
      data = sockClient.recv(self.TAILLE_BLOC)
      if receptionFichier:
        print "recu : ",data
        fichier=open("serveur.txt","w")
				fichier.write(data)
				fichier.close()
      else:
        if data == 'Envoi':
          receptionFichier = True
        if data == 'Pret':
          f=open("serveur.txt","r")
          data=f.read()
          sockClient.send(data)
          f.close()
				if data == "end":
					print "fin de la connexion demandee par le client"
					again = False
		sockClient.shutdown(1)
		sockClient.close()


if __name__=="__main__":
	import sys
	if len(sys.argv)<2:
		print "usage : %s <port>" % (sys.argv[0],)
		sys.exit(-1)
	signal.signal(signal.SIGINT, signal_handler)
	Serveur()

