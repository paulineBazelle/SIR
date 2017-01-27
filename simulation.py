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
  
  def finPas(self):
    """Cette methode sera appelee a la fin d'un pas c'est-a-dire
    lorsqu'on a enchaine move, infect et update."""
    self.pas += 1
    self.move = True
    self.infect = False
    self.update = False
  
  def etape(self, chaine):
    return self.dico_etape[chaine]
