# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:02:21 2017

@author: Théo
"""

from core.agents.agent import Agent

from core.cases.case import Case
from core.cases.cycle import Cycle

class World:
    """Classe "racine" de la simulation"""
    
    def __init__(self, configManager=None):
        """"""
        self._configManager = configManager
        self._defaultColor = "white"
        self._dim = (5, 20) # tuple (numeroLigne, numeroColone)
        self._map = {} # dictionnaire {location: Case}
        self._thread = None
        if not configManager == None:
            self._defaultColor = configManager.getWorldColor()
            self._dim = configManager.getWorldDimension()
            self._initialPositioning = configManager.getInitialPositioning()
        self.__time = 0
        self.__setTime(0)
                    
    def __repr__(self):
        """"""
        result = "+"
        for j in range(self._dim[1]):
            result += "-+"
        for i in range(self._dim[0]):
            result += "\n|"
            for j in range(self._dim[1]):
                if self._map[(i, j)].agent == None:
                    result += " |"
                else:
                    result += "{}|".format(self._map[(i, j)].agent.__repr__())
            result += "\n+"
            for j in range(self._dim[1]):
                result += "-+"
        return result + "\nTIME : {}".format(self.__time)
    
    def __str__(self):
        """"""
        result = "World time:{} [".format(self.__time)
        for loc, case in sorted(self._map.items()):
            result += "\n{} -> {}".format(loc, case)
        result += "\n]"
        return result
    
    def addAgent(self, agent, loc):
        """"""
        if loc in self._map:
            self._map[loc].agent = agent
            
    def _bind(self):
        """Définie les voisins de chaque case"""
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                if (i-1, j) in self._map:
                    self._map[(i, j)].setNeighbours(N=self._map[(i-1, j)])
                if (i, j+1) in self._map:
                    self._map[(i, j)].setNeighbours(E=self._map[(i, j+1)])
                if (i+1, j) in self._map:
                    self._map[(i, j)].setNeighbours(S=self._map[(i+1, j)])
                if (i, j-1) in self._map:
                    self._map[(i, j)].setNeighbours(W=self._map[(i, j-1)])
                if (i-1, j-1) in self._map:
                    self._map[(i, j)].setNeighbours(NW=self._map[(i-1, j-1)])
                if (i-1, j+1) in self._map:
                    self._map[(i, j)].setNeighbours(NE=self._map[(i-1, j+1)])
                if (i+1, j+1) in self._map:
                    self._map[(i, j)].setNeighbours(SE=self._map[(i+1, j+1)])
                if (i+1, j-1) in self._map:
                    self._map[(i, j)].setNeighbours(SW=self._map[(i+1, j-1)])
                
    def _build(self):
        """Mets en place les cases de la simulation"""
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                self._map[(i, j)] = Case((i, j))
    
    def delAgent(self, agent):
        """"""
        for case in self._map:
            if case.agent is agent:
                case.agent = None
                
    def __getConfigManager(self):
        """"""
        return self._configManager
                
    def getMap(self):
        """"""
        return self._map
    
    def __getTime(self):
        """"""
        return self.__time
    
    def run(self, functions, breakTime=0.5):
        """Instancie un thread qui fait tourner en continue la simulation"""
        self._thread = Cycle(self, functions, breakTime)
        self._thread.goOn = True
        self._thread.start()
        
    def __setTime(self, time):
        """"""
        self.__time = 0
        self._build()
        self._bind()
        if not self._configManager == None:
            for i in range(len(self._initialPositioning)):
                self.addAgent(self._initialPositioning[i][0].clone(), 
                              self._initialPositioning[i][1])
        for case in self._map.values():
            case.setUp()
        for case in self._map.values():
            case.runUpdate()
        while self.__time < time:
            self.stepForward()
            
    def stepForward(self):
        """Fais avancer d'une unité de temps le monde"""
        Agent.actionsList.clear()

        for case in self._map.values():
            case.stepForward()
        
        for case in self._map.values():
            case.setUp()
        for case in self._map.values():
            case.runUpdate()
        
        Agent.doActions()
        
        for case in self._map.values():
            if not case.agent == None:
                case.agent.update()
        
        for case in self._map.values():
            case.setUp()
        for case in self._map.values():
            case.runUpdate()
        
        self.__time += 1
            
    def stop(self):
        """"""
        with self._thread.lock:
            self._thread.goOn = False
            
    connfigManager = property(fget=__getConfigManager)
    map = property(fget=getMap)
    time = property(fget=__getTime, fset=__setTime)
    
    