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

class NumberGenerator(Widget):
    def __init__(self,width,height,window_height,linewidth,options_width, **kwargs):
        super(NumberGenerator, self).__init__(**kwargs)
        self.iteration = 1
        self.width = width
        self.height = height
        self.SPEC_LINEWIDTH = linewidth
        self.OPTIONS_WIDTH = options_width
        self.WINDOW_HEIGHT = window_height

        self.baseWidths = {1: 430,
                          2: 430,
                          3: 645,
                          4: 516,
                          5: 645}
        self.secPerTexture = {1: 10, 2: 5, 3: 5, 4: 3, 5: 3}
        self.numbers = []
        
        self.iterationLimit = int(self.baseWidths[self.SPEC_LINEWIDTH]/self.SPEC_LINEWIDTH)
        self.numberLimit = ceil((self.width/self.baseWidths[self.SPEC_LINEWIDTH])*self.secPerTexture[self.SPEC_LINEWIDTH])
        self.currentNumber = 0

        self.appendNumber()

        Clock.schedule_interval(self.calculate, TIMEFRAME)

    def appendNumber(self):
        label = Label(text = str(self.currentNumber), pos = (self.width - 45 - self.OPTIONS_WIDTH,self.WINDOW_HEIGHT-50))
        self.numbers.append(label)
        self.add_widget(label)
        self.currentNumber += 1

    def moveNumbers(self):
        for number in self.numbers:
            number.pos = (number.pos[0] - self.SPEC_LINEWIDTH,self.WINDOW_HEIGHT)

    def deleteLowestNumber(self):
        self.remove_widget(self.numbers[0])
        del self.numbers[0]
    
    def calculate(self,dt):
        if len(self.numbers) > self.numberLimit:
            self.deleteLowestNumber()
        if self.iteration >= int(self.iterationLimit/self.secPerTexture[self.SPEC_LINEWIDTH]):
            self.appendNumber()
            self.iteration = 0
        self.moveNumbers()
        self.iteration += 1
        print("numbers number")
        print(len(self.numbers))

