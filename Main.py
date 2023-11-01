


class Graphe :
    def __init__(self, noeuds : set, arcs : list[tuple[int,int,int]]) -> None:
        """_summary_

        Args:
            noeuds (set): _description_
            arcs (_type_): _description_
        """
        
        self.noeuds = noeuds
        self.arcs = {n : [a[1] for a in arcs if a[0] == n] for n in noeuds}
        self.poids = {n : [a[2] for a in arcs if a[0] == n] for n in noeuds}
    
    def __str__(self) -> str:
        return self.arcs
    def parcoursLargeur(self, s : int) -> list:
        """parcours d'un Graphe depuis un noeud s

        Args:
            s (int): noeud de départ
        """
        assert s in self.noeuds
        file = [s]
        parcours = [s]
        while len(file)!=0:
            n=file.pop(0)
            for i in self.arcs[n]:
                if i not in parcours:
                    parcours.append(i)
                    file.append(i)
        return parcours

    def parcoursProfondeur( self, s : int) -> list:
        """parcours d'un Graphe depuis un noeud s
        Args:
            s (int): noeud de départ
        """
        assert s in self.noeuds
        pile = [s]
        parcours = []
        while len(pile)!=0:
            n= pile.pop(-1)
            parcours.append(n)
            for i in self.arcs[n]:
                if i not in parcours:
                    pile.append(i)
            
        return parcours
    
    def géné_lateX(self):
        tex = "\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[pdf]{graphviz}\n\\usepackage[autosize]{dot2texi}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,arrows}\n\\begin{document}"
        tex += "\n\\begin{dot2tex}[neato,options=-tmath,scale=0.5]digraph grours {rankdir=LR;\n"
        for arc in self.arcs:
            for i in self.arcs[arc]:
                tex+=f"{arc} -> {i};"
        tex += "\n\\end{dot2tex}\n\end{document}"
        file = open("Latex/latex.tex", "w")
        file.write(tex)
        file.close()
        
    #Guille
    def contient_cycle(self):
        for noeud_depart in self.noeuds:
            pile = [noeud_depart]
            parcours = []
            while len(pile)!=0:
                n = pile.pop(0)
                parcours.append(n)
                for i in self.arcs[n]:
                    if i not in parcours:
                        pile.append(i)
                    else:
                        return True
        return False

                   
#a voir si utile
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


  
  
#Ben
import csv

def to_csv(name_csv_file: str, fieldnames:list[str], rows:list[list[str]]) -> None:
    """
    Args:
        namecsvfile (str) : nom du fichier csv (sanssuffixe) 
        fieldnames(list[str]): liste des noms de champs 
        rows(list[list[str]]): liste des lignes (liste de colonnes)
    """
    with open(name_csv_file + ".csv" ,'w', encoding="utf-8") as csvfile:
        csvwriter=csv.writer(csvfile,delimiter=',')
        csvwriter.writerow(fieldnames)
        for r in rows:
            csvwriter.writerow(r)
    
    
def csv_to_Graphe(nom_fichier:str) -> Graphe:  
    """J'ai repris exactement ton code,
    t'avais une condition qui ne servais a rien dans couple (if len(s[3]==1)) car elle est bien traitée dans le split
    j'ai enlevé la condition du OG, car sinon il auriat fallu le mettre dans le manuel d'utilisation, c'est pas fou
    Args:
        nom_fichier (str): nom fichier à convertir

    Returns:
        Graphe: Graphe issu du fichier.
    """
    with open(nom_fichier+'.csv','r',encoding='utf8') as file:
        noeud=set()
        arcs=[]
        for ligne in file:
            s=ligne.split(',')
            noeud = noeud  | {s[0]}
            arcs += couple(s)
        return Graphe(noeud,arcs)
              
def couple(s:list)->tuple:
    """retourne tout les arcs possibles relatif à une certaine tâche sous la forme de tuple(precedents,arrivée,durée)
    Args:
        s (list): éléments de la ligne sous fortme de liste

    Returns:
        tuple: retourne les arcs du noeuds de la i-ème ligne
    """
    s2=list()
    if len(s)>=4:
        precedents=s[3].split()
        for i in range(len(precedents)):
            s2.append((precedents[i],s[0],s[2]))
        return s2

def Dijkstra(g : Graphe, s : int, w : dict[tuple[int,int],int]):
    assert s in g.noeuds
    pred = {n : None for n in g.noeuds}
    dict_dist_source = {n : 0 if n==0 else 99999 for n in g.noeuds}
    D = g.noeuds
    while D != set():
        new_dict = {k : dict_dist_source[k] for k in in D}
        source_courante = min(new_dict, key=new_dict.get)
        D = D - {source_courante}
        for n_dist in g.adj[source_courante]:
            if dict_dist_source[n_dist]> dict_dist_source[source_courante]+ w[source_courante, n_dist]:
                dict_dist_source[n_dist] = dict_dist_source[source_courante] + w[source_courante, n_dist]
                pred[n_dist] = source_courante
    return (pred,dict_dist_source)




def main():
    #grCours = Graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})
   
    
    to_csv("Graphe2",["Identificateur","Description","Durée","Précédente(s)","S0","S1","S2"],
        [["PM","Permis de construire ",'60'],
         ["F","Fondations",'7',"PC"],
         ["GE1","Passage des gaines et évacuations ","3","F"],
         ["DRC","Dalle rez de chaussée","7","GE1"],
         ["MP","Murs porteurs ","14","DRC"],
         ["DP","Dalles plafond ","7","MP"],
        ["GE2","Passage gaines et évacuation","3","DP"],
        ["T","Toiture","14","GE2"],
        ["FE","Fenêtres","7","T"],
        ["PE","Portes extèrieures","3","T C"],
        ["IE","Installation électrique et évacuation","3","GE2"],
        ["C","Chape","7","DP"],
        ["C1","Carrelage du sol","7","C"],
        ["P","Parquets","7","C"],
        ["CM","Cloisons et menuiserie intérieure","10","FE C1 P FC"],
        ["FC","Finition des cloisons","7","CM"],
        ["IC","Implantation de la cuisine ","7","FC"],
        ["IW","Implantation des wc","3","FC"],
        ["IS","Implantation des salles de bain","7","FC"],
        ["PP","Peinture des plafonds ","7","IC IW IS"],
        ["PM","Peinture des murs","7","PP"],
        ["S","Serrurerie","3","P CM"],
        ["R1","Revêtement des sols (moquettes) ","2","C S"],
        ["R","Réception de la maison ","0.5","MP S"]]) 
    
    grph = csv_to_Graphe("Graphe")
    print(grph.noeuds)
    print(grph.arcs)
    grph.géné_lateX()
    print(Dijkstra(grph,"PM",))
    
    
    
if __name__ == "__main__":
    main()


