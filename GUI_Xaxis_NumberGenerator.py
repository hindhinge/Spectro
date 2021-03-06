from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock

from math import ceil

class NumberGenerator(Widget):
    def __init__(self,parent,height, **kwargs):
        super(NumberGenerator, self).__init__(**kwargs)
        self.iteration = 1
        self.interface_widget = parent
        self.options = self.interface_widget.getOptions()


        self.OPTIONS_HEIGHT = 100
        self.OPTIONS_WIDTH = 50
        self.width = self.options.getInt('wwidth') - self.OPTIONS_WIDTH
        self.height = height
        self.SPEC_LINEWIDTH = self.options.getInt('sline')
        self.WINDOW_HEIGHT = self.options.getInt('wheight')
        self.TIMEFRAME = 1/(self.options.getInt('fs')/self.options.getInt('chunk'))
        print('key is {0}, value is {1}, type is {2}'.format("timeframe ngeneratr",self.TIMEFRAME,type(self.TIMEFRAME)))

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
        Clock.schedule_interval(self.calculate,self.TIMEFRAME)

    def appendNumber(self):
        label = Label(text = str(self.currentNumber), pos = (self.width - self.OPTIONS_WIDTH +2,self.WINDOW_HEIGHT-60 - self.height))
        self.numbers.append(label)
        self.add_widget(label)
        self.currentNumber += 1

    def moveNumbers(self):
        for number in self.numbers:
            number.pos = (number.pos[0] - self.SPEC_LINEWIDTH,self.WINDOW_HEIGHT-60 - self.height)

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


