import math
import csv


class Graphe :
    def __init__(self, noeuds : set, arcs : list[tuple[int,int]],poids :dict[str : int],descriptions : dict[str,str] = dict()) -> None:
        """rajouter les descriptions

        Args:
            noeuds (set): _description_
            arcs (_type_): _description_
        """
        
        self.noeuds = noeuds
        self.adj = {n : [a[1] for a in arcs if a[0] == n] for n in noeuds}
        self.poids = poids
        self.descriptions = descriptions
    
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
 
def csv_to_Graphe(nom_fichier:str,k:int=0) -> Graphe:  
    """
    Creer et renvois le graphe associé à un fichier csv.
    Args:
        nom_fichier (str): nom fichier à convertir
        k(int):nombre de suivi réalisé
    Returns:
        Graphe: Graphe issu du fichier.
    """
    Dict_poids={}
    Dict_description={}
    with open('Dépot_de_projet/' + nom_fichier+'.csv','r',encoding='utf8') as file:
        noeud=set()
        arcs=[]
     
        if k==0:
            for ligne in file:
                s=ligne.split(',')
                noeud = noeud  | {s[0]}
                Dict_poids[s[0]] = float(s[2])
                Dict_description[s[0]]=s[1]
                if len(s)>3 and not s[3]=='':
                        arcs += couple(s)
            return(Graphe(noeud,arcs,Dict_poids,Dict_description),csv_to_Graphe(nom_fichier,k+1),csv_to_Graphe(nom_fichier,k+2),csv_to_Graphe(nom_fichier,k+3))
        else:
            for ligne in file:
                s=ligne.split(',')
                if s[3+k]=='' or s[3+k]=='\n':
                    return None
                else:
                    noeud = noeud  | {s[0]}
                    Dict_poids[s[0]] = float(s[3+k])
                    Dict_description[s[0]]=s[1]
                    if len(s)>3 and not s[3]=='':
                            arcs += couple(s)
                    else:
                        pass
            return Graphe(noeud,arcs,Dict_poids,Dict_description)

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

#Bas
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
    """Détermine les dates de départ au plus tot et de fin au plus tot (départ au plus tot + )

    Args:
        graphe (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    #forward pass
    debut_tot = {n : -1 for n in graphe.noeuds}#date de départ minimum
    fin_tot = {n : -1 for n in graphe.noeuds}#date de fin minimum
    par = parents(graphe)
    noeuds_départ  = {n for n in graphe.noeuds if par[n] == set()}# donne les noeuds de départ du graphe (qui n'ont pas de parents)
    file = []
    for n in noeuds_départ:
        debut_tot[n] = 0
        fin_tot[n] = graphe.poids[n]#date de départ minimale
        file += graphe.adj[n]
    
    while len(file)>0:
        n = file.pop(0)
        #on vérifie que tout les parents du noeuds ont déjà étés parcourus
        parents_parcourus = True
        for n_parent in par[n]:
            if fin_tot[n_parent]<0: parents_parcourus = False
            
        #si tout les parents sont parcourus, on détermine le début au plus tot
        if parents_parcourus:
            file += graphe.adj[n]
            for n_parent in par[n]:
                if fin_tot[n_parent]>debut_tot[n]:
                    debut_tot[n] = fin_tot[n_parent]
                    fin_tot[n] = fin_tot[n_parent]+graphe.poids[n]
    return debut_tot,fin_tot    
    
def backward_pass(graphe,debut_tot,fin_tot):
    #backward pass
    #même principe que à l'aller mais on parcours le graphe dans le sens inverse
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
        #on détermine si tout les fils ont étés parcourus
        fils_parcourus = True
        for n_fils in graphe.adj[n]:
            if fin_tard[n_fils] is None: fils_parcourus = False
        #si tous les fils sont parcourus, on détermine la date de fin au plus tard (cad la plus petite des dates de début au plus tot de ses fils)
        if fils_parcourus:
            file += par[n]
            for n_fils in graphe.adj[n]:
                if debut_tard[n_fils]<fin_tard[n]:
                    fin_tard[n] = debut_tard[n_fils]
                    debut_tard[n] = debut_tard[n_fils]-graphe.poids[n]
     
    return debut_tard,fin_tard


def noeuds_critiques(graphe,debut_tot,fin_tard):
    """Détermine les noeuds qui ne peuvent pas avoir de retard

    Args:
        graphe (Graphe): graphe a analyser
        debut_tot (dict): dates de début au plus tot de chaque tache
        fin_tard (dict): dates de fin au plus tard de chaque tache

    Returns:
        set: noeuds dis critique
    """
    noeud_critiques = set()
    for noeud in graphe.noeuds:
        if debut_tot[noeud]+graphe.poids[noeud] == fin_tard[noeud]:
            noeud_critiques.add(noeud)
    return noeud_critiques


def analyse_PERT(graphe):
    """fonction principale d'analyse PERT

    Args:
        graphe (Graphe): graphe à analyser
    """ 
    #déterminer les dates importantes pour l'analyser
    debut_tot,fin_tot= forward_pass(graphe)
    debut_tard,fin_tard = backward_pass(graphe,debut_tot,fin_tot)
    #déterminer les noeuds qui sont critiques
    n_crit = noeuds_critiques(graphe,debut_tot,fin_tard)
    #on trie les noeuds dans l'ordre topologique (chaque noeuds peut etre réalisé si tout les noueds qui le précèdent sont réalisés)
    n_triés = sorted(debut_tot, key = debut_tot.get)
    return(n_triés,n_crit,debut_tot,fin_tard)




def main():
    #grCours = Graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})
    """print(grph.noeuds)
    print(grph.adj)
    print(grph.poids)
    grph = csv_to_Graphe("G_bas")
    debut_tot,fin_tot= forward_pass(grph)
    debut_tard,fin_tard = backward_pass(grph,debut_tot,fin_tot)
    print(debut_tot)
    print(fin_tot)
    print(debut_tard)
    print(fin_tard)
    """
    
    
    
    
    """
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


