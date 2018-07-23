# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:43:31 2017

@author: Théo
"""

from core.agents.agent import Agent

from copy import copy

class Animal(Agent):
    """"""
    
    def __init__(self):
        """"""
        Agent.__init__(self)
        
    def giveBirth(self, status):
        """Créer sur à la case appropriée un nouvel agent du type donné"""
        selection = copy(self._location.neighbours)
        choice = None
        for case in copy(selection):
            if case == None:
                selection.remove(case)
            elif not case.agent == None:
                selection.remove(case)
        choice = self.choose(selection)
        if not choice == None:
            choice.agent = status.AGENT_TYPE()
            status(choice.agent)
        
    def move(self, status=None):
        """Déplace l'Animal à la location appropriée et applique à la case quittée le status donné"""
        case = self.choose([case for case in copy(self._location.neighbours) if not case == None], False)
        if not case == None and not case == self._location:
            print(case._loc)
            if not case.agent == None:
                self.react(case.agent, True)
            if case.agent == None:
                if status == None:
                    self._location.agent = None
                else:
                    agent = status.AGENT_TYPE()
                    status(agent)
                    self._location.agent = agent
                case.agent = self