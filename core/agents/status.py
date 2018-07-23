# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:39:08 2017

@author: Théo
"""

from core.agents.agent import Agent
from core.agents.animal import Animal
from core.agents.mineral import Mineral
from core.agents.vegetal import Vegetal

class MetaStatus(type):
    """Permet la création de classes de status"""
    
    def __new__(metacls, name, agentClasses, color):
        """"""
        attrs = {
                 "COLOR": color,
                 "VAR_CLASSES": {},
                 "AGENT_TYPE": agentClasses[0],
                 "__init__": metacls.__initObject,
                 "__str__": metacls.__strObject,
                 "clone": metacls.__clone,
                 "react": metacls.__react,
                 "stepForward": metacls.__stepForward,
                 "variables": metacls.__variables
                }
        status = type(name, (object, ), attrs)
        Agent.statusList[name] = status
        return status
    
    def __clone(self, agent):
        """Copy le status et renvoie la réplique"""
        dcopy = self.__class__(agent)
        varss = set()
        for var in self._vars:
            varss.add(var.clone())
        dcopy.variables = varss
        return dcopy
        
    def __getVars(self):
        """Retourne les variables du status"""
        return self._vars
    
    def __initObject(self, agent):
        """"""
        self.color = self.COLOR
        self._vars = {var() for var in self.VAR_CLASSES.values()}
        agent.status = self
        
    def __react(self, agent):
        """"""
        for var in self._vars:
            var.react(agent)
            
    def __setVars(self, varss):
        """"""
        self._vars = varss
        
    def __stepForward(self, case):
        """Fais avencer d'une unité de temps ce status"""
        for var in self._vars:
            var.stepForward(case)
        
    def __strObject(self):
        """"""
        result = self.__class__.__name__ + " ["
        for var in self._vars:
            result += " {}".format(var)
        result += " ]"
        return result
    
    __variables = property(fget=__getVars, fset=__setVars)
    
class MetaDeath:
    """Créer une classe de status prédéfinie"""
    
    def __new__(metacls):
        """Créer la classe de status death"""
        status = MetaStatus("death", [Animal, Mineral, Vegetal], "uneCouleur")
        setattr(status, "__new__", MetaDeath.__kill)
        return status
    
    def __kill(cls, agent):
        """Lors de l'instanciation du status death, supprime l'agent passé en argument"""
        agent.location.agent = None
    
class MetaEnd:
    """Créer une classe de status prédéfinie"""
    
    def __new__(metacls):
        """Créer la classe de status end"""
        status = MetaStatus("end", [Animal, Mineral, Vegetal], "uneCouleur")
        setattr(status, "__new__", MetaEnd.__finish)
        return status
        
    def __finish(cls, agent):
        """Lors de l'instanciation du status death, termine la simulation"""
        print("TO_END")