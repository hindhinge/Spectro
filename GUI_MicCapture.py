from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial

from GUI_SpectroApp import Spectrogram
from GUI_Xaxis import Xaxis

class MicCapture(Widget):
    def __init__(self, parent,width,height,options_width,options_height,spec_width,spec_height,spec_linewidth, **kwargs):
        super(MicCapture, self).__init__(**kwargs)
        self.parent_widget = parent

        self.spectrogram = None

        self.SPEC_LINEWIDTH = spec_linewidth
        self.WINDOW_HEIGHT = height
        self.WINDOW_WIDTH = width
        self.OPTIONS_WIDTH = options_width
        self.OPTIONS_HEIGHT = options_height
        self.SPEC_WIDTH = spec_width
        self.SPEC_HEIGHT = spec_height

        self.xaxis = Xaxis(self.WINDOW_WIDTH,self.OPTIONS_WIDTH,self.OPTIONS_HEIGHT,self.SPEC_HEIGHT,self.SPEC_LINEWIDTH)

        self.layout_mic = BoxLayout()
        self.layout_mic.orientation = 'vertical'
        self.layout_mic.height = self.WINDOW_HEIGHT
        self.layout_mic.width = self.WINDOW_WIDTH

        self.add_options()
        self.add_spectro()

        self.add_widget(self.layout_mic)

    def add_options(self):
        layout_options = BoxLayout()
        layout_options.orientation = 'vertical'
        layout_options.size_hint_min_x = self.WINDOW_WIDTH
        layout_options.size_hint_max_x = self.WINDOW_WIDTH
        layout_options.size_hint_min_y = self.OPTIONS_HEIGHT
        layout_options.size_hint_max_y = self.OPTIONS_HEIGHT
        print("layout options pos " + str(layout_options.pos[0]) + " " + str(layout_options.pos[1]) )

        button_file = self.xaxis
        layout_options.add_widget(button_file)
        
        self.layout_mic.add_widget(layout_options)

    def add_spectro(self):
        layout_spectro = BoxLayout()
        layout_spectro.orientation = 'horizontal'
        layout_spectro.size_hint_min_x = self.WINDOW_WIDTH
        layout_spectro.size_hint_max_x = self.WINDOW_WIDTH
        layout_spectro.size_hint_min_y = self.SPEC_HEIGHT
        layout_spectro.size_hint_max_y = self.SPEC_HEIGHT

        button_file = Label(text="options")
        button_file.size_hint_min_x = self.OPTIONS_WIDTH
        button_file.size_hint_max_x = self.OPTIONS_WIDTH

        self.spectrogram = Spectrogram()

        layout_spectro.add_widget(self.spectrogram)
        layout_spectro.add_widget(button_file)

        self.layout_mic.add_widget(layout_spectro)