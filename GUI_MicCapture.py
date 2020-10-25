
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.graphics import *

from GUI_SpectroApp import Spectrogram
from GUI_Xaxis import Xaxis
from GUI_Yaxis import Yaxis

class MicCapture(Widget):
    def __init__(self, parent, **kwargs):
        super(MicCapture, self).__init__(**kwargs)
        self.parent_widget = parent

        self.spectrogram = None
        self.childlist = []

        self.SPEC_LINEWIDTH = self.parent_widget.getOptions().getInt('sline')
        self.WINDOW_HEIGHT = self.parent_widget.getOptions().getInt('wheight')
        self.WINDOW_WIDTH = self.parent_widget.getOptions().getInt('wwidth')
        self.OPTIONS_WIDTH = 50
        self.OPTIONS_HEIGHT = 100
        self.SPEC_WIDTH = self.parent_widget.getOptions().getInt('swidth')
        self.SPEC_HEIGHT = self.parent_widget.getOptions().getInt('sheight')
        self.CHUNK = self.parent_widget.getOptions().getInt('chunk')
        self.FS = self.parent_widget.getOptions().getInt('fs')
        self.TIMEFRAME = 1/(int(self.CHUNK)/int(self.FS))

        self.xaxis = Xaxis(self.parent_widget)

        self.layout_mic = BoxLayout()
        self.layout_mic.orientation = 'vertical'
        self.layout_mic.height = self.WINDOW_HEIGHT
        self.layout_mic.width = self.WINDOW_WIDTH
        
        self.layout_spectro = BoxLayout()

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

        backbutton = Button(text = '<-BACK', size_hint = (0.1,0.1))
        backbutton.bind(on_press=partial(self.goToStartScreen, backbutton))
        layout_options.add_widget(backbutton)

        xaxis = self.xaxis
        # button_file = BoxLayout()
        layout_options.add_widget(xaxis)
        
        self.layout_mic.add_widget(layout_options)

    def add_spectro(self):
        self.layout_spectro.orientation = 'horizontal'
        self.layout_spectro.size_hint_min_x = self.WINDOW_WIDTH
        self.layout_spectro.size_hint_max_x = self.WINDOW_WIDTH
        self.layout_spectro.size_hint_min_y = self.SPEC_HEIGHT
        self.layout_spectro.size_hint_max_y = self.SPEC_HEIGHT

        button_file = Yaxis(self.parent_widget)
        button_file.size_hint_min_x = self.OPTIONS_WIDTH
        button_file.size_hint_max_x = self.OPTIONS_WIDTH

        self.spectrogram = Spectrogram(self.parent_widget)

        self.layout_spectro.add_widget(self.spectrogram)
        self.layout_spectro.add_widget(button_file)

        self.layout_mic.add_widget(self.layout_spectro)

    def goToStartScreen(self,instance,*args):
        self.spectrogram.stopClock()
        self.spectrogram.clear_widgets()
        self.parent_widget.back_spectro()
