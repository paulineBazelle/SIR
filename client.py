import socket 
import select
import time
import sys
import signal

# correction exercice client socket protocol TCP/IP


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

while stopLoop:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,int(port)))

		while stopLoop:
			#msg = raw_input('>> ')
			f=open("donnees.txt","r")
			data=f.read()
			# envoi puis reception de la reponse
			s.send(data)
			#if msg == "end":
			#	stopLoop = False 
			f.close()
			data = s.recv(255) #la taille 
			fichier=open("client.txt","w")
			fichier.write(data)
			fichier.close()
			print data # on affiche la reponse
			
			stopLoop=False
			
	except socket.error, e:
			print "En attente, serveur deja connecte..."
			
	finally:
		# fermeture de la connexion
		print "finally ..."
		s.shutdown(1)#liberer l ensemble de la memoire associe socket
		s.close()
	print "fin du client TCP"

#site python.org 
