# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 22:38:28 2017

@author: Théo
"""

from core.cases.case import Case

from core.config.configManager import ConfigManager

from core.world import World

from tkinter import *

class ButtonsFrame(Frame):
    """La partie contenant tous les boutons"""
    
    def __init__(self, frame, world):
        """"""
        Frame.__init__(self, frame)
        self._world = world
        self._break = DoubleVar()

        runButton = Button(self, text="run simulation", command=self.run)
        breakScale \
        = Scale(self, variable=self._break, from_=0.1, to=2.0, resolution=0.1)
        stopButton = Button(self, text="stop running", command=self.stop)
        stepForwardButton \
        = Button(self, text="next step", command=self.stepForward)
        self._timeSpinbox = Spinbox(self, from_=0, to=2000)
        setButton = Button(self, text="set time", command=self.setTime)

        runButton.pack()
        breakScale.pack()
        stopButton.pack()
        stepForwardButton.pack()
        self._timeSpinbox.pack()
        setButton.pack()
        
    def setTime(self):
        """"""
        self._world.time = int(self._timeSpinbox.get())
        self._world.refresh()
        
    def run(self):
        """"""
        self._world.run([], self._break.get())
    
    def stepForward(self):
        """"""
        self._world.stepForward()
    
    def stop(self):
        """"""
        self._world.stop()

class GraphicCase(Case, Canvas):
    """Une extension graphique des cases de la simulation"""
        
    def __init__(self, loc, frame):
        """"""
        Case.__init__(self, loc)
        Canvas.__init__(self, frame)
            
class GraphicWorld(World, LabelFrame):
    """Une extension graphique du monde"""
        
    def __init__(self, configManager, frame):
        """"""
        LabelFrame.__init__(self, frame, text=configManager._file)
        self._counter = Label(self)
        World.__init__(self, configManager)
        self.refresh()
            
    def _build(self):
        """Mets en place les cases de la simulation"""
        for i in range(self._dim[0]):
            for j in range(self._dim[1]):
                self._map[(i, j)] = GraphicCase((i, j), self)
                self._map[(i, j)].grid(row=i, column=j)
        self._counter.grid(row=self._dim[0], columnspan=self._dim[1])
                
    def refresh(self):
        """Met à jour l'affichage"""
        w = 15
        h = 15
        for case in self._map.values():
            case.configure(width=w, height=h)
            if case._agent == None:
                case.configure(background=self._defaultColor)
            else:
                case.configure(background=case._agent._status.color)
        self._counter.configure(text="TIME : {}".format(self.time))
#        print(self)
        
    def stepForward(self):
        """"""
        super().stepForward()
        self.refresh()

class GUI(Tk):
    """La GUI de permettant de voir en direct la simulation...
       oui oui, en direct \o/"""
    
    def __init__(self):
        """"""
        Tk.__init__(self)
        self._world = None
        self._buttons = None
            
    def build(self, file="core/config/config.txt"):
        """Bâtie la simulation"""
        cm = ConfigManager(file)
        cm.setUpConfig()
        cm.load()
        self._world = GraphicWorld(cm, self)
        self._buttons = ButtonsFrame(self, self._world)
        self._world.pack(side=LEFT, fill=Y)
        self._buttons.pack(side=RIGHT)
        
gui = GUI()
gui.build()
gui.mainloop()