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
from kivy.graphics.texture import Texture
from array import array

import numpy as np

color = [(255, 0, 255), (113, 0, 255), (51, 0, 255), (33, 0, 255), (24, 0, 255), (19, 0, 255), (16, 0, 255), (14, 0, 255), (12, 0, 255), (11, 0, 255), (9, 0, 255), (9, 0, 255), (8, 0, 255), (7, 0, 255), (7, 0, 255), (6, 0, 255), (6, 0, 255), (5, 0, 255), (5, 0, 255), (5, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (4, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (3, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (2, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255), (1, 0, 255)]

class RectBlock(Widget):
    def __init__(self, **kwargs):
        super(RectBlock, self).__init__(**kwargs)
        texture = Texture.create(size=(8,800))
        size = 8 * 800 * 3
        buf = []
        cnt = 0
        for i in range(100):
            for j in range(64):
                for k in range(3):
                    buf.append(color[i][k])
        arr = array('B', buf)
        texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')

        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=(8,800))
    x_size = NumericProperty(8)
    y_size = NumericProperty(800)
    x_pos = NumericProperty(0)
    y_pos = NumericProperty(0)

    def animate(self):
        anim = Animation(x=800, duration=18.576)
        anim.start(self)


class VerticalLine(Widget):
    def __init__(self, line_number, **kwargs):
        super(VerticalLine, self).__init__(**kwargs)
        self.line_number = line_number

    line_number = NumericProperty(0)
    x_size = NumericProperty(8)
    y_size = NumericProperty(800)




class Spectrogram(Widget):
    def __init__(self, **kwargs):
        super(Spectrogram, self).__init__(**kwargs)

    def addVLine(self, dt):
        vline = VerticalLine(0)
        vline.animate()
        self.add_widget(vline)


class SpectroApp(App):
    def build(self):
        rect = RectBlock()
        return rect


SpectroApp().run()
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
#     linenumber = NumericProperty(0)
#     x_size = NumericProperty(8)
#     y_size = NumericProperty(800)
#     def move(self,dt):
#         self.pos[0] += 1
#
#
#
#
#
#
# class SpectroApp(App):
#     def build(self):
#         vline = VerticalLine()
#         return vline
#
#
# SpectroApp().run()







