import pytest
from Main import *

def test_graphe():
    grCours=graphe(set(range (10)),{(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})
    assert graphe.contient_cycle(grCours)==True

test_graphe()