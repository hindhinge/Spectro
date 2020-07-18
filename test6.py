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
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.animation import *
from kivy.graphics.texture import Texture
from kivy.graphics.texture import TextureRegion
from kivy.graphics.transformation import Matrix
from array import array
from kivy.animation import Animation
from record import Recording
from mathfunctions import genRfreq
import pyaudio

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '882')
Config.write()

class RectBlock(Widget):
    def __init__(self,texture_array,xsize,ysize, **kwargs):
        super(RectBlock, self).__init__(**kwargs)
        self.texture = Texture.create(size=(xsize, ysize))
        self.arr = texture_array
        self.setSize(xsize,ysize)
        self.update()
    x_size = NumericProperty(0)
    y_size = NumericProperty(0)
    x_pos = NumericProperty(995)
    y_pos = NumericProperty(0)

    def setSize(self,xsize,ysize):
        self.x_size = xsize
        self.y_size = ysize

    def update(self):
        print('update')
        self.texture.blit_buffer(self.arr, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=(self.x_size,self.y_size))

    def update_rect(self, *args):
        print('update reckt')
        self.canvas.clear()
        self.rect.pos = self.pos
        self.rect.size = self.size

    def setTexture(self,arr):
        print('setTexture')
        print(arr)
        tex = Texture.create(size=(self.x_size, self.y_size))
        self.texture = tex
        self.arr.extend(arr)
        self.update()

    def increaseWidth(self,amount):
        self.x_size += amount

    def moveToLeft(self,amount):
        self.x_pos -= amount

class MathController(Widget):
    def __init__(self,**kwargs):
        super(MathController, self).__init__(**kwargs)
        self.iter = 1
        self.height = 882
        self.width = 1000
        self.texture = self.getRedTexture()
        self.rect = self.createRectBlock()
        Clock.schedule_interval(self.widenRectBlock, 1 / (44100 / 1024))


    def createRectBlock(self):
        block = RectBlock(self.texture,5,882)
        self.add_widget(block)
        return block

    def widenRectBlock(self,dt):
        self.rect.increaseWidth(5)
        if self.iter%2 == 1:
            self.rect.setTexture(self.getRedTexture())
        else:
            self.rect.setTexture(self.getBlueTexture())
        self.rect.moveToLeft(5)
        self.rect.update_rect()
        self.rect.update()
        self.iter+=1

    def getRedTexture(self):
        size = 3 * 5 * 882
        buf = []
        for i in range(size):
            buf.append(255)
            buf.append(0)
            buf.append(0)
        arr = array('B',buf)
        return arr

    def getBlueTexture(self):
        size = 3 * 5 * 882
        buf = []
        for i in range(size):
            buf.append(0)
            buf.append(0)
            buf.append(255)
        arr = array('B',buf)
        return arr


class Spectrogram(Widget):
    def __init__(self, **kwargs):
        super(Spectrogram, self).__init__(**kwargs)
        self.iter = 1
        self.control = MathController()
        self.add_widget(self.control)

class SpectroApp(App):
    def build(self):
        spectro = Spectrogram()
        return spectro
SpectroApp().run()