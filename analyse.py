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
    string += '''
\\section{Visualisation du projet par un graphe}
'''
                                    #Visualisation
    
    string += grph.géné_lateX() 
    string += '\\medskip'
  
    """                    #Tableaux tâches-descriptions et tâche-durée
  
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
    """
    
    string += ('''
\\end{document}''')
    return string

def rediger_rapport(fichier_csv):
    string = rediger_lateX(fichier_csv)
    x = open("Analyse.tex","w")
    x.write(string)
    
rediger_rapport('Graphe2')