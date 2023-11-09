from fonctions import *

def rediger_lateX(fichier_csv):
    
    grph,suivi1,suivi2,suivi3 = csv_to_Graphe(fichier_csv)
    string = '''\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[pdf]{graphviz}
\\usepackage[autosize]{dot2texi}
\\usepackage{tikz}
\\usetikzlibrary{shapes,arrows}


\\title{Analyse de votre projet}
\\begin{document}
\\maketitle


\\section{Faisabilite du projet}
 '''                                #Faisabilité
    if grph.contient_cycle():
        return string +"Votre projet n'est pas faisable car il contient un cycle"+"""
\\end{document}"""
    string += '''Votre projet ne contient pas de cycle, il est faisable.
Nous pouvons donc l'analyser et vous aider à organiser votre travail.
'''
    #Analyse du graphe
    n_triés,n_crit,dicotot,dicotard = analyse_PERT(grph)
    
    string += '''
\\section{Visualisation du projet par un graphe}
\\subsection{Graphe image}
Les chemins critiques sont marques en rouge dans le graphe.'''
                                    #Visualisation
    string += '\n\\begin{dot2tex}[options=-tmath,scale='+str(7/len(grph.noeuds))+']digraph grours '
    string+= "{rankdir=LR;\n"
    for noeud in grph.noeuds:
        string += f'{noeud} [label = "{noeud},{int(grph.poids[noeud])}"]; '
    for n_d in grph.adj:
        for n_f in grph.adj[n_d]:
            string += f'{n_d} -> {n_f}[label = "{grph.poids[n_d]}"'
            string += ',color = "red"];' if n_d in n_crit and n_f in n_crit else "];"
            
            
            
    string += "}\n\\end{dot2tex}"
  
                        #Tableaux tâches-descriptions et tâche-durée
    string+="\n\\subsection{Description des taches}"
    dicodescriptions = grph.descriptions
    
    for tache in n_triés:
        string += tache + " : "+ dicodescriptions[tache] +"\\newline{}"

    string += '''
\\subsection{Tableau des dates}

Ce tableau montre les dates auxquelles vous pourrez commencer chaque tâche au plus tôt et les dates pour lesquelles elles devront êtres finies pour ne pas retarder l'ensemble du projet
Si la tache est de couleur rouge, elle est désignée comme critique,elle n'a pas de mou, c'est a dire qu'un retard sur cette tache implique un retard sur l'ensemble du Projet.\\\\

\\begin{tabular}{|l|l|l|l|l|}
\hline 
Tache & Duree & Date de debut au plus tot & Date de fin au plus tard & Mou\\tabularnewline
\\hline

'''
    for noeud in n_triés:
      string += str(noeud) + '&' +str(grph.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + ('\\textcolor{red}{critique}'if noeud in n_crit else str(dicotard[noeud]-dicotot[noeud]-grph.poids[noeud])) + '''\\tabularnewline
\\hline
'''
    string += '''
\\end{tabular}'''
                               #Chemins critiques
    """                           
    string += '''\\section{Chemins critiques du projet}
'''
    string += '''Les chemins critiques de votre projet sont les suivants : \\medskip
'''
    critique = chemin_critique(g, 'Dep', 'Fin', fichier_taches)
    for chemin in critique[0]:
        string += ''' 
''' + str(chemin) + '\\medskip' '''

'''
    string += "Leur duree est de : " + str(critique[1]) + " jours"
    """
    if suivi1 is not None:
        n_triés,n_crit,dicotot,dicotard = analyse_PERT(suivi1)
        string += '''
\\subsection{Suivi 1}
Ici vous pouvez voir les dates de depart au plus tot et de fin au plus tard du suivi n°1.\\\\
\\begin{tabular}{|l|l|l|l|l|}
\hline 
Tache & Duree & Date de debut au plus tot & Date de fin au plus tard & Mou\\tabularnewline
\\hline

'''
        for noeud in n_triés:
            if suivi1.poids[noeud]==0:
                string += str(noeud) + '&'+ '0 &' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + 'finie' + '''\\tabularnewline
\\hline
'''  
            elif noeud in n_crit:
                string +=str(noeud)+'&' + str(suivi1.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + '\\textcolor{red}{critique}' + '''\\tabularnewline
\\hline
'''         
            else : 
                string += str(noeud) + '&' + str(suivi1.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + str(dicotard[noeud]-dicotot[noeud]-suivi1.poids[noeud]) + '''\\tabularnewline
\\hline
'''

        string += '''
\\end{tabular}'''

    if suivi2 is not None:
        n_triés,n_crit,dicotot,dicotard = analyse_PERT(suivi1)
        string += '''
\\subsection{Suivi 2}
Ici vous pouvez voir les dates de départ au plus tot et de fin au plus tard du suivi n°2. \\\\
\\begin{tabular}{|l|l|l|l|l|}
\hline 
Tache & Duree & Date de debut au plus tot & Date de fin au plus tard & Mou\\tabularnewline
\\hline

'''
        for noeud in n_triés:
            if suivi2.poids[noeud]==0:
                string += str(noeud) + '&'+ '0 &' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + 'finie' + '''\\tabularnewline
\\hline
'''  
            elif noeud in n_crit:
                string += '\\textcolor{red}{'+str(noeud)+'}' +'&' + str(suivi2.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + '\\textcolor{red}{critique}' + '''\\tabularnewline
\\hline
'''         
            else : 
                string += str(noeud) + '&' + str(suivi2.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + str(dicotard[noeud]-dicotot[noeud]-suivi2.poids[noeud]) + '''\\tabularnewline
\\hline
'''

        string += '''
\\end{tabular}'''

    if suivi3 is not None:
        n_triés,n_crit,dicotot,dicotard = analyse_PERT(suivi1)
        string += '''
\\subsection{Suivi 3}
Ici vous pouvez voir les dates de départ au plus tot et de fin au plus tard du suivi n°3. \\\\
\\begin{tabular}{|l|l|l|l|l|}
\hline 
Tache & Duree & Date de debut au plus tot & Date de fin au plus tard & Mou\\tabularnewline
\\hline

'''
        for noeud in n_triés:
            if suivi3.poids[noeud]==0:
                string += str(noeud) + '&'+ '0 &' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + 'finie' + '''\\tabularnewline
\\hline
'''  
            elif noeud in n_crit:
                string += '\\textcolor{red}{'+str(noeud)+'}' +'&' + str(suivi3.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + '\\textcolor{red}{critique}' + '''\\tabularnewline
\\hline
'''         
            else : 
                string += str(noeud) + '&' + str(suivi3.poids[noeud]) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '&' + str(dicotard[noeud]-dicotot[noeud]-suivi3.poids[noeud]) + '''\\tabularnewline
\\hline
'''

        string += '''
\\end{tabular}'''



    string += ('''
\\end{document}''')
    return string

def rediger_rapport(fichier_csv):
    string = rediger_lateX(fichier_csv)
    with  open("Résultat_analyse_PERT/Analyse_PERT_"+fichier_csv+".tex","w",encoding='utf8') as file:
        file.write(string)
    


def main():
    
    fichier_graphe = input("quel est le nom de votre fichier (sans le .csv) : ")
    rediger_rapport(fichier_graphe)

if __name__ == "__main__":main()