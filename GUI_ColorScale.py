from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
from kivy.core.image import Image, Texture
from kivy.clock import Clock
from GUI_Xaxis_NumberGenerator import NumberGenerator
from GUI_Xaxis_Ruler import Ruler
from array import array
from kivy.graphics import *
from kivy.graphics.texture import TextureRegion

from math import ceil

class ColorScale(Widget):
    def __init__(self, parent, **kwargs):
        super(ColorScale, self).__init__(**kwargs)
        self.interface_widget = parent
        self.options = self.interface_widget.getOptions()
        self.WINDOW_WIDTH = self.options.getInt('wwidth')
        self.WINDOW_HEIGHT = self.options.getInt('wheight')
        self.OPTIONS_HEIGHT = 100
        self.OPTIONS_WIDTH = 50
        self.SPEC_LINEWIDTH = self.options.getInt('sline')
        self.height = 10
        self.width = 255
        self.texture = TextureRegion.create(size=(self.width,self.height))
        
        self.layout_scale = BoxLayout()
        self.layout_scale.width = self.width
        self.layout_scale.height = self.height
        self.layout_scale.orientation = 'horizontal'
        if self.options.get('zaxis')=='lin':
            self.max = self.options.getFloat('maxlin')
            self.min = self.options.getFloat('minlin')
        else:
            self.max = self.options.getInt('maxdb')
            self.min = self.options.getInt('mindb')
        self.diff = (self.max - self.min)/10
        for i in range(11):
            self.layout_scale.add_widget(Label(font_size=8, text=str("{:.1f}").format(self.min+(i*self.diff))))
        self.layout_scale.pos = ((self.WINDOW_WIDTH/2)-(self.width/2),self.WINDOW_HEIGHT-self.height - 10)
        self.add_widget(self.layout_scale)
        
        self.arr = self.generateTexture()
        self.setTexture()


    def generateTexture(self):
        size =  self.width
        val_per_line = 5
        buf = []
        for j in range(self.height):
            currval = 0
            for i in range(self.width):
                if (currval <= 255):
                    buf.append(0)
                    buf.append(0)
                    buf.append(currval)
                elif currval > 255 and currval <= 510:
                    buf.append(currval-255)
                    buf.append(0)
                    buf.append(255)
                elif currval > 510 and currval <= 765:
                    buf.append(255)
                    buf.append(0)
                    buf.append(255-(currval-510))
                elif currval > 765 and currval <= 1020:
                    buf.append(255)
                    buf.append(currval-765)
                    buf.append(0)
                elif currval > 1020:
                    buf.append(255)
                    buf.append(255)
                    buf.append(currval - 1020)
                print(currval)
                currval += val_per_line
        for i in range(len(buf)):
            val = buf[i]
            if val>255:
                print("za duzo w {0}".format(i))
            if val<0:
                print("za malo w {0}".format(i))

        arr = array('B', buf)
        return arr

    def setTexture(self):
        self.texture.blit_buffer(self.arr, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            self.rect = Rectangle(texture=self.texture, pos=((self.WINDOW_WIDTH/2)-(self.width/2),self.WINDOW_HEIGHT-self.height), size=(self.width,self.height))
