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

signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C pour arreter le client'
#creation de la socket puis connexion

#execute cette boucle tant qu'il n'a pas recu 'end' du serveur.
while stopLoop:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,int(port)))
		print "connectee"
		receptionFichier = False
	
		#execute cette boucle tant qu'il n'a pas recu 'end' du serveur.
		while stopLoop:
		  if receptionFichier:
			  data = s.recv(2048)
			  f=open('donnees.txt','w')
			  f.write(data)
			  f.close()
		  else:
			  msg = raw_input('>> ')
			  if msg == "end":
				  stopLoop = False
			  if msg =='Envoi':
				  receptionFichier = True
			  if msg == 'Pret':
				  f=open("donnees.txt","r")
				  data=f.read()
				  s.send(data)
				  f.close()
		
			
	except socket.error, e:
		print "En attente, serveur deja connecte...%s"%e
			
	finally:
		# fermeture de la connexion
		print "finally ..."
		s.shutdown(1)#liberer l ensemble de la memoire associe socket
		s.close()
	print "fin du client TCP"

#site python.org 
