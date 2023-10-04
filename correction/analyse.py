from fonctions_principales import *

def rediger_rapport(fichier_taches, fichier_liaisons):
    g = generer_graphe(fichier_taches,fichier_liaisons)
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
 ''' 
                                     #Faisabilité
    cycle = g.contient_cycle()
    if  not cycle[0]:
        string += 'Votre projet ne contient pas de cycle, il est faisable.'
    else:
        string += "Votre projet n'est pas faisable car il contient un cycle entre les noeuds "
        for couple in cycle[1]:
            string += str(couple)
    string += '''
\\section{Visualisation du projet par un graphe}
'''
                                    #Visualisation
    liaisons = lire_liaisons(fichier_liaisons)
    string += """\\begin{dot2tex}[neato,mathmode, scale = 0.5]
digraph G {node [shape=circle];
"""
    dicotache = duree_taches(fichier_taches)
    dicotot = dates_au_plus_tot(g, fichier_taches)
    dicotard = dates_au_plus_tard(g, 'Dep', 'Fin', fichier_taches)
    parcourus = []
    for i in liaisons:
        if i[0] not in parcourus:
          tot_tard = str([dicotot[i[0]], dicotard[i[0]]])
          label = str(dicotache[str(i[0])])
          string += str(i[0]) + str(" -> ") + str(i[1]) + "[ " + 'label = ' + label + ', ' +  'taillabel = ' + f'"{str(tot_tard)}"'  + " ]; " + ''' 
  ''' 
          parcourus.append(i[0])
        else :
          label = str(dicotache[str(i[0])])
          string += str(i[0]) + str(" -> ") + str(i[1]) + "[ " + 'label = ' + label + " ]; " + ''' 
  '''
            
    string += '''}
\\end{dot2tex}
''' 
    string += '\\medskip'
  
                    #Tableaux tâches-descriptions et tâche-durée
  
    dicodescriptions = description_taches(fichier_taches)
    string += '''
\\begin{tabular}{|l|M|}
\hline 
Identifiant & Description \\tabularnewline
\\hline
'''
  
    for i in dicodescriptions.keys():
        string += str(i) + '&' + str(dicodescriptions[i]) + '''\\tabularnewline
\\hline
'''
    string += '''
\\end{tabular}
'''

    string += '''
\\begin{tabular}{|l|M|N|}
\hline 
Tâche & Date de début au plus tôt & Date de début au plus tard \\tabularnewline
\\hline

'''
    for i in triTopologique(g):
      string += str(i) + '&' + str(dicotot[i]) + '&' + str(dicotard[i]) + '''\\tabularnewline
\\hline
'''
    string += '''
\\end{tabular}'''
                               #Chemins critiques
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

    x = open("Analyse.tex","w")
    x.write(string)
    x.write('''
\\end{document}''')

rediger_rapport('taches.txt', 'liaisons.txt')