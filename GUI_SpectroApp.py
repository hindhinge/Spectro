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
        self.width = self.interface_widget.getOptions().get('swidth')
        self.height = self.interface_widget.getOptions().get('sheight')
        self.chunk = int(self.interface_widget.getOptions().get('chunk'))
        self.fs = int(self.interface_widget.getOptions().get('fs'))
        self.timeframe = 1/(self.fs/self.chunk)
        self.control = MathController(self.interface_widget)
        self.add_widget(self.control)
        Clock.schedule_interval(self.control.microProcessing,self.timeframe)


