from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.widget import Widget
from GUI_MathController import MathController
from GUI_RectBlock import REC_FS,REC_CHUNK,SPEC_WIDTH,SPEC_HEIGHT


TIMEFRAME = 1/(REC_FS/REC_CHUNK)  # Amount of time between calculations. Defines how fast does spectrogram move


class Spectrogram(Widget):
    def __init__(self, **kwargs):
        super(Spectrogram, self).__init__(**kwargs)
        self.iter = 1
        self.width = SPEC_WIDTH
        self.height = SPEC_HEIGHT
        self.control = MathController()
        self.add_widget(self.control)
        Clock.schedule_interval(self.control.microProcessing,TIMEFRAME)


