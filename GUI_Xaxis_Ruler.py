from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock

from math import ceil


class Ruler(Widget):
    def __init__(self,parent,height, **kwargs):
        super(Ruler, self).__init__(**kwargs)
        self.iteration = 1
        self.interface_widget = parent
        self.options = self.interface_widget.getOptions()

        self.WINDOW_WIDTH = self.options.getInt('wwidth')
        self.OPTIONS_HEIGHT = height
        self.WINDOW_HEIGHT = self.options.getInt('wheight')
        self.OPTIONS_WIDTH = 50
        self.TIMEFRAME = 1/(self.options.getInt('fs')/self.options.getInt('chunk'))

        self.width = self.options.getInt('wwidth') - self.OPTIONS_WIDTH
        self.height = height
        self.SPEC_LINEWIDTH = self.options.getInt('sline')
        self.baseNames = {1: ['timescale_1.png', 430],
                          2: ['timescale_2.png', 430],
                          3: ['timescale_3.png', 645],
                          4: ['timescale_4.png', 516],
                          5: ['timescale_5.png', 645]}
        self.basename = ''
        self.basewidth = 0
        self.rulers_amount = 0
        self.positionsStart = ()
        self.positionsReset = ()
        self.texture_base = None
        self.resetDone = False
        self.rulers = []

        self.getBase()
        self.createRulers()

        Clock.schedule_interval(self.moveTexture, self.TIMEFRAME)

    def resetIterations(self):
        self.resetDone = True
        self.iteration = 0

    def getBase(self):
        self.basename = self.baseNames[self.SPEC_LINEWIDTH][0]
        self.basewidth = self.baseNames[self.SPEC_LINEWIDTH][1]
        self.texture_base = Image(self.basename).texture

    def createRulers(self):
        self.rulers_amount = ceil(self.WINDOW_WIDTH / self.basewidth) + 1
        positionsStart = []
        positionsReset = []
        for i in range(self.rulers_amount):
            posS = self.WINDOW_WIDTH + (i * self.basewidth) - self.OPTIONS_WIDTH
            posR = i * self.basewidth
            positionsStart.append(posS)
            positionsReset.append(posR)
        self.positionsStart = tuple(positionsStart)
        self.positionsReset = tuple(positionsReset)
        for i in range(self.rulers_amount):
            self.rulers.append(Rectangle(texture=self.texture_base, pos=(self.WINDOW_WIDTH - self.iteration -self.OPTIONS_WIDTH, self.WINDOW_HEIGHT),
                                         size=(self.basewidth, 14)))

    def getPositions(self):
        positions = []
        for i in range(self.rulers_amount):
            if self.resetDone == False:
                pos = self.positionsStart[i] - (self.iteration * self.SPEC_LINEWIDTH)
            else:
                pos = self.positionsReset[i] - (self.iteration * self.SPEC_LINEWIDTH)
            if pos <= self.basewidth * -1:
                self.resetIterations()
            positions.append(pos)
        return tuple(positions)

    def moveTexture(self, dt):
        positions = self.getPositions()
        moved = 0
        self.canvas.clear()
        with self.canvas:
            for ruler in self.rulers:
                # print("ruler " + str(moved) + " position is " + str(positions[moved]))
                ruler = Rectangle(texture=self.texture_base, pos=(positions[moved],self.WINDOW_HEIGHT-self.OPTIONS_HEIGHT-50), size=(self.basewidth, 14))
                moved += 1
        self.iteration += 1