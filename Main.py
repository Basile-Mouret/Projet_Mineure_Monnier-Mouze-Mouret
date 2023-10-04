


class graphe :
    def __init__(self, noeuds, arcs) -> None:
        self.noeuds = noeuds
        self.arcs = {n : [a[1] for a in arcs if a[0] == n] for n in noeuds}
    

    def parcoursLargeur(self, s : int) -> list:
        """parcours d'un graphe depuis un noeud s

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
        """parcours d'un graphe depuis un noeud s
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
    



    def cycle(self) -> bool:
        """détecte si le graphe contient un cycle
        
        Returns:
            bool: résultat
        """
        for noeud in self.noeuds:
            pile = [noeud]
            parcours = []
            while len(pile)!=0:
                n = pile.pop(-1)
                parcours.append(n)
                for i in self.arcs[n]:
                    if i not in parcours:
                        pile.append(i)
                    else : return True#détection d'un cycle
        return False
    
    
    def géné_lateX(self):
        tex = "\documentclass{article}\n\\usepackage{tikz}\n\\begin{document}"
        tex += "\\begin{dot2tex}[neato,options=-tmath,scale=0.5]digraph grours {rankdir=LR;\n"
        for arc in self.arcs:
            for i in self.arcs[arc]:
                tex+=f"{arc} -> {i};"
        tex += "\n\\end{dot2tex}\n\end{document}"
        file = open("Latex/latex.tex", "w")
        file.write(tex)
        file.close()
            
def main():
    grCours = graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})
    grCours.géné_lateX()
    
    
    
    
if __name__ == "__main__":
    main()

