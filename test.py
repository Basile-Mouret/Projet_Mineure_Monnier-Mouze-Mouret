import pytest
from Main import *

def test_graphe():
    grCours=graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})
    assert graphe.contient_cycle2(grCours)==True
    grMoi=graphe(set(range(5)),{(1,2),(2,3),(3,4),(0,4)})
    assert graphe.contient_cycle2(grMoi)==False
    grBasile=graphe(set(range(3)),{(0,0),(0,1),(1,2)})
    assert graphe.contient_cycle2(grBasile)==True
test_graphe()