from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config
from mathfunctions import *
from sigops import *
import matplotlib.pylab as plt
import numpy as np
from scipy.io.wavfile import read
import simpleaudio as sa
from record import Recording
import pyaudio
from play import *
from chirp import *

import kivy
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import *
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.animation import *
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from array import array
from kivy.animation import Animation
from functools import partial

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '1440')
Config.set('graphics', 'height', '900')
Config.write()

class StartSelection(BoxLayout):
    def __init__(self,**kwargs):
        super(StartSelection,self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.font_size = 20
        self.text_welcome = 'Welcome to Spectro!'
        self.text_description = 'This application allows you to create spectrograms from sound files located on your computer or directly from your microphone.'
        self.text_source = 'Please choose the source of your signal: '
        self.text_madeby = 'Made by Radosław Sawicki\nPolitechnika Wrocławska\nWrocław 2021'

        self.add_texts()
        self.add_buttons()
        self.add_signature()

    def add_texts(self):
        text_layout = BoxLayout()
        text_layout.orientation = 'vertical'
        text_layout.size_hint = (1.0,0.2)

        textbox_welcome = Label(font_size = 40,text=self.text_welcome)
        textbox_welcome.size_hint = (1.0,0.7)
        textbox_description = Label(font_size = self.font_size,text=self.text_description)
        textbox_description.size_hint = (1.0, 0.15)
        textbox_source = Label(font_size = self.font_size, text=self.text_source)
        textbox_source.size_hint = (1.0, 0.15)

        text_layout.add_widget(textbox_welcome)
        text_layout.add_widget(textbox_description)
        text_layout.add_widget(textbox_source)

        self.add_widget(text_layout)

    def add_buttons(self):
        button_layout = BoxLayout()
        button_layout.orientation = 'horizontal'
        button_layout.size_hint = (1.0,0.7)
        button_layout.padding = [100,0,100,400]
        button_layout.spacing = 300

        button_file = Button(text="Use audio from file")
        button_file.bind(on_press=partial(self.use_file,button_file))
        button_file.size_hint = (0.3,0.3)
        button_mic = Button(text="Use audio from microphone")
        button_mic.bind(on_press=partial(self.use_mic,button_mic))
        button_mic.size_hint = (0.3, 0.3)

        button_layout.add_widget(button_file)
        button_layout.add_widget(button_mic)

        self.add_widget(button_layout)

    def add_signature(self):
        signature_layout = BoxLayout()
        signature_layout.orientation = 'horizontal'
        signature_layout.size_hint = (1.0,0.1)
        signature_layout.padding = [1300,0,0,0]


        textbox_madeby = Label(halign='right',valign = 'bottom',font_size=10, text=self.text_madeby)
        textbox_madeby.size_hint=(1.0,1.0)
        signature_layout.add_widget(textbox_madeby)
        self.add_widget(signature_layout)

    def use_file(self,instance,*args):
        self.parent.show_file()

    def use_mic(self,instance,*args):
        self.parent.show_mic()

class SpectroMic(Widget):
    def __init__(self,**kwargs):
        super(SpectroMic,self).__init__(**kwargs)
        self.add_widget(Label(text="mic check"))

class FileChooserI(FileChooserIconView):
    def __init__(self,ref,**kwargs):
        super(FileChooserI,self).__init__(**kwargs)
        self.ref = ref
    def on_submit(self,*args):
        try:
            self.path = args[0][0]
            print("self path:"+self.path)
            self.ref.set_filepath(self.path)
            self.ref.popup.dismiss()
        except(IndexError):
            print("ijo ijo error")


class SpectroFile(BoxLayout):
    def __init__(self,**kwargs):
        super(SpectroFile,self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.file_path = "adwdwadawdwad"
        self.popup = Popup()
        self.label_path = Label(text=self.file_path)

        button_path = Button(text='path')
        button_bottom = Button(text='bottom')
        button_option1 = Button(text='option1')
        button_option2 = Button(text='option2')
        button_option3 = Button(text='option3')


        layout_options = BoxLayout()
        layout_options.size_hint = (0.45, 1.0)
        layout_options.orientation = 'vertical'
        layout_options.add_widget(button_option1)
        layout_options.add_widget(button_option2)
        layout_options.add_widget(button_option3)

        layout_bottom = BoxLayout()
        layout_bottom.size_hint = (1.0, 0.6)
        layout_bottom.orientation = 'horizontal'
        layout_bottom.add_widget(button_bottom)
        layout_bottom.add_widget(layout_options)

        self.add_path()
        self.add_widget(layout_bottom)

    def add_path(self):
        label_path_prompt = Label(text='Select a file:\n(only .wav file extension supported)')
        button_path_select = Button(text='Select')
        button_path_select.bind(on_release = self.open_filechooser)

        layout_filepath = BoxLayout()
        layout_filepath.orientation = 'horizontal'
        layout_filepath.size_hint = (1.0, 0.3)
        layout_filepath.add_widget(self.label_path)
        layout_filepath.add_widget(button_path_select)

        layout_path = BoxLayout()
        layout_path.size_hint = (1.0, 0.3)
        layout_path.orientation = 'vertical'
        layout_path.add_widget(label_path_prompt)
        layout_path.add_widget(layout_filepath)
        self.add_widget(layout_path)

    def open_filechooser(self,*args):
        filechooser = FileChooserI(self, path='/')
        self.popup = Popup(title='Select file',content=filechooser,size=(1440,900))
        self.popup.open()
    def set_filepath(self,path):
        self.file_path = path
        self.label_path.text = self.file_path






class WindowWidget(Widget):
    def __init__(self,**kwargs):
        super(WindowWidget,self).__init__(**kwargs)
        self.window_height = 900
        self.window_width = 1440
        self.width = 1440
        self.height = 900

        self.start_selection = StartSelection()
        self.spectro_mic = SpectroMic()
        self.spectro_file = SpectroFile()

        self.set_size(self.start_selection,self.window_width,self.window_height)
        self.add_widget(self.start_selection)

    def set_size(self,instance,width,height):
        instance.height = height
        instance.width = width

    def show_mic(self):
        self.remove_widget(self.start_selection)
        self.set_size(self.spectro_mic, self.window_width, self.window_height)
        self.add_widget(self.spectro_mic)

    def show_file(self):
        self.remove_widget(self.start_selection)
        self.set_size(self.spectro_file, self.window_width, self.window_height)
        self.add_widget(self.spectro_file)

class Spectro(App):
    def build(self):
        return WindowWidget()




Spectro().run()