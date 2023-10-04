class Graphe:
    def __init__(self, noeuds : set [int] , arcs : set [tuple [int , int ]] ) -> None:
        self.noeuds = noeuds
        self.adj = { n : [a[1] for a in arcs if a[0] == n] for n in noeuds }
        self.prec = { n : [a[0] for a in arcs if a[1] == n] for n in noeuds }

    def contient_cycle(self):
        """
        Détecte la présence d'éventuels cycles dans le graphe
        :return: un booléen (vrai si le graphe contient un cycle, faux sinon) 
        """
        T=[]
        for noeud1 in T:
            for noeud2 in T:
                if arc_present(self,noeud1,noeud2):
                    T.append([noeud1,noeud2])
        for b in range(10):
            for i in range(len(T)):
                for j in range(len(T)):
                    if T[i][-1]==T[j][0]:
                        T[i].append(T[j][-1])
                        T[j]=0
        return T

                   
    
def arc_present(g, noeud1, noeud2):
  """
  Indique s'il existe un arc entre deux points
  :param neoud1 et noeud2: noeuds entre lesquels on veut savoir s'il existe un arc
  :return: un booléen (vrai s'il existe un arc entre les deux points, faux sinon)
  """
  depart = noeud1
  arrivee = noeud2
  file = []
  visites = {element: False for element in g.noeuds}
  file.append(depart)

  while file:
    actuel = file.pop(0)
    visites[actuel] = True
    for noeud in g.noeuds:
      if noeud in g.adj[actuel] and visites[noeud] == False:
        file.append(noeud)
        visites[noeud] = True
        if noeud == arrivee:
          return True
  return False