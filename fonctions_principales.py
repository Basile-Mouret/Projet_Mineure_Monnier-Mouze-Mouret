from __future__ import annotations
import ast


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
      liste = []
      for noeud1 in self.noeuds:
          for noeud2 in self.noeuds:
              if arc_present(self,noeud1,noeud2) and arc_present(self,noeud2,noeud1):
                  liste.append([noeud1,noeud2])
                  return [True, liste]
      return [False]
  
    def tous_chemins(self, depart, arrivee, visites, chemin, liste):
      """
      Renvoie une liste de tous les chemins entre un point de départ et un point d'arrivée
      """
      visites[depart]= True
      chemin.append(depart)

      if depart == arrivee:
          liste.append(chemin.copy())
      else:
        for i in self.adj[depart]:
            if visites[i]== False:
              self.tous_chemins(i, arrivee, visites, chemin, liste)
                    
      chemin.pop()
      visites[depart] = False

      return liste

    def Afficher_tous_chemins(self, s, arrivee):
      """
      Permet d'appeler la fonction tous_chemins sans avoir à renseigner les paramètres par            défaut 
      """
      f = self.tous_chemins(s, arrivee, {element: False for element in self.noeuds}, [], [])
      return f
    


def lire_taches(fichier):
  """
  Renvoie une liste contenant les informations sur chaque tâche renseignée dans le fichier 
  tâches
  :param fichier: fichier contenant les tâches
  :return: une liste de listes contenant les identifiants, les durées et les descriptions de      chaque tâche
  """
  with open(str(fichier), encoding = 'utf8') as fichier:
    liste_ensemble_lignes = []
    for ligne in fichier:
        liste_une_ligne = []
        string = ""
        for caractere in ligne:
          if caractere == "_":
            string = string.strip()
            liste_une_ligne.append(string)
            string = ""
          else:
            string += caractere
        string = string.strip()
        liste_une_ligne.append(string)  
        liste_ensemble_lignes.append(liste_une_ligne)
    return(liste_ensemble_lignes)


def lire_liaisons(fichier_liaisons):
  """
  Renvoie un ensemble de doublets contenant chaque tâche et la tâche qui la suit dans l'ordre 
  chronologique
  :param fichier_liaisons: le fichier contenant les liaisons entre chaque tâche
  :return: un ensemble de doublets de la forme ('point de départ', 'point d'arrivée')
  """
  with open(str(fichier_liaisons), encoding = 'utf8') as fichier:
    ensemble_couple = set()
    for ligne in fichier:
      string = ""
      for caractere in ligne:
        if caractere == "<":
          string = string.strip()
          depart = string
          string = ""
        elif caractere == ",":
          ensemble_couple.add((depart,string.strip())) 
          string, depart = "",""
        else:
          string += caractere  
    return ensemble_couple

def duree_taches(fichier_taches):
  """
  Renvoie un dictionnaire qui associe à chaque tâche sa durée
  :param fichier: le fichier contenant les tâches du projet
  :return: le dictionnaire
  """
  liste = lire_taches(fichier_taches)
  dicotache = {}
  for tache in liste:
    dicotache.update({str(tache[0]) :(tache[1])})     
  return dicotache

def description_taches(fichier_taches):
  """
  Renvoie un dictionnaire qui associe à chaque tâche sa description
  :param fichier: le fichier contenant les tâches du projet
  :return: le dictionnaire
  """
  liste = lire_taches(fichier_taches)
  dicotache = {}
  for tache in liste:
    dicotache.update({str(tache[0]) : (tache[2])})
  return dicotache

def generer_graphe(fichier_taches, fichier_liaisons):
  """
  Génère un objet de la classe Graphe associé au système de tâches contenu dans les fichiers fournis
  :param fichier_taches: fichier contenant les informations relatives aux tâches du projet
  :param fichier_liaisons: le fichier contenant les liaisons entre chaque tâche
  :return: le graphe
  """
  liste_tache = lire_taches(fichier_taches)
  ensemble_noms = {n[0] for n in liste_tache}
  ensemble_liaisons = lire_liaisons(fichier_liaisons)
  graphe = Graphe(ensemble_noms, ensemble_liaisons)
  return graphe

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

def parcoursProfondeur (g, s, explores = set(), parcours = []) :
    """
    Renvoie le parcours en profondeur d'un graphe
    :param g: graphe dont on veut le parcours
    :param s: noeud par lequel le parcours commence
    :return: Le parcours sous forme d'une liste contenant les noeuds dans l'ordre
    """
    explores.add(s)
    for i in g.adj[s] :
        if i not in explores:
            parcoursProfondeur(g,i,explores,parcours)
    parcours.insert(0,s)
    return parcours

def chemin_critique(g, debut, fin, fichier_taches):
  """
  Renvoie tous les chemins critiques du graphe, c'est-à-dire les chemins les plus longs entre deux      noeuds, et leur durée
  :param g: le graphe
  :param debut: le noeud de départ
  :param fin: le noeud d'arrivée
  :param fichier_taches: le fichier contenant les informations relatives aux tâches du projet
  :return: un doublet avec comme premier élément une liste contenant les chemins critiques sous forme 
  de listes et comme deuxième élément la durée de ces chemins critiques
  """
  dicosommes = {}
  dicotache = duree_taches(fichier_taches)
  tous_chemins = g.Afficher_tous_chemins(debut,fin)
  for chemin in tous_chemins:
    somme = 0
    for noeud in chemin:
      somme += int(dicotache[noeud])
    dicosommes.update({str(chemin) : somme})
    temps_max = max(dicosommes.values())
  critique = [key for key, value in dicosommes.items() if value == temps_max]
  return (critique,temps_max)
  
def triTopologique(g):
    """
    Renvoie le tri topologique du graphe, c'est-à-dire tous les noeuds du graphe triés du début à la 
    fin, par niveaux
    :param g: le graphe dont on veut le tri
    :return: le tri topologique du graphe, sous forme de liste
    """
    explores = set()
    parcours = []
    for s in g.noeuds:
        if s not in explores:
            parcoursProfondeur(g, s, explores, parcours)
    return parcours

def dates_au_plus_tot(g, fichier_taches):
  """
  Calcule la date de départ possible au plus tôt pour chaque tâche
  :param g: le graphe associé au projet
  :param fichier_taches: le fichier contenant les informations relatives aux tâches du projet
  :return: un dictionnaire qui associe à chaque tâche sa date de début au plus tôt
  """
  dicotache = duree_taches(fichier_taches)
  dicodates = {}
  for noeud in g.noeuds:
    dicodates[noeud] = 0
    liste_noeuds = triTopologique(g)
  for noeud in liste_noeuds:
    for noeud_adj in g.adj[noeud]:
      if dicodates[noeud] + int(dicotache[noeud]) > dicodates[noeud_adj]:
        dicodates[noeud_adj] = dicodates[noeud] + int(dicotache[noeud])
  return dicodates

def dates_au_plus_tard(g, debut, fin, fichier_taches):
  """
  Calcule la date de départ au plus tard pour chaque tâche sous peine de ralentir le projet entier
  :param g: le graphe associé au projet
  :param fichier_taches: le fichier contenant les informations relatives aux tâches du projet
  :return: un dictionnaire qui associe à chaque tâche sa date de début au plus tard
  """
  dicotache = duree_taches(fichier_taches)
  dicodates = {}
  date_fin_projet = chemin_critique(g, debut, fin, fichier_taches)[1] 
  for noeud in g.noeuds:
    dicodates[noeud] = date_fin_projet
    liste_noeuds = triTopologique(g)
    liste_noeuds.reverse()
  for noeud in liste_noeuds:
    for noeud_prec in g.prec[noeud]:
      if dicodates[noeud_prec] > dicodates[noeud] - int(dicotache[noeud_prec]):
        dicodates[noeud_prec] = dicodates[noeud] - int(dicotache[noeud_prec]) 
  return dicodates
  