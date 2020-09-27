from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from GUI_RectBlock import SPEC_WIDTH,SPEC_HEIGHT, SPEC_LINEWIDTH
from GUI_StartScreen import StartScreen
from GUI_MicCapture import MicCapture
from GUI_Xaxis import Xaxis
from GUI_OptionsScreen import OptionsScreen

from functools import partial
# #########GLOBALS##########
# #########Interface options##########
OPTIONS_HEIGHT = 100  # 100 pixels above the spectrogram for options and controls
OPTIONS_WIDTH = 50  # 50 pixels to the right of spectrogram for frequency scale
WINDOW_HEIGHT = SPEC_HEIGHT + OPTIONS_HEIGHT
WINDOW_WIDTH = SPEC_WIDTH + OPTIONS_WIDTH



def setWindowDimension(width, height):
    Config.set('graphics', 'resizable', 0)
    Config.set('graphics', 'width', width)
    Config.set('graphics', 'height', height)
    Config.write()

class Interface(Widget):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.screen_start = StartScreen(self,WINDOW_WIDTH,WINDOW_HEIGHT)
        self.screen_options = OptionsScreen(self,WINDOW_WIDTH,WINDOW_HEIGHT)
        self.mic_capture = None
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT


        self.layout_main = BoxLayout()
        self.layout_main.orientation = 'vertical'
        self.layout_main.width = WINDOW_WIDTH
        self.layout_main.height = WINDOW_HEIGHT
        self.layout_main.add_widget(self.screen_start)

        self.add_widget(self.layout_main)

    def show_mic(self):
        self.layout_main.remove_widget(self.screen_start)
        self.mic_capture = MicCapture(self,WINDOW_WIDTH,WINDOW_HEIGHT,OPTIONS_WIDTH,OPTIONS_HEIGHT,SPEC_WIDTH,SPEC_HEIGHT,SPEC_LINEWIDTH)
        self.layout_main.add_widget(self.mic_capture)

    def show_file(self):
        self.layout_main.remove_widget(self.screen_start)

class SpectroApp(App):
    def build(self):
        interface = Interface()
        return interface
        # xaxis = Xaxis(WINDOW_WIDTH,OPTIONS_HEIGHT,SPEC_LINEWIDTH)
        # return xaxis

setWindowDimension(WINDOW_WIDTH, WINDOW_HEIGHT)
SpectroApp().run()
        




