# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:04:16 2017

@author: Théo
"""

from core.cases.queue import Queue

class Case:
    """"""

    def __init__(self, loc=None):
        """"""
        self._neighbours = [None for i in range(8)]
        self._fields = {} # Dictionnaire de la forme "fieldName": fieldPower
        self._agent = None
        self._loc = loc

    def __repr__(self):
        """"""
        return "Agent: {}; fields: {}".format(self._agent, self._fields)

    def __str__(self):
        """"""
        return "CASE WITH AGENT: {} AND FIELDS: {}"\
                .format(self._agent, self._fields)
    
    def clone(self):
        """Copy la case et renvoie la réplique"""
        dcopy = self.__class__()
        if not self._agent == None:
            dcopy.agent = self._agent.clone()
        return dcopy
    
    def __getAgent(self):
        """Renvoie l'agent qui occupe cette case"""
        return self._agent
    
    def __getFields(self):
        """Renvoie les valeurs des fields sur cette case"""
        return self._fields

    def __getNeighbours(self):
        """Renvoie les cases voisines de cette case"""
        return self._neighbours

    def runUpdate(self):
        """Mets à jour toutes les cases selon l'état actuelle
           de cette case si elle est occupée par un agent"""
        if not self._agent == None:
            for var in self._agent.status.variables:
                for step in var.FIELDS.values():
                    toDo = Queue()
                    done = {self}
                    for neighbour in self._neighbours:
                        if not neighbour == None:
                            toDo.put((neighbour, var.__class__.__name__, var.amount+step))
                    while not toDo.isEmpty():
                        case, fieldName, amount = toDo.pop()
                        case.update(fieldName, amount)
                        done.add(case)
                        for neighbour in case.neighbours:
                            if not neighbour == None:
                                if not neighbour in toDo.keys():
                                    if not neighbour in done:
                                        if amount+step > 0:
                                            toDo.put((neighbour, var.__class__.__name__, amount+step))

    def __setAgent(self, agent):
        """Modifie l'agent actuel de la case"""
        self._agent = agent
        if not agent == None:
            agent.location = self

    def setNeighbours(self, N=None, NE=None, E=None, SE=None, 
                      S=None, SW=None, W=None, NW=None):
        """Modifie les cases perçues comme voisine par celle-ci"""
        if not N == None:
            self._neighbours[0] = N
        if not NE == None:
            self._neighbours[1] = NE
        if not E == None:
            self._neighbours[2] = E
        if not SE == None:
            self._neighbours[3] = SE
        if not S == None:
            self._neighbours[4] = S
        if not SW == None:
            self._neighbours[5] = SW
        if not W == None:
            self._neighbours[6] = W
        if not NW == None:
            self._neighbours[7] = NW

    def setUp(self, sense=False):
        """Réinitialise le niveau des fields de cette case"""
        self._fields = {}
        if sense:
            if not self._agent == None:
                for var in self._agent.status.variables:
                    for field in var.FIELDS.keys():
                        self._fields[field] = var.amount

    def stepForward(self):
        """Fais avancer d'une unité de temps la case"""
        if not self._agent == None:
            return self._agent.stepForward()
        
    def update(self, fieldName, amount):
        """Mets à jour les fields selon leurs états actuels"""
        if fieldName in self._fields.keys():
            self._fields[fieldName] += amount
        else:
            self._fields[fieldName] = amount
    
    agent = property(fget=__getAgent, fset=__setAgent)
    fields = property(fget=__getFields)
    neighbours = property(fget=__getNeighbours)