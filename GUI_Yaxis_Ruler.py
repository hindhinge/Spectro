from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock

class Ruler(Widget):
    def __init__(self,xpos,ypos, **kwargs):
        super(Ruler, self).__init__(**kwargs)
        self.width = 25
        self.height = 42
        self.texture_name = 'freq_timescale.png'
        self.texture = Image(self.texture_name).texture
        with self.canvas:
            rect = Rectangle(texture=self.texture,pos=(xpos,ypos),size=(self.width,self.height))
