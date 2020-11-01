from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from GUI_StartScreen import StartScreen
from GUI_MicCapture import MicCapture
from GUI_Xaxis import Xaxis
from GUI_OptionsScreen import OptionsScreen
from GUI_Options import Options
from kivy.core.window import Window
from GUI_Yaxis import Yaxis


from functools import partial
# #########GLOBALS##########
# #########Interface options##########
from GUI_Xaxis_NumberGenerator import NumberGenerator

OPTIONS_HEIGHT = 100  # 100 pixels above the spectrogram for options and controls
OPTIONS_WIDTH = 50  # 50 pixels to the right of spectrogram for frequency scale

class Interface(Widget):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.options = Options()
        self.screen_start = StartScreen(self)
        self.screen_options = OptionsScreen(self)
        self.mic_capture = None
        self.WINDOW_WIDTH = self.options.getInt('wwidth')
        self.WINDOW_HEIGHT = self.options.getInt('wheight')
        self.width = self.WINDOW_WIDTH
        self.height = self.WINDOW_HEIGHT
        Window.size = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)


        self.layout_main = BoxLayout()
        self.layout_main.orientation = 'vertical'
        self.layout_main.width = self.WINDOW_WIDTH
        self.layout_main.height = self.WINDOW_HEIGHT
        self.layout_main.add_widget(self.screen_start)

        self.add_widget(self.layout_main)

    def show_mic(self):
        self.layout_main.remove_widget(self.screen_start)
        self.mic_capture = MicCapture(self)
        self.layout_main.add_widget(self.mic_capture)

    def show_options(self):
        self.layout_main.remove_widget(self.screen_start)
        self.screen_options.setDimensions(self.options.get('wwidth'),self.options.get('wheight'))
        self.layout_main.add_widget(self.screen_options)

    def setWindowDimension(self, width, height):
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'width', width)
        Config.set('graphics', 'height', height)
        Config.write()

    def getOptions(self):
        return self.options

    def back_options(self):
        self.WINDOW_WIDTH = self.options.get('wwidth')
        self.WINDOW_HEIGHT = self.options.get('wheight')
        self.width = self.WINDOW_WIDTH
        self.height = self.WINDOW_HEIGHT
        self.layout_main.remove_widget(self.screen_options)
        self.screen_start = StartScreen(self)
        Window.size = (self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        self.layout_main.add_widget(self.screen_start)
        
    def back_spectro(self):
        self.mic_capture.clear_widgets()
        self.layout_main.remove_widget(self.mic_capture)
        self.layout_main.add_widget(self.screen_start)


# class SpectroApp(App):
#     def build(self):
#         interface = Interface()
#         interface.setWindowDimension(interface.WINDOW_WIDTH,interface.WINDOW_HEIGHT)
#         # yaxis = Yaxis(interface)
#         # return yaxis
#         return interface
#
#         # options = OptionsScreen(self,WINDOW_WIDTH,WINDOW_HEIGHT)
#         # return options
#
# SpectroApp().run()
        




