# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:21:55 2017

@author: Théo
"""

from core.cases.queue import Queue

from random import choice

class Agent:
    """"""
    
    statusList = {}
    actionsList = Queue()
    
    def clone(self):
        """Copy l'agent et renvoie la réplique"""
        dcopy = self.__class__()
        dcopy.location = self._location
        self._status.clone(dcopy)
        return dcopy
    
    def __init__(self):
        """"""
        self._location = None
        self._status = None
        
    def __repr__(self):
        """"""
        return self._status.__class__.__name__[0]
    
    def __str__(self):
        """"""
        return "{}({})".format(self.__class__.__name__, self._status.__str__())
        
    def changeState(self, statusClass):
        """Change le status de l'agent"""
        statusClass(self)
    
    def choose(self, selection, standStill=False):
        """Choisi parmis les cases données la case la plus attirante ou au hasard"""
        result = None
        previous = 0
        if standStill:
            cases = [self._location]
        else:
            cases = []
        # on initialise la valeur de comparaison
        for var in self._status._vars:
            for field, sensitivity in var.SENSORS.items():
                if len(selection) > 0 and field in self._location.fields.keys():
                    previous = self._location.fields[field] * sensitivity
        # on fabrique la selection de cases dans laquelle choisir
        for case in selection:
            actual = 0
            for var in self._status._vars:
                for field, sensitivity in var.SENSORS.items():
                    if not case.agent == None:
                        for varE in case.agent.status.variables:
                            if field == varE.__class__.__name__:
                                actual += varE.amount * sensitivity
                    if field in case.fields.keys():
                        actual += case.fields[field] * sensitivity
            if actual > previous:
                cases = [case]
                previous = actual
            elif actual == previous:
                cases.append(case)
        # on choisi la case
        if not len(cases) == 0:
            result = choice(cases)
        return result
    
    @staticmethod
    def doActions():
        """"""
        while not Agent.actionsList.isEmpty():
            la  = Agent.actionsList.pop()
            function, agent, status = la
            function(agent, status)
    
    def __getLocation(self):
        """"""
        return self._location
    
    def __getStatus(self):
        """"""
        return self._status
    
    def react(self, agent, mutual=False):
        """"""
        image = agent.clone()
        if mutual:
            agent.react(self)
        self._status.react(image)
        self.update()
    
    def __setLocation(self, case):
        """"""
        self._location = case
    
    def __setStatus(self, status):
        """"""
        self._status = status
        
    def stepForward(self):
        """Fais avancer d'une unité de temps l'agent"""
        self._status.stepForward(self._location)
        
        for var in self._status._vars:
            birth = var.expend()
            if not birth == None:
                Agent.actionsList.put((self.__class__.giveBirth, self, birth))
        
        trace = None
        for var in self._status._vars:
            trace = var.let()
            if not trace == None:
                break
        Agent.actionsList.put((self.__class__.move, self, trace))
            
    def update(self):
        """Prévois la mise à jour le status de l'agent"""
        for var in self._status._vars:
            status = var.evolve()
            if not status == None:
                self.changeState(status)
                break
            
    location = property(fget=__getLocation, fset=__setLocation)
    status = property(fget=__getStatus, fset=__setStatus)