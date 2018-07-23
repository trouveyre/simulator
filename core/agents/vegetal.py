# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:43:32 2017

@author: Théo
"""

from core.agents.agent import Agent

from copy import copy

class Vegetal(Agent):
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
        
    def move(self, location, status=None):
        """Ne fais rien"""
        pass