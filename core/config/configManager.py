# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:33:05 2017

@author: Théo
"""

from core.agents.agent import Agent
from core.agents.animal import Animal
from core.agents.mineral import Mineral
from core.agents.status import *
from core.agents.var import MetaVar
from core.agents.vegetal import Vegetal

import re

import random

class ConfigManager:
    """La classe permetant de gérer le fichier de configuration"""
        
    # définition des "constantes" nécessaires
    RE_CONF_AGENT \
    = r"[ \t]*[^#][ \t]*agent[ \t]+(.+?)[ \t]+(.+)(?=[# \t\n])"
    RE_CONF_BLOC \
    = r"(?<=\n)[ \t]*[^#][ \t]*((?:mineral|animal|vegetal)[ \t]+.+?\n)(?=\n)"
    RE_CONF_FIELD \
    = r"(?!\n#[ \t]*)field[ \t]+{}[ \t]+(.+?)(?=[# \t\n])"
    RE_CONF_LOCATION_COLONE \
    = r",[ \t]*(\d+[ \t]*(?::[ \t]*\d+)?)[ \t]*\)"
    RE_CONF_LOCATION_MULTI \
    = r"(\d+)[ \t]*:[ \t]*(\d+)"
    RE_CONF_LOCATION_ROW \
    = r"\([ \t]*(\d+[ \t]*(?::[ \t]*\d+)?)[ \t]*,"
    RE_CONF_SENSOR \
    = r"(?!\n#[ \t]*)sensor[ \t]+{}[ \t]+(.+?)[ \t]+(.+?)(?=[# \t\n])"
    RE_CONF_STATUS \
    = r"(?!\n#[ \t]*)(mineral|animal|vegetal)[ \t]+(.+?)[ \t]+(.+?)(?=[# \t\n])"
    RE_CONF_THRESHOLD \
    = r"(?!\n#[ \t]*)(.+?)[ \t]+{}[ \t]+(<|>|=)?[ \t]+(.+?)[ \t]+(.+?)(?=[# \t\n])"
    RE_CONF_VAR \
    = r"(?!\n#[ \t]*)var[ \t]+(.+?)[ \t]+(.+?)[ \t]+(.+?)(?=[# \t\n])"
    RE_CONF_WORLD_COLOR \
    = r"^(?!#)[ \t]*world[ \t]+.+?[ \t]+.+?[ \t]+(.+?)(?=[# \t\n])"
    RE_CONF_WORLD_DIM \
    = r"^(?!#)[ \t]*world[ \t]+(.+?)[ \t]+(.+?)[ \t]+.+?(?=[# \t\n])"
    
    def __init__(self, pathway="core/config/config.txt"):
        """"""
        self._file = pathway
        self._config = None
    
    def getInitialPositioning(self):
        """Retourne les agents initiaux"""
        result = []
        confAgents = re.findall(self.RE_CONF_AGENT, self._config)
        reConfLocationMulti = re.compile(self.RE_CONF_LOCATION_MULTI)
        if not len(confAgents) == 0:
            for agents in confAgents:
                rows = re.findall(self.RE_CONF_LOCATION_ROW, agents[1])
                colones = re.findall(self.RE_CONF_LOCATION_COLONE, agents[1])
                if len(rows) == len(colones):
                    for i in range(len(rows)):
                        if reConfLocationMulti.match(rows[i]) and reConfLocationMulti.match(colones[i]):
                            fromRow, toRow = reConfLocationMulti.findall(rows[i])[0]
                            fromColone, toColone = reConfLocationMulti.findall(colones[i])[0]
                            for r in range(int(fromRow), int(toRow)+1):
                                for c in range(int(fromColone), int(toColone)+1):
                                    status = Agent.statusList[agents[0]]
                                    agent = status.AGENT_TYPE()
                                    status(agent)
                                    result.append((agent, (r, c)))
                        elif reConfLocationMulti.match(rows[i]):
                            fromRow, toRow = reConfLocationMulti.findall(rows[i])[0]
                            for r in range(int(fromRow), int(toRow)+1):
                                status = Agent.statusList[agents[0]]
                                agent = status.AGENT_TYPE()
                                status(agent)
                                result.append((agent, (r, int(colones[i]))))
                        elif reConfLocationMulti.match(colones[i]):
                            fromColone, toColone = reConfLocationMulti.findall(colones[i])[0]
                            for c in range(int(fromColone), int(toColone)+1):
                                status = Agent.statusList[agents[0]]
                                agent = status.AGENT_TYPE()
                                status(agent)
                                result.append((agent, (int(rows[i]), c)))
                        else:
                            status = Agent.statusList[agents[0]]
                            agent = status.AGENT_TYPE()
                            status(agent)
                            result.append((agent, (int(rows[i]), int(colones[i]))))
        else:
            dim = self.getWorldDimension()
            maxx = int(dim[0]*dim[1]*2/3)
            for status in Agent.statusList.values():
                if not status.__name__ == "death" and not status.__name__ == "end" and not status.__name__ == "trace": 
                    nb = random.randint(0, maxx)
                    for i in range(nb):
                        agent = status.AGENT_TYPE()
                        status(agent)
                        result.append((agent, (random.randint(0, dim[0]), random.randint(0, dim[1]))))
        return result
    
    def getWorldColor(self):
        """Retourne la couleur par défaut des cases"""
        return re.findall(self.RE_CONF_WORLD_COLOR, self._config, re.RegexFlag.M)[0]
    
    def getWorldDimension(self):
        """Retourne les dimensions du monde"""
        reConfWorldDim = re.compile(self.RE_CONF_WORLD_DIM, re.RegexFlag.MULTILINE)
        dim = reConfWorldDim.findall(self._config)[0]
        return (int(dim[0]),
                int(dim[1]))
        
    def load(self):
        """Charge le fichier de configuration"""
        blocs = re.findall(self.RE_CONF_BLOC, self._config, re.DOTALL)
        reConfStatus = re.compile(self.RE_CONF_STATUS)
        reConfVar = re.compile(self.RE_CONF_VAR)
        
        #créé les classes de status
        MetaDeath()
        MetaEnd()
        for bloc in blocs:
            agentType, statusName, color = reConfStatus.findall(bloc)[0]
            if agentType == "animal":
                MetaStatus(statusName, [Animal], color)
            elif agentType == "mineral":
                MetaStatus(statusName, [Mineral], color)
            elif agentType == "vegetal":
                MetaStatus(statusName, [Vegetal], color)
        
        #créé les classes de variables
        for bloc in blocs:
            status = reConfStatus.findall(bloc)[0][1]
            varss = reConfVar.findall(bloc)
            for var in varss:
                #prépare les arguments pour créer la variable
                tStatus = []
                tBirth = {}
                tTrace = {}
                fields = {}
                sensors = {}
                thresholds = re.findall(self.RE_CONF_THRESHOLD.format(var[0]), bloc)
                for action, operator, threshold, state in thresholds:
                    if operator == "<":
                        operator = float.__lt__
                    elif operator == ">":
                        operator = float.__gt__
                    elif operator == "=":
                        operator = float.__eq__
                    if action == "status":
                        tStatus.append((operator, float(threshold), Agent.statusList[state]))
                    elif action == "birth":
                        tBirth[(operator, float(threshold))] = Agent.statusList[state]
                    elif action == "trace":
                        tTrace[(operator, float(threshold))] = Agent.statusList[state]
                for step in re.findall(self.RE_CONF_FIELD.format(var[0]), bloc):
                    fields[var[0]] = float(step)
                for fieldName, sensitivity in re.findall(self.RE_CONF_SENSOR.format(var[0]), bloc):
                    sensors[fieldName] = float(sensitivity)
                #créé la variable
                MetaVar(var[0], Agent.statusList[status], float(var[1]), float(var[2]), fields, sensors, tStatus, tBirth, tTrace)
        
    def setUpConfig(self):
        """Place en mémoire le fichier de configuration"""
        with open(self._file, 'r') as configFile:
            self._config = configFile.read().lower()
            configFile.close()