# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 21:27:16 2017

@author: Théo
"""

class Queue:
    """"""
    
    def __contains__(self, element):
        """"""
        return element in self._elements
    
    def __init__(self, lst=[]):
        """"""
        self._elements = lst
        
    def __repr__(self):
        """"""
        return self._elements.__repr__()
    
    def clear(self):
        """Vide la queue"""
        self._elements = []
    
    def keys(self):
        """Retourne les premiers éléments de chacun des conteneurs de
           la queue ou les éléments eux-mêmes sinon"""
        result = set()
        for element in self._elements:
            try:
                result.add(element[0])
            except:
                result.add(element)
        return result
    
    def isEmpty(self):
        """Retourne True si la queue est vide d'éléments, None exclus"""
        return len(self._elements) <= 0 \
        or len(self._elements) <= self._elements.count(None)
    
    def isStrictlyEmpty(self):
        """Retourne True si la queue est vide d'éléments, None inclus"""
        return len(self._elements) <= 1
    
    def pop(self):
        """Renvoie l'élément le plus ancien dans la queue"""
        try:
            result = self._elements[0]
            length = len(self._elements)
            for i in range(1, length):
                self._elements[i-1] = self._elements[i]
            del self._elements[length-1]
        except Exception as e:
            print(e)
            result = None
        return result
        
    def put(self, element):
        """Ajoute un élément à la queue"""
        self._elements.append(element)
    
    def putNext(self, element):
        """BOGUE - Ajoute un élément devant la queue"""
        length = len(self._elements)
        self._elements.append(None)
        for i in range(0, length):
            self._elements[i+1] = self._elements[i]
        self._elements[0] = element
        