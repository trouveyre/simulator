# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:18:25 2017

@author: Théo
"""

from core.world import World

from core.agents.animal import Animal
from core.agents.mineral import Mineral
from core.agents.status import *
from core.agents.var import MetaVar
from core.agents.vegetal import Vegetal

from core.config.configManager import ConfigManager
    
def build(file="core/config/lifeGame.txt"):
    """"""
    global w
    cm = ConfigManager(file)
    cm.setUpConfig()
    cm.load()
    w = World(cm)
    print(w)
    print(w.__repr__())
    
def run(breakTime=None, verbose=False):
    """"""
    args = [w.__repr__]
    if verbose:
        args = [w.__str__, w.__repr__]
    if breakTime == None:
        w.run([(print, args)])
    else:
        w.run([(print, args)], breakTime)
    input("Press enter to stop the running thread")
    w.stop()

def stepForward(verbose=False):
    """"""
    w.stepForward()
    if verbose:
        print(w)
    print(w.__repr__())

def test():
    """"""
    global w
    w = World()
    
    scA = MetaStatus("animal", [Animal], "uneCouleur")
    scH = MetaStatus("hungry", [Animal], "uneCouleur")
    MetaVar("fed", scA, 50, -5, {}, {"food": 1}, [(float.__le__, 40, scH), (float.__gt__, 50, scA)], {}, {})
    MetaVar("fed", scH, 40, -5, {}, {"food": 1}, [(float.__gt__, 50, scA), (float.__le__, 0, MetaDeath())], {}, {})
    MetaVar("sense", scH, 0, 0, {}, {"smell": 1} , [], {}, {})
    a1 = Animal()
    a2 = Animal()
    scA(a1)
    scA(a2)
    
    scG = MetaStatus("grass", [Vegetal], "uneCouleur")
    MetaVar("food", scG, 10, 4, {}, {}, [(float.__le__, 0, MetaDeath())], {(float.__ge__, 20): scG}, {})
    MetaVar("smell", scG, 10, 0, {"smell": -1}, {}, [], {}, {})
    v1 = Vegetal()
    v2 = Vegetal()
    v3 = Vegetal()
    v4 = Vegetal()
    scG(v1)
    scG(v2)
    scG(v3)
    scG(v4)
    
    scM = MetaStatus("mineral", [Mineral], "uneCouleur")
    m1 = Mineral()
    m2 = Mineral()
    m3 = Mineral()
    scM(m1)
    scM(m2)
    scM(m3)
    
    w.addAgent(a1, (3, 9))
    w.addAgent(a2, (2, 9))
    w.addAgent(v1, (4, 2))
    w.addAgent(v2, (0, 18))
    w.addAgent(v3, (4, 18))
    w.addAgent(v4, (2, 2))
#    w.addAgent(m1, (4, 17))
#    w.addAgent(m2, (1, 11))
#    w.addAgent(m3, (2, 3))
    
    print(w)
    print(w.__repr__())
    
# variable gloabal contenant le monde ! \o/
w = None