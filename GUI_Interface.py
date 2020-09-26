from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from GUI_RectBlock import SPEC_WIDTH,SPEC_HEIGHT
from GUI_StartScreen import StartScreen
from GUI_SpectroApp import Spectrogram

from functools import partial
# #########GLOBALS##########
# #########Interface options##########
OPTIONS_HEIGHT = 100  # 100 pixels above the spectrogram for options and controls
OPTIONS_WIDTH = 50
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
        self.spectrogram = Spectrogram()
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
        self.layout_main.add_widget(self.spectrogram)

    def show_file(self):
        print("Unavailable")

class SpectroApp(App):
    def build(self):
        interface = Interface()
        return interface


setWindowDimension(WINDOW_WIDTH, WINDOW_HEIGHT)
SpectroApp().run()
        




