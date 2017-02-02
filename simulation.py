import numpy as np
import matplotlib.pyplot as plt

class Simulation:
  """L'objet simulation garde une trace de l'etape a laquelle on en est.
  """
  
  def __init__(self,ID,address):
    """ID est l'identifiant unique de la simulation. Il correspond a
    l'indice du tableau de simulations du serveur. Les booleens
    correspondant aux differentes etapes de simulation valent True
    lorsque l'etape doit etre realisee, False sinon. La variable 'pas'
    rend compte du pas courant. Le dictionnaire dico_etape permet de relier un
    mot cle a une fonction. Les listes S,I,R,M correspondent nombres d'agents
    dans chaque etat a chaque pas de temps. End et en_cours donne l'etat d'une 
    simulation. Si la simulation est termine, end est égal est vrai. Si la simulation
    est en cours, en_cours est egal est vrai. Address donne l'addresse IP
    du client qui a requete la simulation """
    self.ID = ID
    self.init = False
    self.move = True
    self.infect = False
    self.update = False
    self.stats = False
    self.pas = 0
    self.dico_etape = {'Move ' : self.move, 'Infect': self.infect,
    'Update' : self.update}
    self.S = []
    self.I = []
    self.R = []
    self.M = []
    self.end = False
    self.en_cours = False
    self.address = address
  
  def finPas(self):
    """Cette methode sera appelee a la fin d'un pas c'est-a-dire
    lorsqu'on a enchaine move, infect et update."""
    self.pas += 1
    self.move = True
    self.infect = False
    self.update = False
  
  def etape(self, chaine): 
    """Cette methode retourne la fonction associe au mot cle chaine"""
    return self.dico_etape[chaine]
  
