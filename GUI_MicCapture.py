
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial

from GUI_SpectroApp import Spectrogram
from GUI_Xaxis import Xaxis

class MicCapture(Widget):
    def __init__(self, parent, **kwargs):
        super(MicCapture, self).__init__(**kwargs)
        self.parent_widget = parent

        self.spectrogram = None

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

        # button_file = self.xaxis
        button_file = BoxLayout()
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

        self.spectrogram = Spectrogram(self.parent_widget)

        layout_spectro.add_widget(self.spectrogram)
        layout_spectro.add_widget(button_file)

        self.layout_mic.add_widget(layout_spectro)