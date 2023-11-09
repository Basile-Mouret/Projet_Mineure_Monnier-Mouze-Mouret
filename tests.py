import pytest
from fonctions import *

def test_graphe():
    gr1=Graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)},5)
    assert Graphe.contient_cycle(gr1)==True
    gr2=Graphe(set(range(5)),{(1,2),(2,3),(3,4),(0,4)},5)
    assert Graphe.contient_cycle(gr2)==False
    gr3=Graphe(set(range(4)),{(0,0),(0,1),(1,2)},5)
    assert Graphe.contient_cycle(gr3)==True
    assert Graphe.contient_cycle(csv_to_Graphe("Graphe_cours")[0])==True
    assert Graphe.contient_cycle(csv_to_Graphe("Graphe_cours2")[0])==False


def test_parents():
    gr1=Graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)},5)
    gr3=Graphe(set(range(3)),{(0,1),(0,2),(0,0)},5)
    assert parents(gr3)=={0: {0}, 1: {0}, 2: {0}}
    assert parents(gr1)=={0: {4}, 1: {8}, 2: {8}, 3: {1}, 4: {2}, 5: set(), 6: {1, 7}, 7: {0}, 8: {4, 5}, 9: {2}}
    

def test_forward_pass():
    assert forward_pass(csv_to_Graphe("Graphe_base")[0])==({'B': 0, 'C': 7.0, 'A': 0, 'D': 9.0, 'F': 26.0, 'G': 26.0, 'E': 17.0}, {'B': 9.0, 'C': 19.0, 'A': 7.0, 'D': 17.0, 'F': 32.0, 'G': 31.0, 'E': 26.0})

def test_backward_pass():
    assert backward_pass(csv_to_Graphe("Graphe_base")[0],{'B': 0, 'C': 7.0, 'A': 0, 'D': 9.0, 'F': 26.0, 'G': 26.0, 'E': 17.0}, {'B': 9.0, 'C': 19.0, 'A': 7.0, 'D': 17.0, 'F': 32.0, 'G': 31.0, 'E': 26.0})== ({'F': 26.0, 'G': 27.0, 'C': 14.0, 'B': 0.0, 'A': 2.0, 'D': 9.0, 'E': 17.0}, {'F': 32.0, 'G': 32.0, 'C': 26.0, 'B': 9.0, 'A': 9.0, 'D': 17.0, 'E': 26.0})

def test_noeud_critique():
    assert noeuds_critiques(csv_to_Graphe("Graphe_base")[0],{'B': 0, 'C': 7.0, 'A': 0, 'D': 9.0, 'F': 26.0, 'G': 26.0, 'E': 17.0}, {'F': 32.0, 'G': 32.0, 'C': 26.0, 'B': 9.0, 'A': 9.0, 'D': 17.0, 'E': 26.0})=={'F', 'E', 'B', 'D'}

