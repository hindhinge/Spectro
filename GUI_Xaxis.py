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
from GUI_Xaxis_NumberGenerator import NumberGenerator
from GUI_Xaxis_Ruler import Ruler

class Xaxis(Widget):
    def __init__(self,width,options_width,height,window_height,linewidth, **kwargs):
        super(Xaxis, self).__init__(**kwargs)
        print(TIMEFRAME)
        self.iteration = 1

        self.WINDOW_WIDTH = width
        self.OPTIONS_HEIGHT = height
        self.WINDOW_HEIGHT = window_height
        self.OPTIONS_WIDTH = options_width
        self.SPEC_LINEWIDTH = linewidth

        self.width = width
        self.height = height

        self.layout_xaxis = BoxLayout()
        self.layout_xaxis.size = (self.width,self.height)
        self.layout_xaxis.orientation = 'vertical'
        self.layout_xaxis.spacing = 0
        
        self.layout_xaxis.add_widget(NumberGenerator(self.WINDOW_WIDTH,35,self.WINDOW_HEIGHT,self.SPEC_LINEWIDTH,self.OPTIONS_WIDTH))
        self.layout_xaxis.add_widget(Ruler(self.WINDOW_WIDTH,15,self.WINDOW_HEIGHT,self.SPEC_LINEWIDTH,self.OPTIONS_WIDTH))
        
        self.add_widget(self.layout_xaxis)


