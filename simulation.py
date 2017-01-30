import numpy as np
import matplotlib.pyplot as plt

class Simulation:
  """L'objet simulation garde une trace de l'etape a laquelle on en est.
  """
  
  def __init__(self,ID):
    """ID est l'identifiant unique de la simulation. Il correspond a
    l'indice du tableau de simulations du serveur. Les booleens
    correspondant aux differentes etapes de simulation valent True
    lorsque l'etape doit etre realisee, False sinon. La variable 'pas'
    rend compte du pas courant."""
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
  
  def finPas(self):
    """Cette methode sera appelee a la fin d'un pas c'est-a-dire
    lorsqu'on a enchaine move, infect et update."""
    self.pas += 1
    self.move = True
    self.infect = False
    self.update = False
  
  def etape(self, chaine):
    return self.dico_etape[chaine]
  
  def statsFinale(self):
    t=np.arange(self.pas)
    print ("Sains :", self.S)
    plt.plot(t,self.S,c="green")
    #plt.hold(True)
    plt.plot(t,self.I,c="blue")
    #plt.hold(True)
    plt.plot(t,self.R,c="orange")
    #plt.hold(True)
    plt.plot(t,self.M,c="red")
    plt.axis([0, self.pas, 0, (self.S[0]+self.I[0]+self.R[0]+self.M[0])])
    plt.title('Stats simulation %i'%self.ID)
    plt.savefig('statistics%i'%self.ID,format='png') 
    plt.show()
  
