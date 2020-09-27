from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock

from math import ceil

from GUI_SpectroApp import TIMEFRAME
from GUI_RectBlock import SPEC_LINEWIDTH

class Xaxis(Widget):
    def __init__(self,width,height, **kwargs):
        super(Xaxis, self).__init__(**kwargs)
        print(TIMEFRAME)
        self.iteration = 1

        self.WINDOW_WIDTH = width
        self.OPTIONS_HEIGHT = height

        self.width = width
        self.height = height

        self.layout_numbers = BoxLayout()
        self.layout_numbers.size = (self.width,self.height)
        self.layout_numbers.pos = (50, 500)
        self.layout_numbers.orientation = 'horizontal'
        self.layout_numbers.add_widget(Label(text='ijo ijo pierwszy', font_size = 30))
        self.layout_numbers.add_widget(Label(text='ijo ijo drugi', font_size=40))
        self.add_widget(self.layout_numbers)

        self.baseNames = {1:['timescale_1.png',430],
                          2:['timescale_2.png',430],
                          3:['timescale_3.png',645],
                          4:['timescale_4.png',516],
                          5:['timescale_5.png',645]}
        self.secPerTexture = {1:10,2:5,3:5,4:3,5:3}
        self.basename = ''
        self.basewidth = 0
        self.rulers_amount = 0
        self.positionsStart = ()
        self.positionsReset = ()
        self.texture_base = None
        self.resetDone = False
        self.rulers = []

        with self.layout_numbers.canvas:
            Color(1.0,0.0,0.0)
            Rectangle(size=self.size,pos = (100,100))

        self.getBase()
        self.createRulers()

        Clock.schedule_interval(self.moveTexture, TIMEFRAME)

    def resetIterations(self):
        self.resetDone = True
        self.iteration = 1


    def getBase(self):
        self.basename = self.baseNames[SPEC_LINEWIDTH][0]
        self.basewidth = self.baseNames[SPEC_LINEWIDTH][1]
        self.texture_base = Image(self.basename).texture

    def createRulers(self):
        self.rulers_amount = ceil(self.WINDOW_WIDTH/self.basewidth) + 1
        positionsStart = []
        positionsReset = []
        for i in range(self.rulers_amount):
            posS = self.WINDOW_WIDTH + (i*self.basewidth)
            posR = i*self.basewidth
            positionsStart.append(posS)
            positionsReset.append(posR)
        self.positionsStart = tuple(positionsStart)
        self.positionsReset = tuple(positionsReset)
        for i in range(self.rulers_amount):
            self.rulers.append(Rectangle(texture=self.texture_base, pos=(self.WINDOW_WIDTH-self.iteration,0), size=(self.basewidth, 50)))

    def getPositions(self):
        positions = []
        for i in range(self.rulers_amount):
            if self.resetDone == False:
                pos = self.positionsStart[i] - (self.iteration*SPEC_LINEWIDTH)
            else:
                pos = self.positionsReset[i] - (self.iteration * SPEC_LINEWIDTH)
            if pos <= self.basewidth * -1:
                self.resetIterations()
            positions.append(pos)
        return tuple(positions)


    def moveTexture(self,dt):
        positions = self.getPositions()
        moved = 0
        self.canvas.clear()
        with self.canvas:
            for ruler in self.rulers:
                print("ruler " + str(moved) + " position is " + str(positions[moved]))
                ruler = Rectangle(texture=self.texture_base, pos=(positions[moved],100), size=(self.basewidth, 50))
                moved += 1
        self.iteration += 1


