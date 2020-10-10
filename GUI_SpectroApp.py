from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.widget import Widget
from GUI_MathController import MathController



class Spectrogram(Widget):
    def __init__(self,parent, **kwargs):
        super(Spectrogram, self).__init__(**kwargs)
        self.interface_widget = parent
        self.iter = 1
        self.width = self.interface_widget.getOptions().getInt('swidth')
        self.height = self.interface_widget.getOptions().getInt('sheight')
        self.chunk = self.interface_widget.getOptions().getInt('chunk')
        self.fs = self.interface_widget.getOptions().getInt('fs')
        self.timeframe = 1/(self.fs/self.chunk)
        self.control = MathController(self.interface_widget)
        self.add_widget(self.control)
        Clock.schedule_interval(self.control.microProcessing,self.timeframe)


