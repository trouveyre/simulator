# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:46:49 2017

@author: Théo
"""

class MetaVar(type):
    """"""
    
    def __new__(metacls, name, status, initialAmount, step, fields, sensors, tStatus, tBirth, tTrace):
        """"""
        attrs = {
                 "INITIAL_AMOUNT": float(initialAmount),
                 "STEP": step,
                 "_FIELDS": fields, # un tuple de pas
                 "_SENSORS": sensors, # dict {variableDetectée: sensibilité; ...}
                 "_T_BIRTH": tBirth, # dict {(operateur, seuil): statusName; ...}
                 "_T_STATUS": tStatus, # liste [(operateur, seuil, statusName), ...]
                 "_T_TRACE": tTrace, # dict {(operateur, seuil): statusName; ...}
                 "__init__": metacls.__initObject,
                 "__str__": metacls.__strObject,
                 "clone": metacls.__clone,
                 "evolve": metacls.__evolve,
                 "expend": metacls.__expend,
                 "let": metacls.__let,
                 "react": metacls.__react,
                 "stepForward": metacls.__stepForward,
                 "amount": metacls.__amount,
                 "FIELDS": metacls.__FIELDS,
                 "SENSORS": metacls.__SENSORS,
                 "T_BIRTH": metacls.__T_BIRTH,
                 "T_STATUS": metacls.__T_STATUS,
                 "T_TRACE": metacls.__T_TRACE
                }
        var = type(name, (), attrs)
        status.VAR_CLASSES[name] = var
        return var
    
    def __clone(self):
        """Copy la variable et renvoie la réplique"""
        dcopy = self.__class__()
        dcopy.amount = self._amount
        return dcopy
    
    def __evolve(self):
        """Retourne le nouveaux status à adopter sinon retourne None"""
        status = None
        for i in range(len(self._T_STATUS)):
            if self._T_STATUS[i][0](float(self._amount), self._T_STATUS[i][1]):
                status = self._T_STATUS[i][2]
                break
        return status
    
    def __expend(self):
        """Retourne le status du nouvel agent à créer"""
        birth = None
        for operator, value in self._T_BIRTH.keys():
            if operator(self._amount, value):
                birth = self._T_BIRTH[(operator, value)]
                break
        return birth
    
    def __getAmount(self):
        """"""
        return self._amount
    
    def __getFields(self):
        """"""
        return self._FIELDS
    
    def __getSensors(self):
        """"""
        return self._SENSORS
    
    def __getTBirth(self):
        """"""
        return self._T_BIRTH
    
    def __getTStatus(self):
        """"""
        return self._T_STATUS
    
    def __getTTrace(self):
        """"""
        return self._T_TRACE
    
    def __initObject(self):
        """"""
        self._amount = self.INITIAL_AMOUNT
        
    def __let(self):
        """Retourne le status laissé par un animal après un déplacement"""
        trace= None
        for operator, value in self._T_TRACE.keys():
            if operator(self._amount, value):
                trace = self._T_TRACE[(operator, value)]
                break
        return trace
        
    def __react(self, agent):
        """"""
        toAdd = []
        isSub = False
        for field, sensitivity in self.SENSORS.items():
            for var in agent.status.variables:
                if field == var.__class__.__name__:
                    toAdd.append(var.amount * sensitivity)
        for var in agent.status.variables:
            for field, sensitivity in var.SENSORS.items():
                if field == self.__class__.__name__ and sensitivity > 0:
                    isSub = True
                    break
            if isSub:
                break
        if isSub:
            self._amount = 0
        for add in toAdd:
            self._amount += add
            
    def __setAmount(self, amount):
        """"""
        self.__amount = amount
        
    def __strObject(self):
        """"""
        return "var {} ({})".format(self.__class__.__name__, self._amount)
        
    def __stepForward(self, case):
        """Fais avencer d'une unité de temps la variable"""
        self._amount += self.STEP
        for field, sensitivity in self.SENSORS.items():
            if field in case.fields.keys():
                self._amount += case.fields[field] * sensitivity
    
    __amount = property(fget=__getAmount, fset=__setAmount)
    __FIELDS = property(fget=__getFields)
    __SENSORS = property(fget=__getSensors)
    __T_BIRTH = property(fget=__getTBirth)
    __T_STATUS = property(fget=__getTStatus)
    __T_TRACE = property(fget=__getTTrace)