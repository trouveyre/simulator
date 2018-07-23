# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:50:52 2017

@author: Théo
"""

from threading import RLock
from threading import Thread

from time import sleep
    
class Cycle(Thread):
    """La classe permettant de simuler en continue"""
        
    def __init__(self, world, functions, breakTime=0.5):
        """"""
        Thread.__init__(self)
        self._world = world
        self._functions = functions
        self._break = breakTime
        self._goOn = False
        self._lock = RLock()
            
    def __getBreak(self):
        """"""
        return self._break
            
    def __getFunctions(self):
        """"""
        return self._functions
        
    def __getLock(self):
        """"""
        return self._lock
        
    def __getGoOn(self):
        """"""
        return self._goOn
            
    def run(self):
        """"""
        while True:
            with self._lock:
                if self._goOn:
                    self._world.stepForward()
                    for function, args in self._functions:
                        for arg in args:
                            function(arg())
                else:
                    break
            sleep(self._break)
        
    def __setBreak(self, breakTime):
        """"""
        with self._lock:
            self._break = breakTime
        
    def __setFunctions(self, functions):
        """"""
        self._functions = functions
            
    def __setGoOn(self, boolean):
        """"""
        self._goOn = boolean
    
    breakTime = property(fget=__getBreak, fset=__setBreak)
    functions = property(fget=__getFunctions, fset=__setFunctions)
    lock = property(fget=__getLock)
    goOn = property(fget=__getGoOn, fset=__setGoOn)