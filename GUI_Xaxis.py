from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock
from GUI_Xaxis_NumberGenerator import NumberGenerator
from GUI_Xaxis_Ruler import Ruler

from math import ceil

class Xaxis(Widget):
    def __init__(self, parent, **kwargs):
        super(Xaxis, self).__init__(**kwargs)
        self.interface_widget = parent
        self.iteration = 1
        self.options = self.interface_widget.getOptions()

        self.WINDOW_WIDTH = self.options.getInt('wwidth')
        self.WINDOW_HEIGHT = self.options.getInt('wheight')
        self.OPTIONS_HEIGHT = 100
        self.OPTIONS_WIDTH = 50
        self.SPEC_LINEWIDTH = self.options.getInt('sline')

        self.width = self.WINDOW_WIDTH
        self.height = self.OPTIONS_HEIGHT/2

        self.layout_xaxis = BoxLayout()
        self.layout_xaxis.size = (self.width, self.height)
        self.layout_xaxis.orientation = 'horizontal'
        self.layout_xaxis.spacing = 0

        self.spacer = BoxLayout()
        self.spacer.width = self.OPTIONS_WIDTH
        self.spacer.height = self.OPTIONS_HEIGHT
        self.spacer.size_hint_max_x = self.OPTIONS_WIDTH

        self.layout_ruler = BoxLayout()
        self.layout_ruler.orientation = 'vertical'
        self.layout_ruler.width = self.WINDOW_WIDTH - self.OPTIONS_WIDTH
        self.layout_ruler.height = self.OPTIONS_HEIGHT

        ngenerator = NumberGenerator(self.interface_widget,35)
        ruler = Ruler(self.interface_widget,15)
        self.layout_ruler.add_widget(ngenerator)
        self.layout_ruler.add_widget(ruler)
        
        self.layout_xaxis.add_widget(self.layout_ruler)
        self.layout_xaxis.add_widget(self.spacer)
        
        self.add_widget(self.layout_xaxis)
        
