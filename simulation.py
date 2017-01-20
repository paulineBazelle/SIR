class Simulation:
  """L'objet simulation garde une trace de l'etape a laquelle on en est.
  """
  
  def __init__(self,ID):
    """ID est l'identifiant unique de la simulation. Il correspond a
    l'indice du tableau de simulations du serveur. Les booleens
    correspondant aux differentes etapes de simulation valent True
    lorsque l'etape a ete realisee, False sinon. La variable 'pas'
    rend compte du pas courant."""
    self.ID = ID
    self.init = True
    self.move = False
    self.infect = False
    self.update = False
    self.stats = False
    self.pas = 0
  
  def finPas(self):
    """Cette methode sera appelee a la fin d'un pas c'est-a-dire
    lorsqu'on a enchaine move, infect et update."""
    self.pas += 1
    self.move = False
    self.infect = False
    self.update = False
