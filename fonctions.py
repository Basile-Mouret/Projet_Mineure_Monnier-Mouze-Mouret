import math
import csv


class Graphe :
    def __init__(self, noeuds : set, arcs : list[tuple[int,int]],poids :dict[str : int]) -> None:
        """rajouter les descriptions

        Args:
            noeuds (set): _description_
            arcs (_type_): _description_
        """
        
        self.noeuds = noeuds
        self.adj = {n : [a[1] for a in arcs if a[0] == n] for n in noeuds}
        self.poids = poids
    
    def __str__(self) -> str:
        return self.adj
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
            for i in self.adj[n]:
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
            for i in self.adj[n]:
                if i not in parcours:
                    pile.append(i)
            
        return parcours
    
    def géné_lateX(self):
        tex = "\n\\begin{dot2tex}[neato,options=-tmath,scale=0.5]digraph grours {rankdir=LR;\n"
        for arc in self.adj:
            for i in self.adj[arc]:
                tex+=f"{arc} -> {i};"
        tex += "}\n\\end{dot2tex}"
        return tex
    
    def dessiner_graphe(self):
        tex = "\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[pdf]{graphviz}\n\\usepackage[autosize]{dot2texi}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,arrows}\n\\begin{document}"
        #si on veut écrire le latex dans un fichier dédié
        tex+= self.géné_lateX()
        tex+="\n\end{document}"
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
                for i in self.adj[n]:
                    if i not in parcours:
                        pile.append(i)
                    elif i == noeud_depart:
                        return True
        return False

#Ben

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
    """
    Creer et renvois le graphe associé à un fichier csv.
    Args:
        nom_fichier (str): nom fichier à convertir

    Returns:
        Graphe: Graphe issu du fichier.
    """
    Dict_poids={}
    with open(nom_fichier+'.csv','r',encoding='utf8') as file:
        noeud=set()
        arcs=[]
        for ligne in file:
            s=ligne.split(',')
            noeud = noeud  | {s[0]}
            Dict_poids[s[0]] = float(s[2])
            if len(s)>3:
                #cple=couple(s)
                #arcs += cple[0]
                #Dict_poids[cple[1]]=cple[2]
                arcs += couple(s)
        return Graphe(noeud,arcs,Dict_poids)

def couple(s:list)->tuple:
    """retourne tout les arcs possibles relatif à une certaine tâche sous la forme de tuple(precedents,arrivée,durée)
    Args:
        s (list): éléments de la ligne sous fortme de liste

    Returns:
        tuple: retourne les arcs du noeuds de la i-ème ligne
    """
    arcs=[]
    if s[3]=='Précédente(s)' :
        #return [[],'Tâche','Poids']
        return []
    else:
        precedents=s[3].split()
        for i in range(len(precedents)):
            arcs.append((precedents[i],s[0]))
        #return [arcs,s[0],s[2]]
        return arcs

def Dijkstra(g : Graphe, n_départ : str,  poids : dict[tuple[int,int],int], neg = False):
    assert n_départ in g.noeuds
    pred = {n : None for n in g.noeuds}#dictionnaire des prédécesseur du noeud dans le chemin le plus rapide jusqu'à l'origine
    dict_dist_source = {n : 0 if n==n_départ else math.inf for n in g.noeuds}#dictionnaire des distance depuis la source
    noeuds_restants = g.noeuds#noueds qui n'ont pas encore été parcourus
    while noeuds_restants != set():#tant que tout les noeuds n'ont pas été parcourus
        new_dict = {k : dict_dist_source[k] for k in noeuds_restants}#dictionnaire des distance ne contenant que les noeuds non parcourus
        source_courante = min(new_dict, key=new_dict.get)#le prochain noeuds a être analysé est le plus proche des noeuds qui n'a pas été parcourus
        noeuds_restants = noeuds_restants - {source_courante}#on l'enleve des noeuds restants
        for n_dist in g.adj[source_courante]:#pour chaque arcs depuis la source courante
            if dict_dist_source[n_dist]> dict_dist_source[source_courante] + ((-1)**neg )* poids[source_courante]:#si le chemin par la source courante est plus rapide, choisir celui ci
                dict_dist_source[n_dist] = dict_dist_source[source_courante] + ((-1)**neg )* poids[source_courante]
                pred[n_dist] = source_courante
    return (pred,dict_dist_source)#on retourne la liste des prédécesseur et des durées minimales avant le commancement d'une tâche
def Bellman_Ford(g : Graphe, n_départ : str,  poids : dict[tuple[int,int],int], neg = False):
    dico_pred = {n : None for n in g.noeuds}#dictionnaire des prédécesseur du noeud dans le chemin le plus rapide jusqu'à l'origine
    dico_dist_source = {n : 0 if n==n_départ else math.inf for n in g.noeuds}#dictionnaire des distance depuis la source
    for _ in range(len(g.noeuds)-1):
        for u in g.noeuds:
            for v in g.adj[u]:
                if dico_dist_source[u] - g.poids[u]< dico_dist_source[v]:
                    dico_dist_source[v] = dico_dist_source[u]- g.poids[u]
                    dico_pred[v] = u
    
    return dico_dist_source,dico_pred
def chemins_critique(graphe):
    dico_pred,dico_duree = Bellman_Ford(graphe,"PC",graphe.poids,neg = True)
    for tache in dico_duree.keys():
        dico_duree[tache] *= -1
        
        
    noeuds_critiques = set()
    noeuds_critiques.add(max(dico_duree,key = dico_duree.get))
    for n_dep in graphe.adj.keys():
        for n_arr in graphe.adj[n_dep]:
            if dico_duree[n_arr]-dico_duree[n_dep] == graphe.poids[n_dep]:
                noeuds_critiques.add(n_dep)
    return noeuds_critiques

def parents(graphe):
    """retrouve les noeuds parents de chaque noeud
    Returns:
        dict[noeud:set] : dictionnaire contenant le noeud en indice et son/ces parents
    """
    dico_parents = {n : set() for n in graphe.noeuds}
    for n_d in graphe.noeuds:
        for n_f in graphe.adj[n_d]:
            dico_parents[n_f].add(n_d)
    return dico_parents





def forward_pass(graphe) :
    
    #forward pass
    
    debut_tot = {n : -1 for n in graphe.noeuds}#date de départ minimum
    fin_tot = {n : -1 for n in graphe.noeuds}#date de fin minimum
    par = parents(graphe)
    noeuds_départ  = {n for n in graphe.noeuds if par[n] == set()}
    file = []
    for n in noeuds_départ:
        debut_tot[n] = 0
        fin_tot[n] = graphe.poids[n]#date de départ minimale
        file += graphe.adj[n]
    
    while len(file)>0:
        n = file.pop(0)
        parents_parcourus = True
        for n_parent in par[n]:
            if fin_tot[n_parent]<0: parents_parcourus = False
        
        if parents_parcourus:
            file += graphe.adj[n]
            for n_parent in par[n]:
                if fin_tot[n_parent]>debut_tot[n]:
                    debut_tot[n] = fin_tot[n_parent]
                    fin_tot[n] = fin_tot[n_parent]+graphe.poids[n]
    return debut_tot,fin_tot    
    
def backward_pass(graphe,debut_tot,fin_tot):
    #backward pass

    debut_tard = {n : math.inf for n in graphe.noeuds}#date de départ maximum
    fin_tard = {n : math.inf for n in graphe.noeuds}#date de fin minimum
    par = parents(graphe)
    noeuds_fin = {n for n in graphe.noeuds if len(graphe.adj[n])==0}#noeud de fin
    file = []
    duree_chemin_critique = max(fin_tot.values())
    for n in noeuds_fin:
        fin_tard[n] = duree_chemin_critique
        debut_tard[n] = duree_chemin_critique - graphe.poids[n]#date de départ minimale
        file += par[n]
    while len(file)>0:
        n = file.pop(0)
        fils_parcourus = True
        for n_fils in graphe.adj[n]:
            if fin_tard[n_fils] is None: fils_parcourus = False
        
        if fils_parcourus:
            file += par[n]
            for n_fils in graphe.adj[n]:
                if debut_tard[n_fils]<fin_tard[n]:
                    fin_tard[n] = debut_tard[n_fils]
                    debut_tard[n] = debut_tard[n_fils]-graphe.poids[n]
     
    return debut_tard,fin_tard


def main():
    #grCours = Graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})
   
    grph = csv_to_Graphe("G_bas")
    debut_tot,fin_tot= forward_pass(grph)
    debut_tard,fin_tard = backward_pass(grph,debut_tot,fin_tot)
    print(debut_tot)
    print(fin_tot)
    print(debut_tard)
    print(fin_tard)
    
    """print(grph.noeuds)
    print(grph.adj)
    print(grph.poids)"""
    
    
    
    """print(Dijkstra(grph,"PC",grph.poids))
    print(Dijkstra(grph,"PC",grph.poids,neg = True))
    
    print()
    print(Bellman_Ford(grph,"PC",grph.poids))
    print("le graphe contient un cycle ?" ,grph.contient_cycle())
    print(chemins_critique(grph))
    to_csv("G",["Identificateur","Description","Durée","Précédente(s)","S0","S1","S2"],
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
    """
    
if __name__ == "__main__":
    main()


