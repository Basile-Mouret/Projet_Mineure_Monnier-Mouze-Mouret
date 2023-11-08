from fonctions import *

def rediger_lateX(fichier_csv):
    
    grph = csv_to_Graphe(fichier_csv)
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
    string += 'Votre projet ne contient pas de cycle, il est faisable.'
    #Analyse du graphe
    n_triés,n_crit,dicotot,dicotard = analyse_PERT(grph)
    
    string += '''
\\section{Visualisation du projet par un graphe}
'''
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
    """
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
"""
    string += '''
\\begin{tabular}{|l|M|N|}
\hline 
Tâche & Date de début au plus tôt & Date de début au plus tard \\tabularnewline
\\hline

'''
    for noeud in n_triés:
      string += str(noeud) + '&' + str(dicotot[noeud]) + '&' + str(dicotard[noeud]) + '''\\tabularnewline
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
    
    
    string += ('''
\\end{document}''')
    return string

def rediger_rapport(fichier_csv):
    string = rediger_lateX(fichier_csv)
    x = open("Analyse.tex","w")
    x.write(string)
    
rediger_rapport('Graphe3')