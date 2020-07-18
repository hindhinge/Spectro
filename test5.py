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
        self.texture = TextureRegion.create(size=(xsize, ysize))
        self.arr = texture_array
        self.setSize(xsize,ysize)
        self.update()
        self.iter = 1
        self.canvas.before.add(PushMatrix())
        self.canvas.before.add(Rotate(angle=-90,origin=self.center))
        self.canvas.after.add(PopMatrix())
    x_size = NumericProperty(0)
    y_size = NumericProperty(0)
    x_pos = NumericProperty(556)
    y_pos = NumericProperty(439)

    # def setTexture(self,arr):   #####in case of fuckup heres working
    #     tex = TextureRegion.create(size=(self.x_size, self.y_size))
    #     print(len(arr))
    #     self.texture = tex
    #     self.arr.extend(arr)
    #     self.update()

    def setTexture(self,arr):
        tex = TextureRegion.create(size=(self.x_size, self.y_size))
        print(len(arr))
        self.texture = tex
        if self.height < 1000:
            self.arr.extend(arr)
        else:
            del self.arr[0:13230]
            self.arr.extend(arr)
        self.update()


    def setSize(self,xsize,ysize):
        self.x_size = xsize
        self.y_size = ysize

    def moveToLeft(self,amount):
        self.x_pos -= amount

    def moveToLeftFlipped(self,amount):
        self.y_pos -= amount



    def increaseWidth(self,amount):
        self.x_size += amount

    def increaseWidthFlipped(self,amount):
        self.y_size += amount

    def update(self):
        self.texture.blit_buffer(self.arr, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=(self.x_size,self.y_size))
    def update_rect(self, *args):
        self.canvas.clear()
        self.rect.pos = self.pos
        self.rect.size = self.size

class MathController(Widget):
    def __init__(self,**kwargs):
        super(MathController, self).__init__(**kwargs)
        self.iter = 1
        self.height = 882
        self.width = 1000
        self.rec = Recording(1024,pyaudio.paInt16,2,44100,1,"mic_test.wav")
        self.rec.openStream()
        self.texture = self.getBlackTexture()
        self.rect = self.createRectBlock()
        self.rfreq = genRfreq(1024,44100)
        # Clock.schedule_interval(self.widenRectBlock, 1 / (44100 / 1024))

    def createRectBlock(self):
        block = RectBlock(self.texture,882,5)
        self.add_widget(block)
        return block

    def widenRectBlock(self,tex):
        if self.rect.height < 1000:
            self.rect.increaseWidthFlipped(5)
            self.rect.moveToLeftFlipped(5)
        self.rect.setTexture(tex)
        self.rect.update_rect()
        self.rect.update()
        self.iter += 1

    def microProcessing(self,dt):
        dft = self.getDft()
        dbs = self.toDecibels(dft)
        db_color = self.genColorsDB(dbs)
        tex_array = self.getTextureArray(db_color)
        self.widenRectBlock(tex_array)


    def genFft(self,sig, N):
        y = np.fft.rfft(sig)
        modul = np.abs(y) / (N / 2)
        return (y, modul)

    def getDft(self):
        chunk = self.rec.recordChunk()
        dft = self.genFft(chunk, 44100)
        return dft[1]

    def toDecibels(self,chunk):
        output = []
        sig = chunk[0:882]
        sig = sig[::-1]
        for value in sig:
            abs = np.absolute(value)
            if(abs <= 0):
                db = -40
                # if db > self.maxdbs:
                #     self.maxdbs = db
                # if db < self.mindbs:
                #     self.mindbs = db
                output.append(db)
            else:
                db = 10*np.log10(abs)
                # if db > self.maxdbs:
                #     self.maxdbs = db
                # if db < self.mindbs:
                #     self.mindbs = db
                output.append(db)
        return output

    def genColorsDB(self,dbs):
        signal = dbs
        max_value = 15
        min_value = -5
        output = []
        resolution = (max_value - min_value) / 1275
        for value in signal:
            if value > max_value:
                output.append((255,255,255))
            elif value < min_value:
                output.append((0,0,0))
            else:
                added_value = value - min_value
                val = added_value/resolution
                if (val <= 255):
                    color = (0, 0, int(val))
                    output.append(color)
                elif val > 255 and val <= 510:
                    color = (int(val) - 255, 0, 255)
                    output.append(color)
                elif val > 510 and val <= 765:
                    color = (255, 0, 255 - (int(val) - 510))
                    output.append(color)
                elif val > 765 and val <= 1020:
                    color = (255, int(val) - 765, 0)
                    output.append(color)
                elif val > 1020:
                    color = (255, 255, int(val) - 1020)
                    output.append(color)

        return output

    def getTextureArray(self,color):
        buffer = []
        for i in range(len(color)):
            rgb=color[i]
            if type(rgb) != int:
                for j in range(5):
                    for number in rgb:
                        buffer.append(number)
        arr = array('B',buffer)
        return arr

    def getBlackTexture(self):
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
        Clock.schedule_interval(self.control.microProcessing,1/(44100/1024))
        # for i in range(10):
        # self.control.microProcessing(1)

        # self.rect.moveToLeft(500)
        # self.rect.update_rect()
        # self.rect.update()








class SpectroApp(App):
    def build(self):
        spectro = Spectrogram()
        return spectro
SpectroApp().run()