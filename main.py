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

chirp = genChirp(1,20000,44100,10)
print(len(chirp))
# chunks = getChunks(chirp,44100,0.02,1024)
# fft = getFFT(chunks)
# colors = []
# for i in range(len(fft)):
#     line = convertToColors(fft[i])[0:100]
#     colors.append(line)
# #colors = convertToColors(fft[0])[0:100]
# print(colors[0])
#
# print(len(colors))
# print(len(colors[0]))

rec = Recording(1024, pyaudio.paInt16, 1, 44100, 3, "output.wav")
rec.record()
rec.save()

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')
Config.write()
color = [(255, 0, 255), (113, 0, 255), (51, 0, 255), (33, 0, 255), (24, 0, 255), (19, 0, 255), (16, 0, 255), (14, 0, 255), (12, 0, 255), (11, 0, 255), (9, 0, 255), (9, 0, 255), (8, 0, 255), (7, 0, 255), (7, 0, 255), (6, 0, 255), (6, 0, 255), (5, 0, 255), (5, 0, 255), (5, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255)]

# class RectBlock(Widget):
#     def __init__(self, **kwargs):
#         super(RectBlock, self).__init__(**kwargs)
#         self.texture = Texture.create(size=(8,800))
#         self.createTexture()
#         #size = 8 * 800 * 3
#
#         with self.canvas:
#             Rectangle(texture=self.texture, pos=(self.x_size,self.y_size), size=(8,800))
#     buf = []
#     x_size = NumericProperty(8)
#     y_size = NumericProperty(800)
#     x_pos = NumericProperty(0)
#     y_pos = NumericProperty(0)
#
#     def createTexture(self):
#         for i in range(100):
#             for j in range(64):
#                 for k in range(3):
#                     self.buf.append(color[i][k])
#         arr = array('B', self.buf)
#         self.texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
#
# class Spectrogram(Widget):
#     def __init__(self, **kwargs):
#         super(Spectrogram, self).__init__(**kwargs)
#         block = RectBlock()
#         block.createTexture()
#         self.add_widget(block)
#
#
# class SpectroApp(App):
#     def build(self):
#         #spec = Spectrogram()
#         #return spec
#         block = RectBlock()
#         block.createTexture()
#         return block
#
# SpectroApp().run()



# class RectBlock(Widget):
#     def __init__(self,r,g,b, **kwargs):
#         super(RectBlock, self).__init__(**kwargs)
#         self.r = r / 255
#         self.g = g / 255
#         self.b = b / 255
#     x_pos = NumericProperty(0)
#     y_pos = NumericProperty(0)
#     r = NumericProperty(255)
#     g = NumericProperty(255)
#     b = NumericProperty(255)
#     x_size = NumericProperty(8)
#     y_size = NumericProperty(8)
#
#
# class VerticalLine(Widget):
#     def __init__(self,line_number, **kwargs):
#         super(VerticalLine, self).__init__(**kwargs)
#         self.line_number = line_number
#     line_number = NumericProperty(0)
#     x_size = NumericProperty(8)
#     y_size = NumericProperty(800)
#
#     def animate(self):
#         anim = Animation(x=800,duration=18.576)
#         anim.start(self)
#
# class Spectrogram(Widget):
#     def __init__(self, **kwargs):
#         super(Spectrogram, self).__init__(**kwargs)
#
#     def addVLine(self,dt):
#         vline = VerticalLine(0)
#         vline.animate()
#         self.add_widget(vline)
#
#
#
#
#
# class SpectroApp(App):
#     def build(self):
#         spec = Spectrogram()
#         Clock.schedule_interval(spec.addVLine, 0.5)
#         return spec
#
#
# SpectroApp().run()

#I DO TEGO KVY PLIK
#:kivy 1.0.9
#:import RectBlock main.RectBlock
# <RectBlock>:
#     size: self.x_size,self.y_size
#     pos: self.x_pos,self.y_pos
#     canvas:
#         Color:
#             rgba: root.r,root.g,root.b,0.8
#         Rectangle:
#             pos: root.pos
#             size: root.x_size,root.y_size
#
# <VerticalLine>:
#     pos: self.line_number*self.x_size,0
#     size: self.x_size,self.y_size
#     BoxLayout:
#         size: self.parent.size
#         orientation: 'vertical'
#         pos: self.parent.pos
#         on_parent:
#             for i in range(100): id = "b{0}".format(i);self.add_widget(RectBlock(255,255,0))




















# class RectBlock(Widget):
#     def __init__(self,color, **kwargs):
#         super(RectBlock, self).__init__(**kwargs)
#         self.r = color[0]/255
#         self.g = color[1]/255
#         self.b = color[2]/255
#         self.x_size = 8
#         self.y_size = 8
#         with self.canvas:
#             self.color = Color(r=self.r,g=self.g,b=self.b,a=0.8)
#             self.rect = Rectangle(size=(self.x_size, self.y_size), pos=(0,0))
#
# class VerticalLine(Widget):
#     def __init__(self,linenumber,**kwargs):
#         super(VerticalLine, self).__init__(**kwargs)
#         self.linenumber=linenumber
#
#
#     def addRectangles(self,colornum):
#         for i in range(100):
#             for pixel in range(len(colors[colornum])):
#                 block = RectBlock(colors[colornum][pixel])
#                 block.rect.pos=(self.linenumber*block.x_size,pixel*block.y_size)
#                 self.add_widget(block)
#
#
#
#
#
#
# class Spectrograph(Widget):
#     def __init__(self, **kwargs):
#         super(Spectrograph, self).__init__(**kwargs)
#         self.height = 800
#         self.width = 800
#         self.iteration = 0
#
#         with self.canvas:
#             Color(r=1.0, g=1.0, b=1.0, a=0.5)
#             Rectangle(pos=(0,0),size=(self.height,self.width))
#
#     def addLine(self,position,colornum):
#         vline = VerticalLine(position)
#         vline.addRectangles(colornum)
#         self.add_widget(vline)
#
#
#
#
#
#
#
#
# class SpectroApp(App):
#     def build(self):
#         spectrograph = Spectrograph()
#         spectrograph.addLine(99,0)
#         return spectrograph
#
#
# SpectroApp().run()




