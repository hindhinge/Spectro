from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock

from math import ceil

from GUI_Xaxis_NumberGenerator import NumberGenerator
from GUI_Xaxis_Ruler import Ruler


class Xaxis(Widget):
    def __init__(self, parent, **kwargs):
        super(Xaxis, self).__init__(**kwargs)
        self.iteration = 1
        self.interface_widget = parent
        self.options = self.interface_widget.getOptions()

        self.WINDOW_WIDTH = int(self.options.get('wwidth'))
        self.OPTIONS_HEIGHT = 100
        self.WINDOW_HEIGHT = int(self.options.get('wheight'))
        self.OPTIONS_WIDTH = 50
        self.SPEC_LINEWIDTH = int(self.options.get('sline'))
        self.TIMEFRAME = 1 / (int(self.options.get('chunk')) / int(self.options.get('fs')))

        self.width = int(self.options.get('wwidth'))
        self.height = self.OPTIONS_HEIGHT

        self.layout_xaxis = BoxLayout()
        self.layout_xaxis.size = (self.width, self.height)
        self.layout_xaxis.orientation = 'vertical'
        self.layout_xaxis.spacing = 0

        self.layout_xaxis.add_widget(
            NumberGenerator(self.WINDOW_WIDTH, 35, self.WINDOW_HEIGHT, self.SPEC_LINEWIDTH, self.OPTIONS_WIDTH,
                            self.TIMEFRAME))
        self.layout_xaxis.add_widget(
            Ruler(self.WINDOW_WIDTH, 15, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.SPEC_LINEWIDTH, self.OPTIONS_WIDTH,
                  self.TIMEFRAME))

        self.add_widget(self.layout_xaxis)


