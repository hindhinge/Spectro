from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock
from GUI_SpectroApp import TIMEFRAME
from GUI_RectBlock import SPEC_LINEWIDTH

class Xaxis(Widget):
    def __init__(self,width, **kwargs):
        super(Xaxis, self).__init__(**kwargs)
        print(TIMEFRAME)
        self.iteration = 1
        self.WINDOW_WIDTH = width
        self.texture_base = Image('timescale_2.png').texture
        with self.canvas:
            self.rect=Rectangle(texture=self.texture_base,pos=(self.WINDOW_WIDTH,800),size=(430,50))
        Clock.schedule_interval(self.moveTexture, TIMEFRAME)

    def moveTexture(self,dt):
        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(texture=self.texture_base, pos=(self.WINDOW_WIDTH-self.iteration, 800), size=(430, 50))
        self.iteration += 2


