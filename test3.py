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
from array import array
from kivy.animation import Animation

color = [(255, 0, 255), (113, 0, 255), (51, 0, 255), (33, 0, 255), (24, 0, 255), (19, 0, 255), (16, 0, 255), (14, 0, 255), (12, 0, 255), (11, 0, 255), (9, 0, 255), (9, 0, 255), (8, 0, 255), (7, 0, 255), (7, 0, 255), (6, 0, 255), (6, 0, 255), (5, 0, 255), (5, 0, 255), (5, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255)]
class RectBlock(Widget):
    def __init__(self,texture_array,xsize,ysize, **kwargs):
        super(RectBlock, self).__init__(**kwargs)
        self.texture = Texture.create(size=(xsize, ysize))
        self.arr = texture_array
        self.setSize(xsize,ysize)
        self.update()
        #Clock.schedule_interval(self.update, 1.0 / 10.0)
    x_size = NumericProperty(0)
    y_size = NumericProperty(0)
    x_pos = NumericProperty(800)
    y_pos = NumericProperty(0)

    def setSize(self,xsize,ysize):
        self.x_size = xsize
        self.y_size = ysize


    def moveToLeft(self,amount):
        self.x_pos -= amount

    def update(self):
        self.texture.blit_buffer(self.arr, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            #self.opacity = 0.7
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=(self.x_size,self.y_size))
        #self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.canvas.clear()
        self.rect.pos = self.pos
        self.rect.size = self.size

class MathController(Widget):
    def __init__(self,**kwargs):
        super(MathController, self).__init__(**kwargs)
        self.filename = ""
        self.resolution = 0
        self.fs = 0
        self.wav_array = []
        self.signal_chunks = []
        self.fft_result = []
        self.signal_decibels = []
        self.color_table = []
        self.line_width = 0
        self.line_height = 0
        self.iteration = 0
        self.signal_length = len(self.color_table)

    def setFilename(self,filename):
        self.filename = filename

    def setResolution(self,resolution):
        self.resolution = resolution

    def setFS(self,fs):
        self.fs = fs

    def setLineWidth(self,width):
        self.line_width = width

    def setLineHeight(self,height):
        self.line_height = height

    def wavToArray(self):
        file = self.filename
        a = read(file)
        array = np.array(a[1], dtype=float)
        self.wav_array = array

    def getChunks(self):
        signal = self.wav_array
        fs = self.fs
        res = self.resolution
        signal_length = len(signal)
        signal_length_seconds = signal_length / fs
        # resolution = int(np.ceil(fs * chunk_length)) #in samples per square on xaxis
        resolution = res
        iterations = int(np.ceil(signal_length / resolution))
        output = []
        print("iterations: " + str(iterations))
        print("signal_length: " + str(signal_length))
        print("signal_length_seconds: " + str(signal_length_seconds))
        print("resolution: " + str(resolution))
        for i in range(iterations):
            chunk = signal[i * resolution:((i + 1) * resolution) + 100]
            # chunk = signal[i*resolution:(i+1)*resolution]
            output.append(chunk)
        self.signal_chunks = output

    def toDecibels(self):
        output = []
        for chunk in self.fft_result:
            chunks = []
            for value in chunk:
                abs = np.absolute(value)
                if(abs <= 0):
                    db = -100
                else:
                    db = 10*np.log10(abs)
                chunks.append(db)
            output.append(chunks)
        self.signal_decibels = output
        print(len(self.signal_chunks))


    def genFft(self,sig,N):
        y = np.fft.rfft(sig)
        modul = np.abs(y) / (N / 2)
        return (y, modul)

    def getFFT(self):
        signal = self.signal_chunks
        output = []
        for chunk in signal:
            fft = genFft(chunk, len(chunk))[1]
            output.append(fft)
        self.fft_result = output

    def genColors(self):
        signal = self.fft_result
        output = []
        for chunk in signal:
            result = []
            max_value = 0
            for value in chunk:
                if(value>max_value):
                    max_value = value
            resolution = max_value/510
            for value in chunk:
                val = np.floor(value/resolution)
                if(val <= 255):
                    color = (int(val),0,255)
                    result.append(color)
                if(val > 255):
                    color = (255,0,255-(int(val)-255))
                    result.append(color)
            output.append(result)
        self.color_table = output

    def genColorsDB(self):
        signal = self.signal_decibels
        output = []
        max_value = -1
        min_value = -1
        resolution = 0
        for chunk in signal:
            for value in chunk:
                if value < min_value:
                    min_value = value
                if value > max_value:
                    max_value = value
        resolution = (np.abs(max_value) + np.abs(min_value)) / 1275
        for chunk in signal:
            result = []
            for value in chunk:
                val = np.abs(np.floor(value/resolution))
                if(val <= 255):
                    color = (0,0,int(val))
                elif val > 255 and val <= 510:
                    color = (int(val)-255,0,255)
                elif val > 510 and val <= 765:
                    color = (255,0,255-(int(val)-510))
                elif val > 765 and val <= 1020:
                    color = (255,int(val)-765,0)
                elif val > 1020:
                    color = (255,255,int(val)-1020)
                result.append(color)
            output.append(result)
        self.color_table = output
        print(self.color_table)
        print(max_value)
        print(min_value)
        print(resolution)

    def getTextureArray(self):
        size = self.line_height * self.line_width * 3
        texture = Texture.create(size=(self.line_width,self.line_height))
        buf = []
        color = self.color_table[self.iteration]
        for i in range(len(color)):
            for j in range(self.line_width):
                for k in range(3):
                    buf.append(color[i][k])
        if (len(color) < 800):
            for i in range(self.line_height - len(color)):
                for j in range(self.line_width):
                    buf.append(0)
                    buf.append(0)
                    buf.append(0)
        arr = array('B', buf)
        self.iteration += 1
        return arr

    def getUpdatePeriod(self):
        return 1/(self.fs/self.resolution)

    def printPlot(self,signal):
        plt.plot(signal)
        plt.axis('tight')
        plt.show()




class Spectrogram(Widget):
    def __init__(self, **kwargs):
        super(Spectrogram, self).__init__(**kwargs)
        self.control = MathController()
        self.control.setFilename("output.wav")
        self.control.setFS(44100)
        self.control.setResolution(1024)
        self.control.setLineHeight(800)
        self.control.setLineWidth(5)
        self.control.wavToArray()
        self.control.getChunks()
        self.control.getFFT()
        self.control.toDecibels()
        #self.control.genColors()
        self.control.genColorsDB()
        self.updatePeriod = self.control.getUpdatePeriod()

        self.iteration = 0
        Clock.schedule_interval(self.updateChildren, self.updatePeriod)

    def createRectBlock(self):
        tex = self.control.getTextureArray()
        block = RectBlock(tex,self.control.line_width,self.control.line_height)
        self.add_widget(block)


    def updateChildren(self,dt):
        self.createRectBlock()
        for child in self.children:
            if child.pos[0] <= 0:
                self.remove_widget(child)
            child.moveToLeft(5)
            child.update()
            #self.iteration += 8
            print(dt)







class SpectroApp(App):
    def build(self):
        # spec = Spectrogram()
        # Clock.schedule_interval(spec.moveChildren, 1.0 / 43.0)
        # return spec
        # block = RectBlock()
        # return block
        # for i in range(30):
        #     controller.printPlot(controller.fft_result[i])
        spectro = Spectrogram()
        #spectro.createRectBlock()
        return spectro


SpectroApp().run()