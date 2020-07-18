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
#
# class RectBlock(Widget):
#     x_pos = NumericProperty(0)
#     y_pos = NumericProperty(0)
#     r = NumericProperty(0)
#     g = NumericProperty(0)
#     b = NumericProperty(0)
#     x_size = NumericProperty(8)
#     y_size = NumericProperty(8)
#
#     def setColor(self,color):
#         self.r = color[0]/255
#         self.g = color[1] / 255
#         self.b = color[2] / 255
#
#     def setPosition(self,x,y):
#         self.x_pos = x
#         self.y_pos = y
#
#
# class VerticalLine(Widget):
#     def __init__(self,linenumber,**kwargs):
#         super(VerticalLine, self).__init__(**kwargs)
#         self.linenumber=linenumber
#         self.initializePosition()
#
#     def initializePosition(self):
#         self.pos=(self.linenumber*8,0)
#
#     def addRectangles(self,colornum):
#         for pixel in range(100):
#             rect = RectBlock()
#             rect.setColor((255,0,255))
#             rect.setPosition(self.linenumber*rect.x_size,pixel*rect.y_size)
#             self.add_widget(rect)
#             print(rect.pos)
#         print(len(self.children))
#
#     def setPosition(self,x):
#         self.pos = (x,self.y)
#         for rect in self.children:
#             ypos = rect.pos[1]
#             rect.setPosition(x,ypos)
#
#     def moveToRight(self,x):
#         start = self.pos[0]
#         self.pos = (start+x,self.y)
#         for rect in self.children:
#             ypos = rect.pos[1]
#             rect.setPosition(start+x, ypos)
#
#     def calculate(self,dt):
#         self.moveToRight(1)
#
# class Spectrograph(Widget):
#     def __init__(self, **kwargs):
#         super(Spectrograph, self).__init__(**kwargs)
#         Clock.schedule_interval(self.calculate, 0.05)
#
#     def addVLines(self):
#         for i in range(50):
#             vline = VerticalLine(i)
#             self.add_widget(vline)
#     def addColors(self):
#         for vline in self.children:
#             vline.addRectangles(0)
#
#     def moveVLines(self,x):
#         for vline in self.children:
#             vline.moveToRight(x)
#
#     def calculate(self,dt):
#         self.moveVLines(8)
#
#
#
#
#
# class SpectroApp(App):
#     def build(self):
#         spectro = Spectrograph()
#         spectro.addVLines()
#         spectro.addColors()
#         return spectro
#
#
# SpectroApp().run()